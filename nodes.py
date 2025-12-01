import json

from langchain_core.messages import AIMessage, HumanMessage, RemoveMessage

from schemas.booking import Booking
from schemas.finaltripplan import FinalTripPlan
from schemas.intent import Intent
from prompt import BOOKING_PROMPT, INTENT_EXTRACTION_PROMPT, PLANNING_PROMPT
from schemas.plan import Plan
from state import AICompanionState
from utils.helpers import calculate_total_price, call_payment_gateway, get_chat_model


def intent_extraction_node(state: AICompanionState):
    """
    Extracts structured travel intent from the latest user message.
    """
    user_msg = state["messages"][-1].content
    calendar = state["current_activity"]

    print("extracting intent from user message")
    prompt = INTENT_EXTRACTION_PROMPT.format(
        user_msg=user_msg, calendar=calendar)
    result = get_chat_model().with_structured_output(Intent).invoke(prompt)
    return {
        "intent": result,
        "messages": state["messages"] + [
            AIMessage(content=result.model_dump_json())
        ]
    }


def planning_node(state: AICompanionState):
    """
    Plans a detailed travel itinerary based on the extracted intent and user's calendar.
    """
    intent = state["intent"]
    calendar = state["current_activity"]

    prompt = PLANNING_PROMPT.format(
        intent=intent,
        calendar=calendar,
    )
    print("planning itinerary based on intent and calendar")
    result = get_chat_model().with_structured_output(Plan).invoke(prompt)

    return {
        "itinerary_plan": result,
        "messages": state["messages"] + [
            AIMessage(content=result.model_dump_json())
        ]
    }


def booking_node(state: AICompanionState):
    """
    Simulates booking flights and hotels based on the itinerary and intent.
    """
    intent = state["intent"]
    itinerary = state["itinerary_plan"]
    auto_book = state["auto_book"]

    prompt = BOOKING_PROMPT.format(
        intent=intent,
        itinerary=itinerary,
        auto_book=auto_book,
    )
    print("simulating booking based on intent and itinerary")
    result = get_chat_model().with_structured_output(Booking).invoke(prompt)

    return {
        "booking": result,
        "messages": state["messages"] + [
            AIMessage(content=result.model_dump_json())
        ]
    }


def payment_node(state: AICompanionState):
    """
    Processes payment for the booked itinerary.
    """
    itinerary = state["itinerary_plan"]
    booking = state["booking"]

    amount = calculate_total_price(itinerary, booking)
    print(f"processing payment of amount: {amount} USD")
    payment_method_id = "stripe_mock_method_123"
    payment_response = call_payment_gateway(amount, "USD", payment_method_id)

    if payment_response["status"] != "succeeded":
        return {
            "payment": payment_response,
            "messages": state["messages"] + [
                AIMessage(content="Payment failed: " +
                          payment_response["error"])
            ]
        }
    else:
        return {
            "payment": payment_response,
            "messages": state["messages"] + [
                AIMessage(content="Payment succeeded. Payment Intent ID: " +
                          payment_response["payment_intent_id"])
            ]
        }


def final_response_node(state: AICompanionState):
    """
    Compiles the final trip plan including itinerary, bookings, and payment details.
    """
    intent = state["intent"]
    itinerary = state["itinerary_plan"]
    booking = state["booking"]

    final_plan = FinalTripPlan(
        trip_title=f"Trip to {intent.destination}",
        start_date=itinerary.start_date,
        end_date=itinerary.end_date,
        itinerary=itinerary.days,
        flights=booking.flights,
        hotels=booking.hotels,
        notes=intent.notes,
        payment=state.get("payment", None),
    )

    return {
        "trip_plan": final_plan,
        "messages": state["messages"] + [
            AIMessage(content=final_plan.model_dump_json())
        ]
    }
