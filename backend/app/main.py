from fastapi import FastAPI
from backend.app.core.config import settings
from backend.app.api import flight, hotels, destination , team
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title=settings.PROJECT_NAME)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(flight.router, prefix=f"{settings.API_V1_STR}/flights", tags=["Flights"])
app.include_router(hotels.router, prefix=f"{settings.API_V1_STR}/hotels", tags=["Hotels"])
app.include_router(destination.router, prefix=f"{settings.API_V1_STR}/destinations", tags=["Destinations"])
app.include_router(team.router, prefix=f"{settings.API_V1_STR}/team", tags=["Team"])

@app.get("/")
def root():
    return {"message": "Travel Agent API is running 🚀 "}
