import requests
import json

from app.logger import log

# =========================================================
# GET POSTS
# =========================================================
def get_instagram_posts(

    user_id,
    rapidapi_key,
    rapidapi_host,
    rapidapi_url

):

    try:

        headers = {

            "x-rapidapi-key":
                rapidapi_key,

            "x-rapidapi-host":
                rapidapi_host
        }

        params = {
            "user_id": user_id
        }

        response = requests.get(
            rapidapi_url,
            headers=headers,
            params=params,
            timeout=30
        )

        log(
            f"[INSTAGRAM] STATUS "
            f"{response.status_code}"
        )

        if response.status_code != 200:

            return []

        # =================================================
        # DEBUG JSON
        # =================================================
        data = response.json()

        print("\n================ JSON =================")
        print(json.dumps(data, indent=2)[:5000])
        print("=======================================\n")

        # =================================================
        # TENTA PEGAR POSTS
        # =================================================
        posts = []

        items = []

        # formato 1
        if "items" in data:
            items = data["items"]

        # formato 2
        elif "data" in data:

            if isinstance(data["data"], dict):

                items = data["data"].get(
                    "items",
                    []
                )

        for item in items[:5]:

            code = item.get("code")

            if not code:
                continue

            posts.append({

                "code": code,

                "link":
                    f"https://www.instagram.com/p/{code}/"
            })

        return posts

    except Exception as e:

        log(f"[INSTAGRAM ERROR] {e}")

        return []