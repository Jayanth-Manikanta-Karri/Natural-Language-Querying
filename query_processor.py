import PyPDF2
import google.generativeai as genai

genai.configure(api_key="AIzaSyAaYnXPBxf5bWjIJ2V4E4sqYcM5XEj6wA0")
model = genai.GenerativeModel(model_name='gemini-pro')

def process_query(file_path, query):

    with open(file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(reader.pages)

        text = ''
        for page_num in range(num_pages):
            text += reader.pages[page_num].extract_text()

    # Process the query
    prompt = f"Query: {query}\nText: {text}\n"
    response = model.generate_content(prompt)

    generated_text = response.text

    return generated_text