import os
import time

from dotenv import load_dotenv
from google import genai


load_dotenv()


class GeminiDocumentGenerator:
    """Generate draft legal documents with Google's Gemini API."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. Create a .env file and add your Gemini API key."
            )

        self.client = genai.Client(api_key=self.api_key)

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:

        prompt = f"""
You are the drafting engine for LegalEase, an AI-assisted legal-document drafting application.

Create a professional DRAFT of the requested legal document using the supplied information.

This is drafting assistance, not legal advice.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

USER-PROVIDED TERMS:
{terms}

EFFECTIVE DATE:
{effective_date}

Requirements:
1. Use clear professional legal-document language.
2. Do not invent names, addresses, monetary amounts, dates, obligations, or other material facts.
3. If an important fact is missing, insert [TO BE COMPLETED].
4. Organize the document with a title and numbered sections.
5. Include appropriate sections for the requested document type.
6. Include signature blocks where appropriate.
7. Add a final heading called "DRAFTING NOTE".
8. State that the document should be reviewed by a qualified lawyer before signing or use.
9. Return plain text only.
"""

        last_error = None

        # Try up to 3 times for temporary Gemini service errors.
        for attempt in range(3):
            try:
                print(
                    f"\n[LegalEase] Gemini request "
                    f"attempt {attempt + 1}/3 | model={self.model}"
                )

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

                text = getattr(response, "text", None)

                if not text:
                    raise RuntimeError("Gemini returned an empty response.")

                print("[LegalEase] Gemini generation successful.")
                return text.strip()

            except Exception as exc:
                last_error = exc

                print(
                    f"[LegalEase] Gemini error on attempt "
                    f"{attempt + 1}: {type(exc).__name__}: {exc}"
                )

                # Wait before retrying temporary failures.
                if attempt < 2:
                    wait_time = 3 * (attempt + 1)
                    print(
                        f"[LegalEase] Retrying in {wait_time} seconds..."
                    )
                    time.sleep(wait_time)

        raise RuntimeError(
            f"Gemini generation failed after 3 attempts: "
            f"{type(last_error).__name__}: {last_error}"
        )

