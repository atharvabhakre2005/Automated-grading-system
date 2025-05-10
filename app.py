import streamlit as st
import os
from utils.ocr import OCR_Gemini_Model
from utils.grader import GradeWithKeywords, GradewithNoKeywords, GradeUsingLLM
from utils.helper import check_file_extension
from datetime import datetime
import uuid

UPLOAD_DIR = "student_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.title("👨‍🏫 Teacher Dashboard: Evaluate Student Answer Sheets")

# Upload form
with st.expander("📤 Upload New Student Answer Sheet"):
    with st.form("upload_form"):
        student_name = st.text_input("Student Name")
        uploaded_file = st.file_uploader("Upload Answer Sheet (PDF/Image)", type=["pdf", "png", "jpg", "jpeg"])
        submitted = st.form_submit_button("Upload")

        if submitted and uploaded_file and student_name:
            # Save uploaded file
            filename = f"{student_name}_{uuid.uuid4().hex[:6]}_{uploaded_file.name}"
            file_path = os.path.join(UPLOAD_DIR, filename)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            st.success(f"✅ Uploaded successfully for {student_name}!")

# Load all uploaded files
files = os.listdir(UPLOAD_DIR)
student_files = [f for f in files if not f.startswith(".")]

if not student_files:
    st.info("No student uploads yet.")
else:
    selected_file = st.selectbox("📚 Select a student sheet to evaluate:", student_files)

    if selected_file:
        student_name = selected_file.split("_")[0]
        file_path = os.path.join(UPLOAD_DIR, selected_file)
        st.write(f"**🧑 Student:** {student_name}")
        st.write(f"**📄 File:** {selected_file}")

        model_answer = st.text_area("✏️ Model Answer (Required)", height=150)
        keywords = st.text_input("🔑 Keywords (Optional, comma-separated)")
        edit_ocr = st.checkbox("Apply OCR Spell Correction", value=False)

        if model_answer:
            if st.button("🚀 Evaluate"):
                with st.spinner("🔍 Extracting Answer from Image/PDF..."):
                    extracted_answer = OCR_Gemini_Model(file_path, edit=edit_ocr)

                st.subheader("📄 Extracted Answer:")
                st.write(extracted_answer)

                use_llm = st.checkbox("Use LLM for Advanced Grading (Gemini-Pro)", value=True)

                # Grading
                if use_llm:
                    score = GradeUsingLLM(extracted_answer, model_answer)
                elif keywords:
                    score = GradeWithKeywords(extracted_answer, model_answer, keywords)
                else:
                    score = GradewithNoKeywords(extracted_answer, model_answer)

                st.success(f"✅ Final Score for {student_name}: {score:.2f} / 10")
        else:
            st.warning("⚠️ Please enter a model answer to evaluate.")
