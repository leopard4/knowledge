import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 설정 변수
EMBEDDING_MODEL = "text-embedding-ada-002"
PERSIST_DIR = "./chroma_db"
KNOWLEDGE_DIR = "./Knowledge_Base"

# (1) 모델/DB 캐싱 로직
if not os.path.exists(PERSIST_DIR):
    print("⏳ 처음 실행: 문서 로딩 및 벡터 DB 생성 중...")
    loader = DirectoryLoader(
        KNOWLEDGE_DIR,
        glob='**/*.md',
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'},
        recursive=True,
        show_progress=True
    )
    docs = loader.load()
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    db = Chroma.from_documents(docs, embeddings, persist_directory=PERSIST_DIR)
    db.persist()
    print("✅ 벡터 DB 생성 완료")
else:
    print("🚀 기존 벡터 DB 로딩 중...")
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    db = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    print("✅ DB 로딩 완료")

# (2) 개선된 검색 함수
def search(query: str, top_n: int = 3, min_length: int = 500):
    results = db.similarity_search_with_score(query, k=top_n*2)  # 후보군 확장
    
    seen = set()  # 중복 검사용
    filtered = []
    
    for doc, score in results:
        doc_id = doc.metadata.get('source', 'unknown')
        if doc_id not in seen:
            seen.add(doc_id)
            # 길이 조정 (min_length 적용)
            content = doc.page_content
            if len(content) < min_length:
                content += "..."  # 짧은 경우 표시
            else:
                content = content[:min_length] + "..."
            filtered.append((doc, score, content))
            if len(filtered) >= top_n:
                break
    
    print(f"\n🔍 '{query}' 검색 결과 (상위 {len(filtered)}개):")
    for i, (doc, score, content) in enumerate(filtered, 1):
        print(f"\n[{i}] (유사도: {score:.2f})")
        print(f"출처: {doc.metadata['source']}")
        print(f"내용: {content}")

# (3) 사용자 입력 처리
if __name__ == "__main__":
    while True:
        query = input("\n❓ 질문을 입력하세요 (종료: q): ")
        if query.lower() == 'q':
            break
        
        # 사용자 정의 옵션
        try:
            top_n = int(input("📌 표시할 결과 개수 (기본 3): ") or 3)
            min_length = int(input("📌 최소 내용 길이 (기본 500자): ") or 500)
        except ValueError:
            print("⚠️ 숫자만 입력 가능합니다. 기본값으로 진행합니다.")
            top_n, min_length = 3, 500
        
        search(query, top_n=top_n, min_length=min_length)

# todo gpu가속, 비동기처리, ui통합

# 동적 길이조정, 형식 강조, json 출력

# 정확도가 많이 떨어진다.