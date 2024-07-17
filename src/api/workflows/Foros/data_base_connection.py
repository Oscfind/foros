from dotenv import load_dotenv
from qdrant_client import QdrantClient
from openai import OpenAI
import os

class DataBaseConnection:
        qdrant_client = QdrantClient(url="https://11c0c6de-74a5-44f2-976a-37089c2fdf5f.us-east4-0.gcp.cloud.qdrant.io", 
                        api_key=os.environ["QDRANT_API_KEY"])

        def encode_text(texto):
            load_dotenv()
            openai_api_key = os.environ['OPEN_AI__API_KEY']
            response = OpenAI(api_key=openai_api_key).embeddings.create(input=texto, model="text-embedding-3-large")
            return response.data[0].embedding


        def seach_context(qdrant_client, collection_name, embeding_pregunta):
            print(f"collection_name: {collection_name}")
            try:
                search_result = qdrant_client.search(collection_name=collection_name,
                                                    query_vector=embeding_pregunta,
                                                    limit=3)
                return search_result
            except:
                return f"La colección asociada al curso {collection_name} no existe"


        def create_context(search_result):
            print(f"Search_result: {search_result}, tipo: {type(search_result)}")
            context_text = "\n---\n".join([hit.payload['text'] for hit in search_result])
            return context_text