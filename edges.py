from state import AICompanionState


def auto_booking_edge(state: AICompanionState):
    """
    Determines the next edge based on the auto_book flag.
    If auto_book is True, proceeds to payment_edge; otherwise, goes to final_response_node
    """
    auto_book = state["auto_book"]
    if not auto_book:
        return "final_response_node"
    return "payment_node"
