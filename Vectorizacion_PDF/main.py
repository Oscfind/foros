from funciones import *
import logging

logging.basicConfig(filename="logger_info.log",
                    level=logging.DEBUG)
logger = logging.getLogger()


def main():
    
    # Cargar variable de entorno de openai
    variables_de_entorno()
    logger.info("Variables de entorno cargadas correctamente")

    # Nombre del curso (igual al nombre del pdf y de la colección de qdrant)
    curso_pdf = "Teología fundamental"
    url="https://11c0c6de-74a5-44f2-976a-37089c2fdf5f.us-east4-0.gcp.cloud.qdrant.io"
    modelo_embeddings = "text-embedding-3-large"
    path = "PDF"

    # Cargar archivo PDF a Document.
    documents = pdf_to_document(path, curso_pdf)
    logger.info("Documents cargados correctamente")

    # Creación de los chunks a partir de los Document.
    document_chunks = separacion_documentos(documents)
    logger.info("Documents chunkeados correctamente")

    # Creación de los embeddings a partir de los chunks de los Document.
    chunks_embeddings = codificar_chunks(document_chunks, modelo_embeddings)
    logger.info(f"Chunk embeddings cargados correctamente, chunk_size:{len(chunks_embeddings)}")

    # Creación de cliente Qdrant
    qdrant_client = conexion_qdrant_cliente(url)
    logger.info("Cliente de qdrant creado correctamente")

    # Actualizar o crear colección y agregar los nuevos embeddings.
    subir_a_base_datos_qdrant(qdrant_client, chunks_embeddings, curso_pdf, document_chunks)
    logger.info("Base de vectores cargada correctamente")
    

if __name__ == "__main__":
    main()