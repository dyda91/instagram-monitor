# app/monitor.py

import threading
import time

from app.config_manager import load_config
from app.services.instagram import get_instagram_posts
from app.services.smm import send_smm_order
from app.logger import log

# =========================================================
# ESTADO GLOBAL
# =========================================================
monitor_data = {
    "posts": [],
    "last_check": None
}

# =========================================================
# CACHE POSTS
# =========================================================
cache_codes = []

# =========================================================
# GET DATA
# =========================================================
def get_monitor_data():

    config = load_config()

    return {
        "posts": monitor_data["posts"],
        "last_check": monitor_data["last_check"],
        "config": config
    }

# =========================================================
# LOOP PRINCIPAL
# =========================================================
def monitor_loop():

    global cache_codes

    while True:

        try:

            config = load_config()

            log("================================================")
            log("MONITOR INICIADO")
            log("================================================")

            posts = get_instagram_posts(
                user_id=config["instagram_user_id"],
                rapidapi_key=config["rapidapi_key"],
                rapidapi_host=config["rapidapi_host"],
                rapidapi_url=config["rapidapi_url"]
            )

            processed_posts = []

            found_new_post = False

            for post in posts:

                code = post["code"]

                is_new = code not in cache_codes

                smm_sent = False

                # =============================================
                # NOVO POST
                # =============================================
                if is_new:

                    found_new_post = True

                    log(f"[NOVO POST] {code}")

                    # =========================================
                    # ENVIO SMM POST
                    # =========================================
                    response = send_smm_order(
                        api_url=config["smm_api_url"],
                        api_key=config["smm_api_key"],
                        service=config["service_post"],
                        link=post["link"],
                        quantity=config["quantity_post"]
                    )

                    log(f"[SMM POST] {response}")

                    smm_sent = True

                processed_posts.append({
                    "code": code,
                    "link": post["link"],
                    "is_new": is_new,
                    "smm_sent": smm_sent
                })

            # =============================================
            # ENVIO PERFIL
            # =============================================
            if found_new_post:

                profile_link = (
                    f"https://www.instagram.com/"
                    f"{config['instagram_user']}/"
                )

                response = send_smm_order(
                    api_url=config["smm_api_url"],
                    api_key=config["smm_api_key"],
                    service=config["service_account"],
                    link=profile_link,
                    quantity=config["quantity_account"]
                )

                log(f"[SMM PERFIL] {response}")

            # =============================================
            # UPDATE CACHE
            # =============================================
            cache_codes = [
                p["code"]
                for p in processed_posts
            ]

            monitor_data["posts"] = processed_posts

            monitor_data["last_check"] = time.strftime(
                "%d/%m/%Y %H:%M:%S"
            )

            log(
                f"[MONITOR] "
                f"{len(processed_posts)} posts processados"
            )

        except Exception as e:

            log(f"[ERRO MONITOR] {e}")

        # =================================================
        # AGUARDA
        # =================================================
        config = load_config()

        minutes = int(
            config.get("tempo_minutos", 15)
        )

        sleep_time = minutes * 60

        log(f"[SLEEP] {minutes} minutos")

        time.sleep(sleep_time)

# =========================================================
# START THREAD
# =========================================================
def start_monitor():

    thread = threading.Thread(
        target=monitor_loop,
        daemon=True
    )

    thread.start()

    log("[THREAD] Monitor iniciado")