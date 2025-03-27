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

# todo 배치크기조절, 에러처리, 성능최적화