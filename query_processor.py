from main import get_pdf_text, get_text_chunks, get_vector_store, user_input

def process_query(file_paths, query_text):
    text = get_pdf_text(file_paths)
    text_chunks = get_text_chunks(text)
    vector_store = get_vector_store(text_chunks)
    response = user_input(query_text)
    return response
