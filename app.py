import streamlit as st
from utils.ocr import OCR_Gemini_Model
from utils.grader import GradeWithKeywords, GradewithNoKeywords
from utils.helper import check_file_extension

st.title("📝 Handwritten Answer Evaluator")
st.write("Upload a student's handwritten answer sheet and evaluate it based on the model answer and keywords.")

uploaded_file = st.file_uploader("Upload Image or PDF", type=["pdf", "png", "jpg", "jpeg"])

model_answer = st.text_area("✏️ Model Answer (Required)", height=150)
keywords = st.text_input("🔑 Keywords (Optional, comma-separated)")
edit_ocr = st.checkbox("Apply OCR Spell Correction", value=False)
keywords = st.text_area("Feedback")

if uploaded_file and model_answer:
    with st.spinner("🔍 Extracting Answer from Image/PDF..."):
        extracted_answer = OCR_Gemini_Model(uploaded_file, edit=edit_ocr)

    st.subheader("📄 Extracted Answer:")
    st.write(extracted_answer)  

    # Scoring
    use_llm = st.checkbox("Use LLM for Advanced Grading (Gemini-Pro)", value=True)

    if use_llm:
        from utils.grader import GradeUsingLLM
        score = GradeUsingLLM(extracted_answer, model_answer)
    elif keywords:
        score = GradeWithKeywords(extracted_answer, model_answer, keywords)
    else:
        score = GradewithNoKeywords(extracted_answer, model_answer)


    st.success(f"✅ Final Score: {score:.2f} / 10")

elif uploaded_file and not model_answer:
    st.warning("⚠️ Please enter a model answer to continue.")
    