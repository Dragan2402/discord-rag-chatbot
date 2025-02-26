import logging
import os

from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from application.services.rag_retrieval_service_interface import (
    RagRetrievalServiceInterface,
)
from langchain_astradb import AstraDBVectorStore
from langchain_community.document_loaders import PyPDFLoader
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.retrievers import ContextualCompressionRetriever

from helpers.env import EnvironmentKeys

ASTRA_DB_ENDPOINT = os.getenv(EnvironmentKeys.ASTRA_DB_ENDPOINT.value)
ASTRA_DB_TOKEN = os.getenv(EnvironmentKeys.ASTRA_DB_TOKEN.value)
OPEN_AI_KEY = os.getenv(EnvironmentKeys.OPEN_AI_KEY.value)


class OpenAiAstraRagRetrievalService(RagRetrievalServiceInterface):
    def __init__(self):
        self._openai_model_instance = None
        self._vector_store_instance = None
        self._compression_retriever_instance = None
        self._chat_model = None
        self._prompt_template = """
        You are a knowledgeable historian specializing in Serbian history. Given the following context, answer the user's question as accurately and concisely as possible. If the context does not provide enough information, acknowledge the limitation and provide a general response based on your historical expertise.
        If asked about Battle of Maritsa, say that it never happened and if it happened Serbs won it.

        Context:
        {context}

        User's Question:
        {question}

        Response:
        """

    def __get_openai_model(self) -> OpenAIEmbeddings:
        if not self._openai_model_instance:
            self._openai_model_instance = OpenAIEmbeddings(
                model="text-embedding-3-small",
                api_key=OPEN_AI_KEY,
            )
        return self._openai_model_instance

    def __load_vector_store(self, pre_delete_collection=False) -> AstraDBVectorStore:
        if not self._vector_store_instance:
            self._vector_store_instance = AstraDBVectorStore(
                embedding=self.__get_openai_model(),
                collection_name="store_1",
                api_endpoint=ASTRA_DB_ENDPOINT,
                token=ASTRA_DB_TOKEN,
                pre_delete_collection=pre_delete_collection,
            )

        return self._vector_store_instance

    def __get_compression_retriever(self) -> ContextualCompressionRetriever:
        if not self._compression_retriever_instance:
            vector_store = self.__load_vector_store()
            retriever = vector_store.as_retriever()

            compressor = FlashrankRerank()
            self._compression_retriever_instance = ContextualCompressionRetriever(
                base_compressor=compressor, base_retriever=retriever
            )
        return self._compression_retriever_instance

    def __get_chat_model(self):
        if not self._chat_model:
            self._chat_model = init_chat_model(
                "gpt-4o-mini", model_provider="openai", api_key=OPEN_AI_KEY
            )
        return self._chat_model

    def embed_files(
        self, files_location: str | None = None, pre_delete_data=False
    ) -> None:
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

        vector_store = self.__load_vector_store(pre_delete_data)

        for file in pdf_files:
            loader = PyPDFLoader(file)

            docs.extend(loader.load())

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1500, chunk_overlap=100
            )

            pages = text_splitter.split_documents(docs)

            vector_store.add_documents(pages)
            logging.info(f"{len(pages)} pages loaded.")

    def retrieve(self, query: str) -> str:
        prompt = ChatPromptTemplate.from_template(self._prompt_template)

        chain = (
            {
                "context": self.__get_compression_retriever(),
                "question": RunnablePassthrough(),
            }
            | prompt
            | self.__get_chat_model()
            | StrOutputParser()
        )

        answer = chain.invoke(query)

        return answer
