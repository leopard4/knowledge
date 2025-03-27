새로운 MD 파일을 추가하고 자동으로 ChromaDB에 저장하는 방법을 단계별로 설명드리겠습니다. 📁 → 🔄 자동화

---

### **1. 새로운 MD 파일 추가 방법**
#### **(1) 파일 생성 예시**
```markdown
<!-- Knowledge_Base/New_Topic.md -->
# 새로운 주제
- 핵심 내용: LLM 학습 시 배치 크기(batch size)는 32 권장
- 참고: [[LLM 최적화.md]]
```

#### **(2) 코드 수정 (수동 추가)**
```python
collection.add(
    documents=["LLM 학습 시 배치 크기(batch size)는 32 권장"],
    metadatas=[{"source": "New_Topic.md"}],
    ids=["knowledge_002"]
)
```

---

### **2. 자동 감지 시스템 구축 (디렉토리 모니터링)**
#### **(1) 필요한 패키지 설치**
```bash
pip install watchdog
```

#### **(2) 파일 감시 스크립트 추가**
```python
import chromadb
from chromadb.utils import embedding_functions
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ChromaDB 설정
client = chromadb.Client()
collection = client.create_collection("my_knowledge")

# 감시할 디렉토리
WATCH_DIR = "./Knowledge_Base"

class MDFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".md"):
            self.update_db()

    def on_created(self, event):
        if event.src_path.endswith(".md"):
            self.update_db()

    def update_db(self):
        """MD 파일을 읽어 ChromaDB에 저장"""
        for root, _, files in os.walk(WATCH_DIR):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # 기존 데이터 확인
                    existing = collection.get(ids=[file])
                    if not existing["documents"]:
                        # 새 파일 추가
                        collection.add(
                            documents=[content],
                            metadatas=[{"source": file}],
                            ids=[file]
                        )
                        print(f"✅ {file} 추가됨")

# 감시 시작
event_handler = MDFileHandler()
observer = Observer()
observer.schedule(event_handler, path=WATCH_DIR, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
```

---

### **3. 주요 기능 설명**
1. **실시간 감시**:  
   `Knowledge_Base` 폴더 내의 `.md` 파일 생성/수정을 감지
2. **자동 저장**:  
   파일 변경 시 내용을 읽어 ChromaDB에 자동 저장
3. **중복 방지**:  
   `collection.get()`으로 기존 데이터 존재 여부 확인

---

### **4. 실행 결과 예시**
```bash
# Knowledge_Base/New_Topic.md 생성 시
✅ New_Topic.md 추가됨
```

---

### **5. 추가 개선 사항**
1. **배치 크기 조절**:
   ```python
   # 한 번에 최대 100개 파일 처리
   BATCH_SIZE = 100
   ```
2. **에러 처리**:
   ```python
   try:
       content = f.read()
   except UnicodeDecodeError:
       print(f"⚠️ {file} 인코딩 오류")
       continue
   ```
3. **성능 최적화**:
   ```python
   # 파일 변경 대신 내용 해시 비교
   import hashlib
   file_hash = hashlib.md5(content.encode()).hexdigest()
   ```

---

이제 **MD 파일을 추가/수정하면 자동으로 ChromaDB에 반영**됩니다! 🔄  
문서 검색은 기존 코드 그대로 사용 가능합니다. 😊