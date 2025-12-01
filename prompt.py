
INTENT_EXTRACTION_PROMPT = """
    Extract structured travel intent from this user message:

    "{user_msg}"

    Consider the user's current calendar activities to avoid conflicts:
    {calendar}

    Return JSON:
    {{
        "destination": "...",
        "start_date": "... or null",
        "end_date": "... or null",
        "budget_range": "... or null",
        "notes": "..."
    }}
    """

PLANNING_PROMPT = """
    Plan a full travel itinerary based on this intent:
    {intent}

    Avoid these busy dates:
    {calendar}

    Produce JSON only:
    {{
        "start_date": "...",
        "end_date": "...",
        "days": [
            {{
                "date": "...",
                "city": "...",
                "activities": [
                    {{
                        "time": "...",
                        "title": "...",
                        "details": "..."
                    }}
                ]
            }}
        ]
    }}
    """

BOOKING_PROMPT = """
    Based on this intent:
    {intent}

    And this itinerary:
    {itinerary}

    Auto-booking enabled: {auto_book}

    Simulate booking flights + hotels.

    Return JSON:
    {{
        "flights": [
                    {{
                        "provider": "...",
                        "booking_reference": "...",
                    }}
                ],
        "hotels": [
                    {{
                        "hotel_name": "...",
                        "booking_reference": "...",
                    }}
                ]
    }}
    """
