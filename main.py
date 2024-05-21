from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_fireworks import FireworksEmbeddings
from langchain_fireworks import ChatFireworks
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv
import os
import logging
load_dotenv()
os.environ["FIREWORKS_API_KEY"] = os.getenv("FIREWORKS_API_KEY")

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = FireworksEmbeddings(model="nomic-ai/nomic-embed-text-v1.5")
    
    if embeddings is None:
        logging.error("Failed to initialize embeddings.")
        return
    
    try:
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")
    except Exception as e:
        logging.error("An error occurred while creating the vector store: %s", e)

def get_conversational_chain():
    prompt_template = """
    Please provide an appropriate response to the user input.
    If the input is a general conversation (like greetings or small talk), respond accordingly. 
    If the input is a specific question related to the provided context, answer the question using the context information. 
    If the answer is not available in the context, simply state, "The answer is not available in the context."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    model = ChatFireworks(model_name="accounts/fireworks/models/mixtral-8x7b-instruct",
                          temperature=0.0,
                          verbose=True)

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(user_question):
    general_conversation_keywords = ["hi", "hello", "hey", "how are you", "good morning", "good evening", "what's up"]

    if any(keyword in user_question.lower() for keyword in general_conversation_keywords):
        general_response = handle_general_conversation(user_question)
        return general_response

    embeddings = FireworksEmbeddings(model="nomic-ai/nomic-embed-text-v1.5")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    try:
        response = chain(
            {"input_documents": docs, "question": user_question},
            return_only_outputs=True
        )
        return response["output_text"]
    except BlockedPromptException as e:
        return "Error: " + str(e)

def handle_general_conversation(user_question):
    # Add more sophisticated logic for handling general conversation if needed
    general_responses = {
        "hi": "Hello! How can I assist you today?",
        "hello": "Hi there! How can I help you?",
        "hey": "Hey! What can I do for you?",
        "how are you": "I'm just a bot, but I'm here to help! How can I assist you?",
        "good morning": "Good morning! How can I assist you today?",
        "good evening": "Good evening! How can I help you?",
        "what's up": "Not much, just here to assist you! What can I do for you?"
    }
    user_question_lower = user_question.lower()
    for keyword in general_responses:
        if keyword in user_question_lower:
            return general_responses[keyword]
    return "I'm here to help! How can I assist you?"

if __name__ == "__main__":
    main()
