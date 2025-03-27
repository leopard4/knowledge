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

