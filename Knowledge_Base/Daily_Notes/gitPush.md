깃허브/깃랩에 코드를 푸시하는 방법을 단계별로 안내드리겠습니다. 🚀

---

### **1. 원격 저장소 연결**
**깃허브 예시:**
```bash
# 원격 저장소 추가 (HTTPS)
git remote add origin https://github.com/사용자명/저장소명.git

# 또는 SSH 사용 (권장)
git remote add origin git@github.com:사용자명/저장소명.git
```

---

### **2. 변경 사항 커밋**
```bash
# 모든 변경 파일 추가
git add .

# 커밋 메시지 작성
git commit -m "초기 버전: 지식 관리 시스템 구축"
```

---

### **3. 푸시 실행**
```bash
# 첫 푸시 (브랜치: main 또는 master)
git push -u origin main

# 이후 푸시는 간단히
git push
```

---

### **4. 자주 발생하는 오류 해결**
#### **(1) 인증 오류**
```bash
# 해결: 깃허브 계정 연결
git config --global credential.helper store
# 이후 푸시 시 사용자명/토큰 입력
```

#### **(2) "remote origin already exists"**
```bash
# 기존 원격 저장소 제거 후 재연결
git remote remove origin
git remote add origin [새 URL]
```

---

### **5. SSH 키 설정 (추천)**
**깃허브 SSH 설정 가이드:**
1. SSH 키 생성:
   ```bash
   ssh-keygen -t ed25519 -C "이메일@example.com"
   ```
2. 공개키 복사:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
3. 깃허브 → Settings → SSH and GPG keys → **New SSH key**에 붙여넣기

---

### **6. 확인 사항**
1. `.gitignore` 파일이 제대로 설정되었는지
2. `Knowledge_Base/.git` 폴더가 없는지 (이전 중첩 문제 해결)
3. ChromaDB 데이터 (`chroma_db/`)가 `.gitignore`에 포함되었는지

---

### **7. 최종 명령어 예시**
```bash
git add .
git commit -m "지식 베이스 업데이트: LLM 최적화 추가"
git push origin main
```

푸시가 완료되면 깃허브에서 코드를 확인할 수 있습니다! 🎉  
문제 발생 시 오류 메시지를 알려주시면 즉시 도와드리겠습니다 😊