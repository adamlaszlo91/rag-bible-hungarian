from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.chains import RetrievalQA
from dummy_llm import DummyLLM
import os


class RAG:

    def __init__(self):
        self.init_embedding_model()
        self.dummy_llm = DummyLLM()
        self.qa = RetrievalQA.from_chain_type(llm=self.dummy_llm,
                                              chain_type='stuff',
                                              retriever=self.create_retriever(),
                                              return_source_documents=True)

    def init_embedding_model(self) -> None:
        print('Initializing embedding model...')
        model_name = 'BAAI/bge-m3'
        self.embedding = HuggingFaceEmbeddings(model_name=model_name)

    def create_retriever(self) -> VectorStoreRetriever:
        database = self.create_database()
        print('Creating retriever...')
        retriever = database.as_retriever(search_kwargs={'k': 3})
        return retriever

    def create_database(self) -> Chroma:
        documents = self.split_documents()
        chroma_database_dir = 'chroma_database'
        if os.path.isfile(chroma_database_dir + '/' + 'chroma.sqlite3'):
            print('Loading database...')
            database = Chroma(
                persist_directory=chroma_database_dir, embedding_function=self.embedding)
        else:
            print('Creating database...')
            os.makedirs(chroma_database_dir, exist_ok=True)
            database = Chroma.from_documents(
                persist_directory=chroma_database_dir, documents=documents, embedding=self.embedding)
        return database

    def split_documents(self) -> list[Document]:
        documents = self.create_documents()
        print('Splitting documents...')
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len,
        )
        return text_splitter.split_documents(documents)

    def create_documents(self) -> list[Document]:
        content = self.read_text_content()
        print('Creating documents...')
        documents = []
        books = content.split('\n{book_separator}\n')
        print(f'  Number of books: {len(books)}')
        for book in books:
            content = book.split('\n{content_separator}\n')
            book_title = content[0]
            chapters = content[1].split('\n{chapter_separator}\n')
            print(f'    {book_title} ({len(chapters)})')
            for chapter_index, chapter in enumerate(chapters):
                documents.append(Document(page_content=chapter, metadata={
                    'book': book_title, 'chapter': str(chapter_index+1)}))

        print(f'  Cumulated number of chapters: {len(documents)}')
        return documents

    def read_text_content(self) -> str:
        print('Reading text content...')
        file = open(file='assets/bible_hun.txt', mode='r')
        content = file.read()
        file.close()
        return content

    def query(self, text: str) -> list:
        response = self.qa.invoke(text)
        # Since we only care about the literal results, we use a lightweight dummy llm
        # just to complete the RAG pipeline. The displayed answer is constructed here.
        documents = response['source_documents']
        result = 'A legjobb találatok:'
        for document in documents:
            result += f'\n\n"{document.page_content}"\n{
                document.metadata['book']} ({document.metadata['chapter']}. Fejezet)'
        # If we used a normal LLM, it would be
        # return response['result']
        return result
