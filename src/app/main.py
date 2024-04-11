from fastapi import FastAPI
from starlette.middleware import Middleware
from fastapi_versioning import VersionedFastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.web.address_book.controllers import address_book_controller



origins = [
    "http://localhost:8001",
    "*",
]

middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
   
]

app = FastAPI(title="address-services", middleware=middlewares)



app.include_router(
    address_book_controller.router, 
    prefix="/address", tags=["address"]
)
app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/adress-services/v{major}",
    middleware=middlewares,
)

@app.on_event("startup")
async def startup():
    print("Address Services App started.....")
    


FastAPIInstrumentor.instrument_app(app)
