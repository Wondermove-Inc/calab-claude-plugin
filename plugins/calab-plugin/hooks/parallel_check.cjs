#!/usr/bin/env node
/**
 * Parallel Check Executor - Generic Quality Check
 * Runs TypeScript, ESLint, and Prettier checks in parallel
 *
 * Output format:
 * 🔴 [Error] - Immediate fix required (TypeScript compile errors, ESLint errors)
 * 🟡 [Warning] - Immediate fix required (ESLint warnings)
 * 🟢 [Info] - No action needed (Prettier)
 *
 * Usage:
 *   node parallel_check.cjs <file_path>
 *
 * Configuration (via environment variables):
 *   CALAB_PROJECT_DIR - Project root directory
 *   CALAB_SKIP_TYPECHECK - Skip TypeScript check (1 to skip)
 *   CALAB_SKIP_ESLINT - Skip ESLint check (1 to skip)
 *   CALAB_SKIP_PRETTIER - Skip Prettier check (1 to skip)
 */

const { spawn, execSync } = require("child_process");
const path = require("path");
const fs = require("fs");

const filePath = process.argv[2];
if (!filePath) process.exit(0);

// Skip non-source files
const sourceExtensions = [".ts", ".tsx", ".js", ".jsx", ".vue", ".svelte"];
const ext = path.extname(filePath);
if (!sourceExtensions.includes(ext)) {
  process.exit(0);
}

// Get project root
const projectRoot = process.env.CALAB_PROJECT_DIR || process.cwd();

// Check which tools are available
function hasCommand(cmd) {
  try {
    execSync(`which ${cmd} 2>/dev/null || where ${cmd} 2>nul`, {
      stdio: "ignore",
    });
    return true;
  } catch {
    return false;
  }
}

function hasNpmScript(script) {
  try {
    const pkgPath = path.join(projectRoot, "package.json");
    if (!fs.existsSync(pkgPath)) return false;
    const pkg = JSON.parse(fs.readFileSync(pkgPath, "utf-8"));
    return pkg.scripts && pkg.scripts[script];
  } catch {
    return false;
  }
}

// Build check list based on available tools
const checks = [];

// TypeScript check
if (
  process.env.CALAB_SKIP_TYPECHECK !== "1" &&
  (hasNpmScript("typecheck") || fs.existsSync(path.join(projectRoot, "tsconfig.json")))
) {
  checks.push({
    name: "TypeScript",
    command: hasNpmScript("typecheck")
      ? "npm run typecheck --"
      : "npx tsc --noEmit",
    type: "error",
  });
}

// ESLint check
if (
  process.env.CALAB_SKIP_ESLINT !== "1" &&
  (hasNpmScript("lint") || fs.existsSync(path.join(projectRoot, ".eslintrc.js")) ||
   fs.existsSync(path.join(projectRoot, ".eslintrc.json")) ||
   fs.existsSync(path.join(projectRoot, "eslint.config.js")))
) {
  checks.push({
    name: "ESLint",
    command: hasNpmScript("lint")
      ? `npm run lint -- --format stylish "${filePath}"`
      : `npx eslint --format stylish "${filePath}"`,
    type: "mixed",
  });
}

// Prettier check
if (
  process.env.CALAB_SKIP_PRETTIER !== "1" &&
  (hasNpmScript("format:check") || fs.existsSync(path.join(projectRoot, ".prettierrc")) ||
   fs.existsSync(path.join(projectRoot, ".prettierrc.json")) ||
   fs.existsSync(path.join(projectRoot, "prettier.config.js")))
) {
  checks.push({
    name: "Prettier",
    command: `npx prettier --check "${filePath}"`,
    type: "info",
  });
}

// If no checks available, exit silently
if (checks.length === 0) {
  process.exit(0);
}

// Run checks in parallel
Promise.all(checks.map((check) => runCheck(check))).then((results) => {
  const errors = [];
  const warnings = [];
  const infos = [];

  results.forEach((r) => {
    if (r.success) {
      if (r.type === "info") {
        infos.push({ name: r.name, details: "Format check passed" });
      }
      return;
    }

    if (r.type === "error") {
      errors.push({ name: r.name, details: r.details });
    } else if (r.type === "mixed") {
      const { errorLines, warningLines } = classifyEslintOutput(r.details);
      if (errorLines) {
        errors.push({ name: r.name, details: errorLines });
      }
      if (warningLines) {
        warnings.push({ name: r.name, details: warningLines });
      }
      if (!errorLines && !warningLines && r.details) {
        errors.push({ name: r.name, details: r.details });
      }
    } else if (r.type === "info") {
      infos.push({ name: r.name, details: r.details });
    }
  });

  // Output errors and warnings
  if (errors.length > 0 || warnings.length > 0) {
    console.error("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");

    errors.forEach((e) => {
      const label = getErrorLabel(e.name);
      console.error(`\n🔴 [Error] ${label} - 즉시 수정 필요\n`);
      console.error(e.details);
    });

    warnings.forEach((w) => {
      console.error(`\n🟡 [Warning] ESLint 경고 - 즉시 수정 필요\n`);
      console.error(w.details);
    });

    infos.forEach((i) => {
      console.error(`\n🟢 [Info] ${i.name}\n`);
      console.error(`   ${i.details}`);
    });

    console.error("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    process.exit(2);
  }

  // All checks passed - silent exit
  process.exit(0);
});

function runCheck(check) {
  return new Promise((resolve) => {
    const proc = spawn("sh", ["-c", check.command], {
      cwd: projectRoot,
      stdio: ["ignore", "pipe", "pipe"],
      timeout: 30000,
    });

    let output = "";
    proc.stdout.on("data", (d) => (output += d));
    proc.stderr.on("data", (d) => (output += d));

    proc.on("close", (code) => {
      resolve({
        name: check.name,
        type: check.type,
        success: code === 0,
        details: code === 0 ? null : output.trim(),
      });
    });

    proc.on("error", (err) => {
      resolve({
        name: check.name,
        type: check.type,
        success: false,
        details: `Execution error: ${err.message}`,
      });
    });
  });
}

function getErrorLabel(name) {
  switch (name) {
    case "TypeScript":
      return "TypeScript compile error";
    case "ESLint":
      return "ESLint error";
    case "Prettier":
      return "Formatting error";
    default:
      return `${name} error`;
  }
}

function classifyEslintOutput(output) {
  if (!output) return { errorLines: null, warningLines: null };

  const lines = output.split("\n");
  const errorLines = [];
  const warningLines = [];
  let currentFile = null;

  lines.forEach((line) => {
    // Detect file path line
    if (line.match(/^[\/\w].*\.(ts|tsx|js|jsx)$/)) {
      currentFile = line;
      return;
    }

    // ESLint output format: "  10:5  error  message  rule-name"
    const match = line.match(/^\s*(\d+):(\d+)\s+(error|warning)\s+(.+)$/);
    if (match) {
      const severity = match[3];

      if (severity === "error") {
        if (currentFile && !errorLines.includes(currentFile)) {
          errorLines.push(currentFile);
        }
        errorLines.push(line);
      } else if (severity === "warning") {
        if (currentFile && !warningLines.includes(currentFile)) {
          warningLines.push(currentFile);
        }
        warningLines.push(line);
      }
    }
  });

  return {
    errorLines: errorLines.length > 0 ? errorLines.join("\n") : null,
    warningLines: warningLines.length > 0 ? warningLines.join("\n") : null,
  };
}
