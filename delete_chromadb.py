import shutil
import os

# ChromaDB 데이터베이스 강제 삭제
if os.path.exists("./chroma_db"):
    shutil.rmtree("./chroma_db")
    print("✅ 기존 ChromaDB 삭제 완료")

# 새 데이터베이스 생성
db = Chroma.from_documents(
    docs,
    OpenAIEmbeddings(),
    persist_directory="./chroma_db"
)