import json
import os

from dotenv import load_dotenv

load_dotenv()

# =========================================================
# PATH DO ARQUIVO
# =========================================================
CONFIG_PATH = "data/config.json"

# =========================================================
# CONFIG PADRÃO
# =========================================================
DEFAULT_CONFIG = {

    # =====================================================
    # INSTAGRAM
    # =====================================================
    "instagram_user": "esteyfe_kerolem",
    "instagram_user_id": "1907093366",

    # =====================================================
    # RAPIDAPI POSTS
    # =====================================================
    "rapidapi_url":
        "https://instagram-api-fast-reliable-public-data-scraper.p.rapidapi.com/feed",

    "rapidapi_host":
        "instagram-api-fast-reliable-public-data-scraper.p.rapidapi.com",

    # =====================================================
    # RAPIDAPI VIDEO
    # =====================================================
    "rapidapi_video_url":
        "https://instagram-downloader-download-instagram-stories-videos4.p.rapidapi.com/convert",

    "rapidapi_video_host":
        "instagram-downloader-download-instagram-stories-videos4.p.rapidapi.com",

    # =====================================================
    # TEMPO
    # =====================================================
    "tempo_minutos": 15,

    # =====================================================
    # SMM
    # =====================================================
    "smm_api_url":
        "https://morethanpanel.com/api/v2",

    # =====================================================
    # SERVIÇO POST PRINCIPAL
    # =====================================================
    "service_post": "2847",
    "quantity_post": "1000",

    # =====================================================
    # SERVIÇO POST 2
    # =====================================================
    "enable_service_post_2": True,
    "service_post_2": "5707",
    "quantity_post_2": "1000",

    # =====================================================
    # SERVIÇO COMENTÁRIOS IA
    # =====================================================
    "enable_service_post_3": True,
    "service_post_3": "4641",
    "quantity_post_3": "20",

    # =====================================================
    # SERVIÇO POST 4
    # =====================================================
    "enable_service_post_4": False,
    "service_post_4": "",
    "quantity_post_4": "1000",

    # =====================================================
    # PERFIL
    # =====================================================
    "service_account": "",
    "quantity_account": "100"
}


# =========================================================
# GARANTE PASTA DATA
# =========================================================
def ensure_data_dir():
    os.makedirs(
        "data",
        exist_ok=True
    )


# =========================================================
# LOAD CONFIG
# =========================================================
def load_config():

    ensure_data_dir()

    if not os.path.exists(CONFIG_PATH):

        save_config(DEFAULT_CONFIG)

        config = DEFAULT_CONFIG.copy()

    else:

        try:

            with open(
                CONFIG_PATH,
                "r",
                encoding="utf-8"
            ) as f:

                config = json.load(f)

            for key, value in DEFAULT_CONFIG.items():

                if key not in config:
                    config[key] = value

        except Exception as e:

            print(
                f"[CONFIG] ERRO AO LER CONFIG: {e}"
            )

            save_config(DEFAULT_CONFIG)

            config = DEFAULT_CONFIG.copy()

    # =====================================================
    # VARIÁVEIS DO .ENV
    # =====================================================
    config["rapidapi_key"] = os.getenv(
        "RAPIDAPI_KEY",
        ""
    )

    config["rapidapi_video_key"] = os.getenv(
        "RAPIDAPI_VIDEO_KEY",
        ""
    )

    config["smm_api_key"] = os.getenv(
        "SMM_API_KEY",
        ""
    )

    config["gemini_api_key"] = os.getenv(
        "GEMINI_API_KEY",
        ""
    )

    return config


# =========================================================
# SAVE CONFIG
# =========================================================
def save_config(config):

    ensure_data_dir()

    with open(
        CONFIG_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            config,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(
        "[CONFIG] Configuração salva com sucesso"
    )