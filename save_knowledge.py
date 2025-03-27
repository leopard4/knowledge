import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()
collection = client.create_collection("my_knowledge")

# 지식 추가
collection.add(
    documents=["Temperature 0.7 설정은 창의성 향상에 효과적"],
    metadatas=[{"source": "LLM 최적화.md"}],
    ids=["knowledge_001"]
)

results = collection.query(query_texts=["LLM 창의성 향상 방법"], n_results=1)
print(results)  # 저장된 지식이 출력됨


# todo : md 파일을 자동으로 메타데이터로 저장
# todo2 : gitignore 적용이 제대로 되지 않음 chroma_db, __pycahe__ 는 제외됬어야 했음
# todo3 : knowledge_base 폴더가 올라가지지 않음