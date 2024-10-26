# from transformers import pipeline

# # Hugging Face GPT-like model for text generation
# generator = pipeline('text-generation', model='gpt-2')

# # Function to generate a response
# def generate_answer(query):
#     # search_results = search_milvus(query)
    
#     # # Get relevant document chunks based on search results
#     # documents = [result.entity for result in search_results]
#     context = "rigger new thoughts, to perceive and learn’. Artificial a property of machines or programs: the intelligence that the intelligence can be defined that area of computer science that system demonstrates. Artificial intelligence is combination of mainly focus on the making on such kind of intelligent science and engineering for making the machines which machines that work and give reactions same like human behaves in intelligent manner. In it many fields are combined"

#     # Concatenate relevant chunks and query, and generate a response
#     context = ' '.join(documents)
#     prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
#     response = generator(prompt, max_length=150)
    
#     return response[0]['generated_text']

# # Example query
# query = "Explain the recent findings in intelilgence"
# answer = generate_answer(query)
# print(answer)

import google.generativeai as genai

genai.configure(api_key="AIzaSyAwIEpg7iGKz-LoYdRBnoF1hycvT5Ks77U")

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Write a story about a magic backpack.")
print(response.text)    