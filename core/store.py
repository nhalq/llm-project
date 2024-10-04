from fastapi import HTTPException
from pymongo.errors import OperationFailure
from pymongo import MongoClient
from core.embedding import create  # Import the create function from embedding.py

# MongoDB Atlas 
MONGODB_ATLAS_URI = "mongodb+srv://minhtri171997:test123@cluster0.vv0ot.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGODB_ATLAS_URI)
db = client['llm_db'] 
collection = db['llm_collection']
# embedding
embedding_model = create() 

class KnowledgeStore:
    def retrieve(self, query: str) -> str:
        relevant_data = self.search_knowledge(query)
        if relevant_data:
            return relevant_data
        else:
            return "Xin lỗi thông tin không tồn tại"

    def search_knowledge(self, query: str):
        query_embedding = compute_embedding(query)
        
        try:
            result = collection.aggregate([
                {
                    "$vectorSearch": {
                        "index": "vector_index",  
                        "path": "embedding",
                        "queryVector": query_embedding,
                        "numCandidates": 5,
                        "limit": 5
                    }
                },
                {
                    "$project": {
                        "text": 1, 
                        "score": {"$meta": "searchScore"} 
                    }
                }
            ])

            documents = list(result)
            if documents:
                return documents[0].get('text') 
            return None
        except OperationFailure as e:
            raise HTTPException(status_code=500, detail=f"MongoDB aggregation failed: {str(e)}")

def compute_embedding(text: str) -> list:
    return embedding_model.embed_documents([text])[0]
