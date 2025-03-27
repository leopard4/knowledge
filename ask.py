from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 문서 로드
loader = DirectoryLoader(
    './Knowledge_Base',
    glob='**/*.md',  # 모든 하위 폴더의 .md 파일 포함
    loader_cls=TextLoader,
    loader_kwargs={'encoding': 'utf-8'},
    silent_errors=False,  # 오류 발생 시 확인 가능
    recursive=True,       # 하위 폴더 포함 검색
    show_progress=True    # 로딩 진행 상황 표시
)
docs = loader.load()

# 벡터 DB 생성
db = Chroma.from_documents(docs, OpenAIEmbeddings(), persist_directory="./chroma_db")


# 질문
# query = "LLM에서 Temperature 설정 방법은?"
query = input()
results = db.similarity_search(query)
print(f"🔍 '{query}' 검색 결과:")
print(results[0].page_content)  # 관련 지식 출력
