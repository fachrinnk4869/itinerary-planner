from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from graph import create_workflow_graph
from langchain_core.messages import HumanMessage
from schemas.common import InternalServerErrorResponse
from schemas.finaltripplan import FinalTripPlan, itineraryQuery
app = FastAPI(title="AssistX API", version="0.1.0")


@app.get("/itinerary", responses={
    "200": {"model": FinalTripPlan},
    "500": {"model": InternalServerErrorResponse},
},)
async def itinerary(query: itineraryQuery = Depends()):
    graph = create_workflow_graph().compile()
    return graph.invoke({
        "messages": [HumanMessage(content=query.input)],
        "current_activity": {
            "2026-01-01": "office meeting"
        },
        "auto_book": query.auto_book
    })["trip_plan"]


@app.get("/")
async def hello():
    return {"Hello": "from assistx!"}
