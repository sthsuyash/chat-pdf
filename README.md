# Question Answering RAG System

This project is a REST API for a Question Answering system using Retrieval-Augmented Generation (RAG) with OpenAI's language models. The system processes PDF documents, splits them into chunks, stores them in a vector store and allows users to ask questions based on the uploaded documents.

A RAG(Retrieval-Augmented Generation) model is a transformer-based model that combines the benefits of retrieval-based and generation-based models. It uses a retriever to find relevant passages from a large corpus of documents and then generates an answer based on the retrieved passages.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
  - [Root Endpoint](#root-endpoint)
  - [Upload PDF](#upload-pdf)
  - [Ask Question](#ask-question)
- [Project Structure](#project-structure)
- [License](#license)

## Features

- Upload PDF files and process them into document chunks.
- Store document chunks in a vector store for efficient retrieval.
- Ask questions based on the uploaded documents using a RAG approach.
- Consistent JSON response format for all endpoints.

## Requirements

- Python
- FastAPI
- Uvicorn
- PyPDF2
- Langchain libraries

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/sthsuyash/chat-pdf.git
   cd chat-pdf
   ```

2. Create a virtual environment:

   - For Windows:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

   - For MacOS/Linux:

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Start the FastAPI server:

   ```sh
   uvicorn main:app --reload
   ```

2. The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### Root Endpoint

- **GET /**
  - Description: Root endpoint to test the API.
  - Response:

    ```json
    {
      "status": "success",
      "data": {
        "message": "Welcome to the Question Answering RAG system!"
      }
    }
    ```

### Upload PDF

- **POST /upload_pdf**
  - Description: Upload a PDF file and process it into chunks for the vector store.
  - Request:
    - File: A PDF file.
  - Response:
    - Success:

      ```json
      {
        "status": "success",
        "data": {
          "message": "File uploaded successfully."
        }
      }
      ```

    - Error:

      ```json
      {
        "status": "error",
        "data": {
          "message": "Error processing file: <error_message>"
        }
      }
      ```

### Ask Question

- **POST /ask_question**
  - Description: Ask a question based on the uploaded documents.
  - Request:
    - JSON body:

      ```json
      {
        "question": "Your question here"
      }
      ```

  - Response:
    - Success:

      ```json
      {
        "status": "success",
        "data": {
          "answer": "The answer to your question."
        }
      }
      ```

    - Error:

      ```json
      {
        "status": "error",
        "data": {
          "message": "Error answering question: <error_message>"
        }
      }
      ```

## Project Structure

```readme
.
├── main.py             # Main FastAPI application
├── utils.py            # Utility functions for the application
├── requirements.txt    # Project dependencies
├── README.md           # Project documentation
└── pdf/                # Directory to store uploaded PDF files
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
