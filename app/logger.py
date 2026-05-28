# app/logger.py

from datetime import datetime

# =========================================================
# LOGGER SIMPLES
# =========================================================
def log(message):

    now = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    print(f"[{now}] {message}")