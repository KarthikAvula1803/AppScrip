# 📈 Trade Opportunities AI Market Analysis API

A production-ready, AI-driven market analysis service designed to identify trade opportunities in Indian sectors. This project combines real-time data scraping with **Google Gemini AI** to generate structured, actionable reports in both **Markdown** and **PDF** formats.

---

## 🚀 Overview
This application automates the process of market research. It fetches real-time news and trends for any given Indian sector (e.g., Pharma, Tech, EV, Banking) and uses advanced LLMs to synthesize this information into a professional analysis, complete with sentiment analysis and confidence scoring.

## ✨ Key Features
- **🌍 Real-time Intelligence**: Fetches live data from DuckDuckGo and Google News RSS.
- **🧠 AI Analysis**: Powered by **Google Gemini (gemini-1.5-flash)** for thematic insights.
- **📊 Market Metrics**: Automated sentiment detection and trending keyword extraction.
- **📄 Dual Export**: Download professional reports in both **Markdown (.md)** and **PDF** formats.
- **🔒 Security First**: Built-in API Key authentication and Rate Limiting per session.
- **⚡ Performance**: In-memory caching for ultra-fast response times on repeated queries.
- **🎨 Interactive Dashboard**: Built with Streamlit for a premium user experience.

---

## 🏗️ System Architecture
The service follows a modular, clean architecture:
1.  **API Layer (FastAPI)**: Handles requests, validation, and security middleware.
2.  **Service Layer**: 
    - `data_collector`: Scrapes real-time search data.
    - `ai_service`: Communicates with Google Gemini.
    - `formatter`: Converts data into structured Markdown.
3.  **Utility Layer**: Handles PDF generation (`fpdf2`), caching, and business logic.

---

## 🛠️ Setup Instructions

### 1. Clone the Project
```bash
git clone https://github.com/Avulakarthik18/appScrip.git
cd market-analysis-api
```

### 2. Set Up Environment
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_google_ai_key
API_KEY=mysecureapikey123
```

### 3. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the Application
You need to run both the Backend and the Frontend:

**Start Backend (FastAPI):**
```bash
uvicorn app.main:app --reload
```

**Start Frontend (Streamlit):**
```bash
streamlit run streamlit_app.py
```

---

## 🔗 API Documentation
Once the backend is running, you can access the interactive documentation at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Sample Endpoint:
`GET /api/v1/analyze/{sector}`
**Headers**: `x-api-key: your_key`

---

## 📂 Folder Structure
```text
market-analysis-api/
├── app/
│   ├── api/routes/      # API endpoints (analyze.py)
│   ├── models/          # Pydantic validation schemas
│   ├── services/        # Logic: AI, Scrapers, Formatters
│   ├── security/        # Auth & Rate limiting middleware
│   └── utils/           # PDF Generator, Caching, Helpers
├── streamlit_app.py     # Frontend Dashboard
├── requirements.txt     # Dependency list
└── .env                 # Environment variables (private)
```

---

## 👨‍💻 Author
**Avulakarthik18**  
Submitted as part of the Developer Task for the Trade Opportunities API.
