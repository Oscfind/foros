from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import models, QdrantClient
from langchain.schema import Document
import openai
from openai import OpenAI
import numpy as np
from typing import List
from dotenv import load_dotenv
import os


def variables_de_entorno() -> None:
    """
    Activa la variable de entorno de OpenAI.
    """
    load_dotenv()
    openai.api_key = os.environ['OPENAI_API_KEY']


def conexion_qdrant_cliente(url_cluster: str):
    """
    Crea el cliente de Qdrant para conectarse a la colleción de la url hardcodeada.
    Devuelve el cliente creado.
    """
    qdrant_client = QdrantClient(url_cluster, 
                                 api_key=os.environ["QDRANT_API_KEY"])
    return qdrant_client


def pdf_to_document(data_path: str, archivo_pdf: str) -> List[Document]:
    """
    data_path: Directorio que almacema el pdf.
    archivo_pdf: Nombre del archivo pdf sin la extensión.
    Devuelve: Lista de documentos creados a partir del pdf.
    """
    loader = DirectoryLoader(data_path, glob=f"{archivo_pdf}.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents


def separacion_documentos(lista_documentos: List[Document], chunk_size: int=1000, chunk_overlap: int=500) -> List[Document]:
    """
    lista_documentos: Lista con los documentos generados a partir del pdf.
    chunk_size: Tamaño de cada uno de los chunks, 1000 por defecto.
    chunk_overlap: Traslapo entre los chunks, 500 por defecto.
    Devuelve: Lista de documentos "chunkeados" según los parámetros especificados.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                chunk_overlap=chunk_overlap,
                                                length_function=len,
                                                add_start_index=True)
    chunks = text_splitter.split_documents(lista_documentos)
    return chunks


def texto_embeddings(texto: str, modelo_embeddings: str="text-embedding-3-large") -> List[float]:
    """
    texto: Texto al que se le generarán embeddings.
    modelo_embeddings: text-embedding-3-large por defecto.
    Devuelve: Vector de embeddings para el texto ingresado.
    """
    response = OpenAI().embeddings.create(input=texto, model=modelo_embeddings) 
    return response.data[0].embedding


def codificar_chunks(chunks: List[Document], modelo_embeddings: str) -> List[List]:
    """
    chunks: Lista de chunks o fragmentos de los Documents.
    modelo_embeddings: Modelo para generar embeddings.
    Devuelve: Lista con los embeddings para cada uno de los chunks.
    """
    embedding_list = []
    for chunk in chunks:
        embedding = texto_embeddings(chunk.page_content, modelo_embeddings)
        embedding_list.append(embedding)
    return embedding_list


def subir_a_base_datos_qdrant(qdrant_client, chunks_embeddings: List[List], collection_name: str, documents_chunks: List[Document]) -> None:
    """
    qdrant_cliente: Cliente de Qdrant.
    chunks_embeddings: Embeddings de los chunks.
    collection_name: Nombre de la colección de Qdrant (nombre del curso).
    documents: Documents separados con el texto asociado a cada embedding.
    """
    vectors = np.array(chunks_embeddings)
    vector_size = len(chunks_embeddings[0])

    # Verificación de la existencia de la colección
    collections = qdrant_client.get_collections().collections
    collection_exists = any(collection.name == collection_name for collection in collections)

    # Asignación de índice para evitar sobre escritura
    if collection_exists:
        collection_info = qdrant_client.get_collection(collection_name=collection_name)
        start_point = collection_info.points_count
    else: 
        start_point = 0

    # Preparación de los puntos
    points = []
    for idx, (vector, chunk) in enumerate(zip(vectors, documents_chunks), start_point):
        point = models.PointStruct(
            id=idx,
            vector=vector.tolist(),
            payload={"text": chunk.page_content}
        )
        points.append(point)

    # Creación de la colección si no existe
    if not collection_exists:
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=vector_size,
                                        distance=models.Distance.COSINE)
        )

    # Insersión de datos en la colección
    qdrant_client.upsert(
        collection_name=collection_name,
        points=points
        )