from langgraph.graph import MessagesState


class AICompanionState(MessagesState):
    """State class for the AI workflow.

    Extends MessagesState to track conversation history and maintains the last message received.

    Attributes:
        last_message (AnyMessage): The most recent message in the conversation, can be any valid
            LangChain message type (HumanMessage, AIMessage, etc.)
    """

    current_activity: dict
    auto_book: bool | None = None
    intent: dict | None = None
    itinerary_plan: dict | None = None
    booking: dict | None = None
    trip_plan: dict | None = None

    # payment
    payment: dict | None = None
