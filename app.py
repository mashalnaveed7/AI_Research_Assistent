
import streamlit as st
import os

from summarizer import summarize_document
from compare import compare_papers
from citation import generate_citation

from pypdf import PdfReader


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="logo.png",
    layout="wide"
)


# ---------------- API KEY ----------------

api_key = st.secrets["GROQ_API_KEY"]



# ---------------- CUSTOM CSS ----------------

st.markdown("""

<style>

/* Background */

.stApp {

    background-image:
    linear-gradient(
        rgba(255,255,255,0.88),
        rgba(255,255,255,0.88)
    ),
    url("background.png");

    background-size:cover;
    background-position:center;
    background-attachment:fixed;

}


/* Header */

.header-box {

    background:rgba(255,255,255,0.65);
    padding:25px;
    border-radius:20px;
    backdrop-filter:blur(10px);

}


.title {

    font-size:45px;
    font-weight:800;
    color:#0F4C81;

}


.subtitle {

    font-size:20px;
    color:#334155;

}


/* Cards */

.card {

    background:rgba(255,255,255,0.75);
    padding:20px;
    border-radius:18px;
    box-shadow:0px 8px 25px rgba(0,0,0,0.08);

}


/* Sidebar */

section[data-testid="stSidebar"] {

    background:rgba(230,240,255,0.9);

}


/* Buttons */

.stButton button {

    width:100%;
    height:50px;
    border-radius:12px;
    font-size:18px;
    font-weight:bold;

}


</style>

""", unsafe_allow_html=True)



# ---------------- PDF TEXT EXTRACTION ----------------


def extract_text(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text



# ---------------- HEADER ----------------


col1, col2 = st.columns([1,5])


with col1:

    if os.path.exists("logo.png"):

        st.image(
            "logo.png",
            width=100
        )


with col2:

    st.markdown("""

    <div class="header-box">

    <div class="title">
    📚 AI Research Assistant
    </div>

    <div class="subtitle">
    Summarize • Compare • Analyze • Cite Research Papers
    </div>

    </div>

    """,
    unsafe_allow_html=True)



st.divider()



# ---------------- SIDEBAR ----------------


with st.sidebar:


    if os.path.exists("logo.png"):

        st.image(
            "logo.png",
            width=120
        )


    st.header("📄 Upload Papers")


    uploaded_files = st.file_uploader(

        "Upload PDF file(s)",

        type="pdf",

        accept_multiple_files=True

    )



# ---------------- MAIN ----------------


st.subheader("🚀 Choose AI Action")


option = st.radio(

    "Select feature:",

    [

        "Summarize Paper",

        "Compare Papers",

        "Generate Citation"

    ]

)



# ---------------- SUMMARIZE ----------------


if option == "Summarize Paper":


    st.info("Upload one PDF")


    if uploaded_files:


        if st.button("✨ Summarize"):


            with st.spinner("Generating summary..."):


                text = extract_text(
                    uploaded_files[0]
                )


                summary = summarize_document(

                    text,

                    api_key

                )


            st.markdown(summary)



# ---------------- COMPARE ----------------


elif option == "Compare Papers":


    st.info("Upload exactly two PDF files.")


    if uploaded_files:


        if len(uploaded_files) != 2:


            st.warning(
                "Please upload exactly two PDFs."
            )


        else:


            if st.button("🔍 Compare"):


                with st.spinner(
                    "Comparing research papers..."
                ):


                    paper1 = extract_text(
                        uploaded_files[0]
                    )


                    paper2 = extract_text(
                        uploaded_files[1]
                    )


                    comparison = compare_papers(

                        paper1,

                        paper2,

                        api_key

                    )


                st.markdown(comparison)



# ---------------- CITATION ----------------


elif option == "Generate Citation":


    st.info("Upload one PDF.")


    if uploaded_files:


        if len(uploaded_files) != 1:


            st.warning(
                "Please upload only one PDF."
            )


        else:


            if st.button("📚 Generate Citation"):


                with st.spinner(
                    "Generating APA citation..."
                ):


                    text = extract_text(
                        uploaded_files[0]
                    )


                    citation = generate_citation(

                        text,

                        api_key

                    )


                st.markdown(citation)



# ---------------- FOOTER ----------------


st.markdown("""

<br><br>

<div style="text-align:center;color:gray">

Built with heart using Streamlit + Groq AI

</div>

""",
unsafe_allow_html=True)
