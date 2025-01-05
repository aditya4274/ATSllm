import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template
input_prompt="""

Task:
You are an experienced ATS (Applicant Tracking System) with a deep understanding of the technology job market. The goal is to evaluate a given resume against a specific job description (JD) and provide actionable feedback. Please ensure that the evaluation is accurate and detailed, as the market is highly competitive and requires an excellent resume to align with the JD.

Instructions:
Using the provided resume and job description as context, follow these steps:

Matching Percentage: Calculate the percentage match between the resume and the job description. This percentage should reflect how closely the resume aligns with the required skills, qualifications, and experience mentioned in the JD.

Missing Skills: Identify the key skills or qualifications mentioned in the JD that are missing or underrepresented in the resume. Focus only on the relevant skills and avoid adding extra keywords or qualifications that do not align with the specific role.

Profile Summary: Provide a brief summary of how well the candidate’s profile fits the job based on the resume. Mention strengths and areas for improvement, focusing on how the candidate can better match the JD.

Recommendations for Improvement: Suggest concrete ways the resume can be improved to increase the match with the JD. This could include rephrasing existing content, adding missing qualifications, or emphasizing certain skills that are currently understated in the resume.

Output Structure:

Matching Percentage:
Provide a percentage that reflects how well the resume matches the JD.

Missing Skills/Qualifications:
List the skills or qualifications required by the JD but missing from the resume.

Profile Summary for the JD:
Write a short summary that explains the strengths of the profile in relation to the JD and areas where it falls short.

Recommendations for Improvement:
Offer concrete suggestions on how the candidate can improve the resume to better align with the JD.

Context:
Resume: {text}
Job Description: {jd}
"""

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
job_desc=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        resume_text=input_pdf_text(uploaded_file)
        prompt = input_prompt.format(text=resume_text, jd=job_desc) 
        response=get_gemini_repsonse(prompt)
        st.subheader(response)