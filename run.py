# run.py

import os
import uvicorn

from dotenv import load_dotenv

# =========================================================
# LOAD ENV
# =========================================================
load_dotenv()

# =========================================================
# CONFIG
# =========================================================
HOST = os.getenv(
    "HOST",
    "0.0.0.0"
)

PORT = int(
    os.getenv(
        "PORT",
        8000
    )
)

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development"
)

DEBUG = ENVIRONMENT == "development"

# =========================================================
# START
# =========================================================
if __name__ == "__main__":

    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG
    )