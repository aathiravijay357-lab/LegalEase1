import html
import os
from datetime import date

import requests
import streamlit as st
from dotenv import load_dotenv

from utils.document_generator import format_docx, format_pdf, format_txt

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(
    page_title="LegalEase - AI Legal Document Drafting",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main-title { text-align:center; font-size:42px; font-weight:800; margin-bottom:0; }
    .subtitle { text-align:center; color:#718096; margin-top:4px; margin-bottom:25px; }
    .disclaimer { background:#fff7ed; border:1px solid #fed7aa; padding:14px; border-radius:10px; }
    .preview { background:#111827; color:#f9fafb; padding:24px; border-radius:12px; line-height:1.65; white-space:pre-wrap; max-height:650px; overflow-y:auto; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">⚖️ LegalEase</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-assisted legal document drafting and export</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="disclaimer"><b>Important:</b> LegalEase generates AI-assisted drafts for informational and drafting purposes. It is not a substitute for advice from a qualified lawyer. Review the document for your jurisdiction and circumstances before signing or using it.</div>',
    unsafe_allow_html=True,
)

st.write("")

if "document" not in st.session_state:
    st.session_state.document = ""

with st.sidebar:
    st.header("Document details")
    document_type = st.text_input(
        "Document type",
        value="Non-Disclosure Agreement",
        help="Examples: NDA, Lease Agreement, Employment Contract, Freelance Contract.",
    )
    parties = st.text_area(
        "Parties involved",
        height=130,
        placeholder="Jane Doe (Service Provider)\nTechNova Inc. (Client)",
    )
    terms = st.text_area(
        "Terms & conditions",
        height=180,
        placeholder="Payment within 30 days of invoice;\nConfidentiality must be maintained;\nEither party may terminate with 15 days notice",
        help="Separate individual terms with semicolons or put each term on a new line.",
    )
    effective_date = st.date_input("Effective date", value=date.today())

    generate_clicked = st.button("✨ Generate Document", type="primary", use_container_width=True)

if generate_clicked:
    if not document_type.strip() or not parties.strip() or not terms.strip():
        st.error("Please complete document type, parties, and terms before generating.")
    else:
        payload = {
            "document_type": document_type.strip(),
            "parties": parties.strip(),
            "terms": terms.strip(),
            "effective_date": effective_date.isoformat(),
        }

        with st.spinner("Generating your draft with Gemini..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=120,
                )
                if response.ok:
                    data = response.json()
                    st.session_state.document = data.get("document", "")
                    if not st.session_state.document:
                        st.error("The backend returned an empty document.")
                else:
                    try:
                        detail = response.json().get("detail", response.text)
                    except Exception:
                        detail = response.text
                    st.error(f"Backend error ({response.status_code}): {detail}")
            except requests.RequestException as exc:
                st.error(
                    "Could not connect to the FastAPI backend. Make sure it is running on "
                    f"{BACKEND_URL}. Details: {exc}"
                )

st.subheader("Document preview")

if st.session_state.document:
    st.markdown(
        f'<div class="preview">{html.escape(st.session_state.document)}</div>',
        unsafe_allow_html=True,
    )

    st.divider()
    st.subheader("Edit document")
    edited_document = st.text_area(
        "Make any changes you need",
        value=st.session_state.document,
        height=500,
        key="editor",
    )

    if st.button("💾 Apply edits"):
        st.session_state.document = edited_document
        st.success("Edits applied.")
        st.rerun()

    current_document = st.session_state.document

    st.subheader("Download")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            "⬇️ Download TXT",
            data=format_txt(current_document),
            file_name="LegalEase_Document.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col2:
        try:
            docx_bytes = format_docx(current_document, document_type, terms)
            st.download_button(
                "⬇️ Download DOCX",
                data=docx_bytes,
                file_name="LegalEase_Document.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
        except Exception as exc:
            st.error(f"DOCX generation failed: {exc}")

    with col3:
        try:
            pdf_bytes = format_pdf(current_document, document_type, terms)
            st.download_button(
                "⬇️ Download PDF",
                data=pdf_bytes,
                file_name="LegalEase_Document.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as exc:
            st.error(f"PDF generation failed: {exc}")
else:
    st.info("Fill in the document details on the left and click 'Generate Document'.")

st.divider()
st.caption("LegalEase is an AI-assisted drafting tool. Always obtain appropriate professional legal review before relying on a legal document.")
