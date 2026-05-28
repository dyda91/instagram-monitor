# app/services/smm.py

import requests

from app.logger import log

# =========================================================
# ENVIO PEDIDO SMM
# =========================================================
def send_smm_order(

    api_url,
    api_key,
    service,
    link,
    quantity

):

    try:

        payload = {
            "key": api_key,
            "action": "add",
            "service": service,
            "link": link,
            "quantity": quantity
        }

        response = requests.post(
            api_url,
            data=payload,
            timeout=30
        )

        log(
            f"[SMM] STATUS "
            f"{response.status_code}"
        )

        try:

            return response.json()

        except Exception:

            return response.text

    except Exception as e:

        log(f"[SMM ERROR] {e}")

        return {
            "error": str(e)
        }