import streamlit as st
import pandas as pd
import tempfile
import time

from utils.extractor import extract_text_from_pdf
from utils.claim_detector import extract_claims
from utils.search import search_claim
from utils.verifier import verify_claim

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Fact-Checking Agent",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

.stApp {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: white;
}

.upload-box {
    padding: 20px;
    border-radius: 12px;
    background-color: #161B22;
    border: 1px solid #30363D;
}

.result-card {
    background-color: #161B22;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 20px;
    border: 1px solid #30363D;
}

.verified {
    color: #2ECC71;
    font-weight: bold;
    font-size: 18px;
}

.false {
    color: #E74C3C;
    font-weight: bold;
    font-size: 18px;
}

.inaccurate {
    color: #F39C12;
    font-weight: bold;
    font-size: 18px;
}

.metric-card {
    background-color: #161B22;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #30363D;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #

st.title("🛡️ AI Fact-Checking Agent")

st.markdown("""
Detect misinformation, verify claims using live web data, and generate a truth validation report from uploaded PDFs.
""")

st.divider()

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.header("About")

    st.write("""
    This tool:
    - Extracts factual claims
    - Searches live web evidence
    - Verifies authenticity
    - Flags misinformation
    """)

    st.header("Technologies")

    st.write("""
    - Streamlit
    - Cohere AI
    - Tavily Search
    - PyMuPDF
    """)

# ---------------- FILE UPLOAD ---------------- #

st.markdown('<div class="upload-box">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📄 Upload a PDF document",
    type=["pdf"]
)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- MAIN LOGIC ---------------- #

if uploaded_file:

    st.success("PDF uploaded successfully!")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        pdf_path = tmp_file.name

    # ---------------- EXTRACTION ---------------- #

    with st.spinner("Extracting text from PDF..."):

        time.sleep(1)

        text = extract_text_from_pdf(pdf_path)

    st.success("Text extracted successfully!")

    # ---------------- CLAIM DETECTION ---------------- #

    with st.spinner("Detecting factual claims..."):

        time.sleep(1)

        claims = extract_claims(text)

    st.success(f"Found {len(claims)} potential claims")

    results = []

    verified_count = 0
    false_count = 0
    inaccurate_count = 0

    st.divider()

    st.subheader("🔍 Fact-Checking Results")

    for claim in claims:

        if len(claim.strip()) < 10:
            continue

        with st.spinner(f"Checking claim: {claim[:60]}..."):

            web_results = search_claim(claim)

            verification = verify_claim(claim, web_results)

        # ---------------- STATUS DETECTION ---------------- #

        verification_lower = verification.lower()

        if "verified" in verification_lower:

            status = "Verified"
            status_class = "verified"
            verified_count += 1

        elif "false" in verification_lower:

            status = "False"
            status_class = "false"
            false_count += 1

        else:

            status = "Inaccurate"
            status_class = "inaccurate"
            inaccurate_count += 1

        # ---------------- RESULT CARD ---------------- #

        st.markdown(f"""
        <div class="result-card">

        <p><strong>📌 Claim</strong></p>

        <p>{claim}</p>

        <p class="{status_class}">✅ Status: {status}</p>

        <p><strong>📝 Verification Details</strong></p>

        <p>{verification}</p>

        </div>
        """, unsafe_allow_html=True)

        results.append({
            "Claim": claim,
            "Status": status,
            "Verification": verification
        })

    # ---------------- SUMMARY METRICS ---------------- #

    st.divider()

    st.subheader("📊 Summary Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <h2>{verified_count}</h2>
        <p>✅ Verified</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <h2>{inaccurate_count}</h2>
        <p>⚠️ Inaccurate</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
        <h2>{false_count}</h2>
        <p>❌ False</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- DATAFRAME ---------------- #

    st.divider()

    st.subheader("📄 Detailed Results Table")

    df = pd.DataFrame(results)

    st.dataframe(
        df,
        use_container_width=True
    )

    # ---------------- DOWNLOAD BUTTON ---------------- #

    csv = df.to_csv(index=False)

    st.download_button(
        label="⬇️ Download Report",
        data=csv,
        file_name="fact_check_results.csv",
        mime="text/csv"
    )

# ---------------- FOOTER ---------------- #

st.divider()

st.caption("Built for Product Management Trainee Assessment")