# Calab Plugin 설치/제거 가이드

## 설치

```bash
./install-plugin.sh
```

출력된 명령어를 복사해서 실행:

```bash
claude plugin marketplace add ~/.claude/calab-marketplace
claude plugin install calab-plugin@calab-marketplace --scope user
```

## 제거

```bash
claude plugin uninstall calab-plugin
claude plugin marketplace remove calab-marketplace
rm -rf ~/.claude/calab-marketplace
```

## 사용

```bash
/calab-plugin:onboard
/calab-plugin:dev-plan
/calab-plugin:research
```

상세: `CLAUDE.md`, `README.md`
