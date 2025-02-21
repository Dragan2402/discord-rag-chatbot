import logging
import os

from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from application.services.rag_retrieval_service_interface import (
    RagRetrievalServiceInterface,
)
from langchain_astradb import AstraDBVectorStore
from langchain_community.document_loaders import PyPDFLoader

from helpers.env import EnvironmentKeys

ASTRA_DB_ENDPOINT = os.getenv(EnvironmentKeys.ASTRA_DB_ENDPOINT.value)
ASTRA_DB_TOKEN = os.getenv(EnvironmentKeys.ASTRA_DB_TOKEN.value)
OPEN_AI_KEY = os.getenv(EnvironmentKeys.OPEN_AI_KEY.value)


class OpenAiAstraRagRetrievalService(RagRetrievalServiceInterface):

    def __get_openai_model(self) -> OpenAIEmbeddings:
        return OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=OPEN_AI_KEY,
        )

    def __load_vector_store(self) -> AstraDBVectorStore:
        vector_store = AstraDBVectorStore(
            embedding=self.__get_openai_model(),
            collection_name="store_1",
            api_endpoint=ASTRA_DB_ENDPOINT,
            token=ASTRA_DB_TOKEN,
        )

        return vector_store

    def embed_files(self, files_location: str | None = None) -> None:
        docs = []

        pdf_files = []
        for root, _, files in os.walk(
            files_location if files_location else self.get_default_file_path()
        ):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_files.append(os.path.join(root, file))

        if not pdf_files:
            logging.warning("No PDF files found.")
            return

        vector_store = self.__load_vector_store()

        for file in pdf_files:
            loader = PyPDFLoader(file)

            docs.extend(loader.load())

            # Create the text splitter
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1500, chunk_overlap=100
            )

            # Vectorize the PDF and load it into the Astra DB Vector Store
            pages = text_splitter.split_documents(docs)

            vector_store.add_documents(pages)
            logging.info(f"{len(pages)} pages loaded.")
