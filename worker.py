# worker.py

import time
from app.config_manager import load_config
from app.monitor import run_monitor

def main():

    print("[WORKER] Monitor iniciado")

    while True:

        try:
            config = load_config()

            tempo_minutos = config.get("tempo_minutos", 15)

            print(f"[WORKER] Executando monitor... (a cada {tempo_minutos} min)")

            run_monitor()

        except Exception as e:
            print("[WORKER ERROR]", e)

        time.sleep(tempo_minutos * 60)


if __name__ == "__main__":
    main()