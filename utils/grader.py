import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the pre-trained SentenceTransformer model
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

# Function to calculate similarity using SBERT
def calculate_similarity(student_answer, model_answer):
    student_embedding = sbert_model.encode(student_answer)
    model_embedding = sbert_model.encode(model_answer)
    return cosine_similarity([student_embedding], [model_embedding])[0][0]

# Function to calculate keyword matching score
def calculate_keyword_score(student_answer, keywords):
    keyword_list = [k.strip().lower() for k in keywords.split(',')]
    student_answer = student_answer.lower()
    matched = sum(k in student_answer for k in keyword_list)
    return (matched / len(keyword_list)) if keyword_list else 0

# Grade using keywords and semantic similarity
def GradeWithKeywords(student_answer, model_answer, keywords):
    sim_score = calculate_similarity(student_answer, model_answer)
    key_score = calculate_keyword_score(student_answer, keywords)
    return sim_score * 8 + key_score * 2

# Grade using only semantic similarity (no keywords)
def GradewithNoKeywords(student_answer, model_answer):
    return calculate_similarity(student_answer, model_answer) * 10

# Grade using LLM-based evaluation (Gemini or other models)
def GradeUsingLLM(student_answer, model_answer, max_marks=10):
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    prompt = f"""
You are an evaluator for student answer sheets.

Evaluate the following student answer based on the model answer.
Give marks out of {max_marks}. Just return the number (e.g., 6.5) with no explanation.

Model Answer:
{model_answer}

Student Answer:
{student_answer}

Marks:
"""
    try:
        response = model.generate_content(prompt)
        return float(response.text.strip().split()[0])
    except Exception as e:
        return 0  # fallback score
