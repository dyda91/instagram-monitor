# app/monitor.py

import threading
import time

from app.config_manager import load_config
from app.services.instagram import get_instagram_posts
from app.services.smm import (
    send_smm_order,
    send_custom_comments
)
from app.services.comments_ai import CommentsAI
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
# IA COMMENTS
# =========================================================
comments_ai = None

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
    global comments_ai

    while True:
        try:
            config = load_config()

            # Inicializa IA apenas uma vez
            if comments_ai is None:
                comments_ai = CommentsAI(config)

            log("================================================")
            log("MONITOR INICIADO")
            log("================================================")

            posts = get_instagram_posts(
                user_id=config["instagram_user_id"],
                rapidapi_key=config["rapidapi_key"],
                rapidapi_host=config["rapidapi_host"],
                rapidapi_url=config["rapidapi_url"]
            )
            log(f"[INSTAGRAM] Retornou {len(posts)} posts")

            for post in posts:
                log(f"[POST] {post}")

            processed_posts = []
            found_new_post = False

            # =================================================
            # LOOP DE PROCESSAMENTO DOS POSTS
            # =================================================
            for post in posts:

                code = post["code"]
                is_new = code not in cache_codes
                smm_sent = False

                # =============================================
                # NOVO POST DETECTADO
                # =============================================
                if is_new:

                    found_new_post = True

                    log(f"[NOVO POST] {code}")
                    log(f"[LINK] {post['link']}")

                    # =========================================
                    # SERVIÇO PRINCIPAL
                    # =========================================
                    response = send_smm_order(
                        api_url=config["smm_api_url"],
                        api_key=config["smm_api_key"],
                        service=config["service_post"],
                        link=post["link"],
                        quantity=config["quantity_post"]
                    )

                    log(f"[SMM POST] {response}")

                    # =========================================
                    # SERVIÇO EXTRA 1
                    # =========================================
                    if config.get("enable_service_post_2"):

                        response = send_smm_order(
                            api_url=config["smm_api_url"],
                            api_key=config["smm_api_key"],
                            service=config["service_post_2"],
                            link=post["link"],
                            quantity=config["quantity_post_2"]
                        )

                        log(f"[SMM POST 2] {response}")

                    # =========================================
                    # SERVIÇO EXTRA 2 - COMENTÁRIOS IA
                    # =========================================
                    if config.get("enable_service_post_3"):

                        try:

                            log(
                                "[IA] Iniciando geração de comentários"
                            )

                            comentarios = (
                                comments_ai.generate_comments(
                                    post["link"]
                                )
                            )

                            log(
                                "[IA] Comentários gerados com sucesso"
                            )

                            response = send_custom_comments(
                                api_url=config["smm_api_url"],
                                api_key=config["smm_api_key"],
                                service=config["service_post_3"],
                                link=post["link"],
                                comments=comentarios
                            )

                            log(
                                f"[SMM COMMENTS] {response}"
                            )

                        except Exception as e:

                            log(
                                f"[ERRO IA COMMENTS] {e}"
                            )
                    # SERVIÇO EXTRA 3 (POST 4)
                if config.get("enable_service_post_4"):
                    response = send_smm_order(
                        api_url=config["smm_api_url"],
                        api_key=config["smm_api_key"],
                        service=config["service_post_4"],
                        link=post["link"],
                        quantity=config["quantity_post_4"]
                    )
                    log(f"[SMM POST 4] {response}")
                    
                    smm_sent = True

                processed_posts.append({
                    "code": code,
                    "link": post["link"],
                    "is_new": is_new,
                    "smm_sent": smm_sent
                })

            # =================================================
            # SERVIÇO DE PERFIL
            # =================================================
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
            config.get(
                "tempo_minutos",
                15
            )
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