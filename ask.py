import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 설정 변수
EMBEDDING_MODEL = "text-embedding-ada-002"  # 고성능 모델 선택
PERSIST_DIR = "./chroma_db"
KNOWLEDGE_DIR = "./Knowledge_Base"

# (1) 모델/DB 캐싱 로직
if not os.path.exists(PERSIST_DIR):
    print("⏳ 처음 실행: 문서 로딩 및 벡터 DB 생성 중...")
    
    # 문서 로드 (진행률 표시)
    loader = DirectoryLoader(
        KNOWLEDGE_DIR,
        glob='**/*.md',
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'},
        recursive=True,
        show_progress=True
    )
    docs = loader.load()
    
    # 벡터 DB 생성 (캐싱)
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    db = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory=PERSIST_DIR
    )
    db.persist()
    print("✅ 벡터 DB 생성 완료")
else:
    print("🚀 기존 벡터 DB 로딩 중...")
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    db = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    print("✅ DB 로딩 완료")

# (2) 검색 함수 (결과 3개 반환)
def search(query: str, top_n: int = 3):
    results = db.similarity_search_with_score(
        query,
        k=top_n
    )
    
    print(f"\n🔍 '{query}' 검색 결과 (상위 {top_n}개):")
    for i, (doc, score) in enumerate(results, 1):
        print(f"\n[{i}] (유사도: {score:.2f})")
        print(f"출처: {doc.metadata['source']}")
        print(f"내용: {doc.page_content[:200]}...")

# (3) 사용자 입력 처리
if __name__ == "__main__":
    while True:
        query = input("\n❓ 질문을 입력하세요 (종료: q): ")
        if query.lower() == 'q':
            break
        search(query)

# todo gpu가속, 비동기처리, ui통합