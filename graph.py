import asyncio
from functools import lru_cache

from edges import auto_booking_edge
from langgraph.graph import END, START, StateGraph
from langchain_core.messages import AIMessage, HumanMessage, RemoveMessage

from nodes import (
    booking_node,
    final_response_node,
    intent_extraction_node,
    payment_node,
    planning_node,
)
from state import AICompanionState


@lru_cache(maxsize=1)
def create_workflow_graph():
    graph = StateGraph(AICompanionState)

    graph.add_node("intent_extraction_node", intent_extraction_node)
    graph.add_node("planning_node", planning_node)
    graph.add_node("booking_node", booking_node)
    graph.add_node("payment_node", payment_node)
    graph.add_node("final_response_node", final_response_node)

    graph.add_edge(START, "intent_extraction_node")
    graph.add_edge("intent_extraction_node", "planning_node")
    graph.add_edge("planning_node", "booking_node")
    graph.add_edge("booking_node", "final_response_node")
    graph.add_conditional_edges(
        "booking_node", auto_booking_edge)
    graph.add_edge("payment_node", "final_response_node")
    graph.add_edge("final_response_node", END)

    return graph


if __name__ == "__main__":
    """
    Test the workflow graph independently.
    """
    graph = create_workflow_graph().compile()

    result = graph.invoke({
        "messages": [HumanMessage(content="Plan a romantic 4-day trip to Bali next month. Booking OK.")],
        "current_activity": {
            "2026-01-01": "office meeting"
        },
        "auto_book": True
    })

    print(result["trip_plan"])
