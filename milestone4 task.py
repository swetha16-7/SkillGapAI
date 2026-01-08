# 1.Create a basic Streamlit app with title & description
import streamlit as st
st.title("Skill Gap Analysis Dashboard")
st.write("This app analyzes skill match between Resume and Job Description.")

# 2.Add a Streamlit sidebar with navigation text
st.sidebar.title("Navigation")
st.sidebar.write("📄 Upload Files")
st.sidebar.write("📊 Skill Analysis")
st.sidebar.write("📥 Export Report")

# 3.File uploader (PDF, DOCX, TXT only)
resume_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"]
)

jd_file = st.file_uploader(
    "Upload Job Description",
    type=["pdf", "docx", "txt"]
)




# 4.Display uploaded file name


if resume_file:
    st.success(f"Uploaded Resume: {resume_file.name}")

if jd_file:
    st.success(f"Uploaded JD: {jd_file.name}")




# 5.Show first 300 characters of uploaded text


from io import StringIO
import PyPDF2
import docx

def read_file(file):
    if file.name.endswith(".txt"):
        return StringIO(file.getvalue().decode("utf-8")).read()
    elif file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return "".join([p.extract_text() for p in reader.pages])
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    return ""

if resume_file:
    resume_text = read_file(resume_file)
    st.text(resume_text[:300])




# 6. Button to trigger processing


process_btn = st.button("Analyze Skills")




# 7.Resume & JD previews in separate sections


col1, col2 = st.columns(2)

with col1:
    st.subheader("Resume Preview")
    st.text(resume_text[:300])

with col2:
    st.subheader("Job Description Preview")
    st.text(jd_text[:300])




# 8.Skill match percentage using metric


match_percentage = 65.5
st.metric("Skill Match Percentage", f"{match_percentage}%")




# 9. Matched & missing skills lists


matched_skills = ["", "sql", "ml"]
missing_skills = ["nlp", "streamlit"]

st.subheader("Matched Skills")
st.write(matched_skills)

st.subheader("Missing Skills")
st.write(missing_skills)




# 10.Bar chart: matched vs missing skills


import pandas as pd
import matplotlib.pyplot as plt

data = pd.DataFrame({
    "Category": ["Matched", "Missing"],
    "Count": [len(matched_skills), len(missing_skills)]
})

fig, ax = plt.subplots()
ax.bar(data["Category"], data["Count"])
st.pyplot(fig)




# 11.Table of skills & similarity scores


df = pd.DataFrame({
    "Skill": ["", "sql", "ml", "nlp"],
    "Similarity Score": [1.0, 1.0, 1.0, 0.0]
})

st.dataframe(df)




# 12.Session state to preserve data


if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

st.session_state.resume_text = resume_text




# 13.Error handling


if resume_file is None or jd_file is None:
    st.error("Please upload both files.")

if resume_text.strip() == "":
    st.error("Resume file is empty.")




# 14.Download button (CSV export)


csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Skill Gap Report",
    data=csv,
    file_name="skill_gap_report.csv",
    mime="text/csv"
)
