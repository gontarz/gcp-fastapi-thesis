import logging

import google.cloud.logging
from fastapi import FastAPI
from google.cloud.logging_v2.handlers import CloudLoggingHandler, setup_logging

from api.routes import router
from fastapi import Request, Response
import traceback
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router)

# client = google.cloud.logging.Client()
# handler = CloudLoggingHandler(client)
# setup_logging(handler)
logger = logging.getLogger(__name__)


# CORS
# origins = [
#     "http://localhost",
#     "http://localhost:8000", # TODO
#     "http://127.0.0.1:8000"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    logger.exception(exc, stack_info=True, exc_info=True)
    return Response(content="".join(traceback.format_exception(exc)), status_code=500)
