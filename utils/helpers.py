import uuid
import random
import re

from langchain_core.output_parsers import StrOutputParser

from langchain_google_genai import ChatGoogleGenerativeAI
from settings import GOOGLE_API_KEY


def get_chat_model(temperature: float = 0.7):
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GOOGLE_API_KEY,
    )


def format_schedule_dict(activity_dict: dict):
    lines = [f"{date}: {event}" for date, event in activity_dict.items()]
    return "\n".join(lines)


def remove_asterisk_content(text: str) -> str:
    """Remove content between asterisks from the text."""
    return re.sub(r"\*.*?\*", "", text).strip()


def calculate_total_price(itinerary, booking):
    # Dummy implementation for total price calculation
    return 1000  # Replace with actual logic


def call_payment_gateway(amount, currency, payment_method_id):
    # Simulate gateway call
    # In real-case: use requests.post("https://api.stripe.com/v1/payment_intents", ...)

    success = random.random() > 0.1  # 90% success simulate

    if success:
        return {
            "status": "succeeded",
            "payment_intent_id": "pi_" + uuid.uuid4().hex[:12],
            "provider": "mock_stripe"
        }
    else:
        return {
            "status": "failed",
            "error": "card_declined",
            "provider": "mock_stripe"
        }


class AsteriskRemovalParser(StrOutputParser):
    def parse(self, text):
        return remove_asterisk_content(super().parse(text))
