import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from utils import format_docs, create_response

# Ensure the /pdf directory exists
os.makedirs("pdf", exist_ok=True)

app = FastAPI()

# Template for the question-answer prompt
template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum and keep the answer as concise as possible.
Always say "thanks for asking!" at the end of the answer.

{context}

Question: {question}

Helpful Answer:"""
prompt = ChatPromptTemplate.from_template(template)

llm = ChatOpenAI()
output_parser = StrOutputParser()

embeddings = OpenAIEmbeddings()
vectorstore = None


@app.get("/")
async def root():
    """
    Root endpoint to test the API.
    """
    return create_response("Welcome to the Question Answering RAG system!", 200)


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)) -> JSONResponse:
    """
    Endpoint to upload a PDF file and process it into chunks for the vector store.

    Args:
        file (UploadFile): The PDF file to be uploaded.

    Returns:
        JSONResponse: Response indicating success or failure.
    """
    global vectorstore
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400, detail="Only PDF files are allowed.")

    file_path = os.path.join("pdf", file.filename)

    try:
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        reader = PyPDFLoader(file_path)
        docs = reader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        vectorstore = Chroma.from_documents(
            documents=splits, embedding=embeddings)
        return create_response("File uploaded successfully.", 200)
    except Exception as e:
        return create_response(f"Error processing file: {str(e)}", 500)


@app.post("/ask_question")
async def ask_question_endpoint(request: Request) -> JSONResponse:
    """
    Endpoint to ask a question based on the uploaded documents.

    Args:
        request (Request): The request object containing the question.

    Returns:
        JSONResponse: Response containing the answer to the question.
    """
    global vectorstore

    try:
        data = await request.json()
        question = data.get("question")

        if not question:
            return create_response("Question field is required.", 400)

        if not vectorstore:
            return create_response("No documents uploaded yet.", 400)

        retriever = vectorstore.as_retriever()
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | output_parser
        )

        answer = rag_chain.invoke(question)
        return create_response({"answer": answer}, 200)
    except Exception as e:
        return create_response(f"Error answering question: {str(e)}", 500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
