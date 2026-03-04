---
name: toolkit:mongodb
description: MongoDB 데이터베이스 작업. mongosh로 데이터 조회, 수정, 삭제, 집계를 수행합니다.
allowed-tools: Bash
disable-model-invocation: true
argument-hint: "[작업 설명]"
---

# /toolkit:mongodb - MongoDB 데이터베이스 작업

## 설명

mongosh를 사용하여 MongoDB 데이터베이스 작업을 수행합니다.
인터뷰를 통해 접속 정보를 확인한 후 요청된 작업을 진행합니다.

## 사용법

```bash
/toolkit:mongodb                      # 인터뷰 시작
/toolkit:mongodb 사용자 목록 조회      # 작업 힌트와 함께 시작
```

---

## 실행 절차

### Phase 1: 인터뷰 (필수)

**다음 정보를 텍스트로 한 번에 출력하여 수집합니다. 사용자 응답을 기다린 후 Phase 2로 진행합니다.**

```
MongoDB 작업에 필요한 정보를 입력해주세요.

1. 접속 URI: (기본: localhost:27017)
2. 데이터베이스 이름:
3. 작업 유형: 조회(find) / 수정(update) / 삭제(delete) / 집계(aggregate)
4. 컬렉션 이름: (목록 확인이 필요하면 "목록" 입력)
```

### Phase 2: 접속 테스트

```bash
mongosh "mongodb://{URI}/{DB}" --eval "db.runCommand({ ping: 1 })"
```

접속 실패 시 오류 메시지를 사용자에게 안내하고 URI 재확인 요청.

### Phase 3: 작업 수행

수집된 정보를 바탕으로 사용자 요청 작업 수행.

---

## mongosh 기본 사용법

### 접속
```bash
# 기본 접속
mongosh "mongodb://localhost:27017/{database}"

# 인증 포함
mongosh "mongodb://user:pass@host:port/{database}"

# 명령 실행
mongosh "mongodb://localhost:27017/{database}" --eval '<JavaScript>'
```

### 컬렉션 목록
```javascript
db.getCollectionNames()
```

### 조회 (find)
```javascript
// 전체 조회 (제한)
db.{collection}.find().limit(10)

// 조건 조회
db.{collection}.find({ field: "value" })

// 특정 필드만
db.{collection}.find({ field: "value" }, { name: 1, email: 1 })

// 정렬
db.{collection}.find().sort({ createdAt: -1 }).limit(10)

// 개수
db.{collection}.countDocuments({ field: "value" })
```

### 수정 (update)
```javascript
// 단일 문서
db.{collection}.updateOne(
  { _id: ObjectId("...") },
  { $set: { field: "newValue" } }
)

// 다중 문서
db.{collection}.updateMany(
  { status: "pending" },
  { $set: { status: "completed" } }
)
```

### 삭제 (delete)
```javascript
// 단일 문서
db.{collection}.deleteOne({ _id: ObjectId("...") })

// 다중 문서
db.{collection}.deleteMany({ status: "expired" })
```

### 집계 (aggregate)
```javascript
db.{collection}.aggregate([
  { $match: { status: "active" } },
  { $group: { _id: "$category", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])
```

---

## 작업 원칙

### 안전 규칙
| 규칙 | 설명 |
|------|------|
| **삭제/수정 전 확인** | `deleteMany`, `updateMany` 전 `countDocuments`로 대상 건수 확인 |
| **결과 보고** | 작업 후 영향받은 문서 수 보고 |
| **대량 작업 경고** | 100건 이상 변경 시 사용자 확인 |

### 출력 형식
```bash
# JSON 출력 제한
mongosh --eval "..." --quiet

# 보기 좋은 출력
mongosh --eval "printjson(db.{collection}.find().limit(5).toArray())"
```

---

## 사용 예시

### 예시 1: 사용자 조회
```
사용자: /toolkit:mongodb 최근 가입한 사용자 10명 조회

[인터뷰]
- 접속 URI: localhost:27017
- 데이터베이스: myapp
- 작업 유형: 조회
- 컬렉션: users

[실행]
mongosh "mongodb://localhost:27017/myapp" --eval \
  "printjson(db.users.find().sort({createdAt:-1}).limit(10).toArray())"
```

### 예시 2: 상태 업데이트
```
사용자: /toolkit:mongodb 만료된 세션 삭제

[인터뷰]
- 접속 URI: localhost:27017
- 데이터베이스: myapp
- 작업 유형: 삭제
- 컬렉션: sessions

[확인]
mongosh ... --eval "db.sessions.countDocuments({expiredAt:{$lt:new Date()}})"
→ 결과: 47건

[사용자 확인 후 실행]
mongosh ... --eval "db.sessions.deleteMany({expiredAt:{$lt:new Date()}})"
→ 결과: { deletedCount: 47 }
```

---

## 요구사항

| 항목 | 필수 |
|------|------|
| mongosh | 필수 |

### mongosh 설치
```bash
# macOS
brew install mongosh

# Ubuntu/Debian
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
sudo apt-get install -y mongodb-mongosh
```

---

## 관련 스킬

| 스킬 | 설명 |
|------|------|
| `/toolkit:solve` | 문제 해결 |
| `/toolkit:research` | 리서치 |
