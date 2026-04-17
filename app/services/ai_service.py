import os
import logging
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    logger = logging.getLogger(__name__)
    logger.info(f"GEMINI_API_KEY is set. Starts with: {api_key[:10]}...")
    genai.configure(api_key=api_key)
else:
    logger = logging.getLogger(__name__)
    logger.warning("GEMINI_API_KEY environment variable not set. API calls will fail.")

# Advanced Improvements: Temperature Control
model = genai.GenerativeModel(
    "gemini-flash-latest",
    generation_config={"temperature": 0.3}
)


async def analyze_with_ai(sector: str, data: list[str]) -> str:
    try:
        # Advanced Improvements: Context Filtering
        filtered_data = [d for d in data if len(d) > 20]
        
        # Limit data size
        trimmed_data = filtered_data[:10]

        # Create context text
        context = "\n".join(trimmed_data)

        # Strong Prompt Engineering
        prompt = f"""
You are a financial market analyst specializing in Indian sectors.

Analyze the {sector} sector using the following recent data:

{context}

Provide a structured analysis with the following sections:

1. Market Trends
2. Key Opportunities
3. Risks and Challenges
4. Top Companies Involved
5. Future Outlook (next 1–3 years)

Keep it concise, factual, and insightful.
Use bullet points under each section.
Do NOT use markdown formatting.
"""

        logging.info(f"Sending prompt to Gemini for sector: {sector}")

        response = model.generate_content(prompt)

        if not response or not response.text:
            return "Analysis temporarily unavailable. Please try again later."

        logging.info("AI response received successfully")

        return response.text.strip()

    except Exception as e:
        logging.error(f"AI Analysis Error: {str(e)}")
        return "Analysis temporarily unavailable. Please try again later."
