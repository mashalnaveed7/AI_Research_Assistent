

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from langchain.chains import RetrievalQA


def create_vector_store(pages):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )


    documents = []

    for page_number, text in pages:

        chunks = splitter.split_text(text)

        for chunk in chunks:

            documents.append(
                {
                    "page": page_number,
                    "content": chunk
                }
            )


    texts = [
        doc["content"]
        for doc in documents
    ]

    metadatas = [
        {
            "page": doc["page"]
        }
        for doc in documents
    ]


    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


    vectorstore = FAISS.from_texts(
        texts,
        embeddings,
        metadatas=metadatas
    )


    return vectorstore




def ask_question(vectorstore, question, api_key):


    llm = ChatGroq(

        groq_api_key=api_key,

        model_name="llama-3.1-8b-instant"

    )


    qa_chain = RetrievalQA.from_chain_type(

        llm=llm,

        retriever=vectorstore.as_retriever(
            search_kwargs={
                "k":4
            }
        ),

        return_source_documents=True

    )


    result = qa_chain.invoke(
        {
            "query": question
        }
    )


    answer = result["result"]


    sources = result["source_documents"]


    pages = set()


    for doc in sources:

        pages.add(
            doc.metadata["page"]
        )


    return answer, pages
