# app/services/comments_ai.py

import json
import tempfile
import time
import requests

from google import genai


class CommentsAI:

    def __init__(self, config):
        self.config = config

        self.client = genai.Client(
            api_key=config["gemini_api_key"]
        )

    def generate_comments(self, instagram_url):

        # 1 - Obter URL do vídeo
        headers = {
            "x-rapidapi-key": self.config["rapidapi_video_key"],
            "x-rapidapi-host": self.config["rapidapi_video_host"],
            "Content-Type": "application/json"
        }

        response = requests.get(
            self.config["rapidapi_video_url"],
            headers=headers,
            params={
                "url": instagram_url
            }
        )

        data = response.json()

        if "media" not in data:
            raise Exception("Vídeo não encontrado")

        video_url = data["media"][0]["url"]

        # 2 - Baixar vídeo
        video_response = requests.get(
            video_url,
            timeout=120
        )

        with tempfile.NamedTemporaryFile(
            suffix=".mp4",
            delete=False
        ) as f:

            f.write(video_response.content)
            video_path = f.name

        # 3 - Upload Gemini
        video_file = self.client.files.upload(
            file=video_path
        )

        # 4 - Esperar processamento
        while True:

            file_info = self.client.files.get(
                name=video_file.name
            )

            state = str(file_info.state)

            if "ACTIVE" in state:
                break

            if "FAILED" in state:
                raise Exception(
                    "Falha ao processar vídeo"
                )

            time.sleep(5)

        # 5 - Gerar comentários
        result = self.client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                file_info,
                """
                Analise este vídeo.

                Gere 20 comentários para Instagram.

                Regras:
                - Entre 1 e 5 palavras.
                - Pode usar emojis, mas no maximo em metade dos comentários.
                - Comentários positivos, principalmente elogios.
                - Comentários naturais, para uma mulher sensual.
                - Todos diferentes.

                Retorne APENAS JSON.

                Exemplo:

                {
                    "comentario1": "",
                    "comentario2": "",
                    "comentario3": ""
                }
                """
            ]
        )

        # 6 - Converter JSON retornado
        json_text = (
            result.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        comentarios_json = json.loads(
            json_text
        )

        comentarios = "\n".join(
            comentarios_json[k]
            for k in sorted(comentarios_json.keys())
        )

        return comentarios