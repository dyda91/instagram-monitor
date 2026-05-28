import time
from app.config_manager import load_config
from app.monitor import start_monitor


def main():

    print("[WORKER] Monitor iniciado")

    # inicia thread do monitor UMA VEZ
    start_monitor()

    while True:

        try:
            config = load_config()

            tempo_minutos = config.get("tempo_minutos", 15)

            print(f"[WORKER] rodando... (heartbeat a cada {tempo_minutos} min)")

        except Exception as e:
            print("[WORKER ERROR]", e)
            tempo_minutos = 15

        time.sleep(tempo_minutos * 60)


if __name__ == "__main__":
    main()