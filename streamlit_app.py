import streamlit as st
import requests
import os
from dotenv import load_dotenv
from app.utils.pdf_generator import generate_pdf

# Load environment variables
load_dotenv()

# Configuration
BACKEND_BASE = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
# Ensure the URL points to the v1 API
if "/api/v1" not in BACKEND_BASE:
    API_URL = f"{BACKEND_BASE.rstrip('/')}/api/v1"
else:
    API_URL = BACKEND_BASE
    
API_KEY = os.getenv("API_KEY", "mysecureapikey123")

# Page Config
st.set_page_config(
    page_title="AI Market Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Title & Sidebar
st.title("📈 AI Market Analysis Dashboard")
st.info("Using real-time AI + Indian market news data")

with st.sidebar:
    st.header("Settings")
    # Robust Health Check
    api_status = "Offline"
    status_color = "red"
    try:
        if requests.get(f"{API_URL}/health", timeout=2).status_code == 200:
            api_status = "Online"
            status_color = "green"
    except Exception:
        pass
    
    st.markdown(f"API Status: <span style='color:{status_color}; font-weight:bold;'>{api_status}</span>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### How it works")
    st.write("1. Enter an Indian market sector.")
    st.write("2. AI fetches live news & trends.")
    st.write("3. Get a professional analysis report.")

# Input Section
sector = st.text_input("🔍 Enter Market Sector (e.g. Pharma, Tech, EV, Banking)", placeholder="technology")

if st.button("Analyze Sector"):
    if not sector:
        st.warning("Please enter a sector name to analyze.")
    else:
        with st.spinner(f"Fetching real-time data and generating analysis for '{sector}'..."):
            try:
                headers = {"x-api-key": API_KEY}
                response = requests.get(f"{API_URL}/analyze/{sector}", headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    report = data.get("report", "No report generated.")
                    is_cached = data.get("cached", False)
                    
                    st.success("Analysis Complete ✅")
                    
                    if is_cached:
                        st.caption("⚡ Serving from cache")
                    
                    # Download Buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="📥 Download Markdown",
                            data=report,
                            file_name=f"{sector}_market_analysis.md",
                            mime="text/markdown",
                        )
                    with col2:
                        pdf_bytes = generate_pdf(report)
                        st.download_button(
                            label="📄 Download PDF",
                            data=pdf_bytes,
                            file_name=f"{sector}_market_analysis.pdf",
                            mime="application/pdf",
                        )
                    
                    # Display the Markdown Report
                    st.markdown("---")
                    st.markdown(report)
                    
                    # Sidebar metrics
                    with st.sidebar:
                        st.divider()
                        st.metric(label="Data Points", value=data.get("data_count", 0))
                        st.write("Confidence Score: **Success**" if data.get("status") == "success" else "Status: Failed")
                
                elif response.status_code == 401:
                    st.error("Authentication Failed: Invalid API Key.")
                elif response.status_code == 400:
                    st.error(f"Validation Error: {response.json().get('detail')}")
                else:
                    st.error(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")
            
            except Exception as e:
                st.error(f"Could not connect to the Backend API. Make sure FastAPI server is running. Error: {e}")

# Footer
st.markdown("---")
st.caption("Market Analysis AI Backend v1.0.0 | Built with FastAPI & Streamlit")
