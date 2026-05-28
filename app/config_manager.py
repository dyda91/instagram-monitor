import json
import os

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
    # RAPIDAPI
    # =====================================================
    "rapidapi_url":
        "https://instagram-api-fast-reliable-public-data-scraper.p.rapidapi.com/feed",

    "rapidapi_host":
        "instagram-api-fast-reliable-public-data-scraper.p.rapidapi.com",

    "rapidapi_key": "",

    # =====================================================
    # TEMPO
    # =====================================================
    "tempo_minutos": 15,

    # =====================================================
    # SMM
    # =====================================================
    "smm_api_url":
        "https://smmoficial.com/api/v2",

    "smm_api_key": "",

    # =====================================================
    # SERVIÇO POSTS
    # =====================================================
    "service_post": "1003",

    "quantity_post": "1000",

    # =====================================================
    # SERVIÇO PERFIL
    # =====================================================
    "service_account": "1034",

    "quantity_account": "300"
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

    # =====================================================
    # CRIA CONFIG SE NÃO EXISTIR
    # =====================================================
    if not os.path.exists(CONFIG_PATH):

        save_config(DEFAULT_CONFIG)

        return DEFAULT_CONFIG

    try:

        with open(
            CONFIG_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        # =================================================
        # GARANTE NOVAS CHAVES
        # =================================================
        for key, value in DEFAULT_CONFIG.items():

            if key not in data:

                data[key] = value

        return data

    except Exception as e:

        print(f"[CONFIG] ERRO AO LER CONFIG: {e}")

        save_config(DEFAULT_CONFIG)

        return DEFAULT_CONFIG

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

    print("[CONFIG] Configuração salva com sucesso")