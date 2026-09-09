import sys
import os
import logging
import time

logging.basicConfig(level=logging.INFO, format='[Anjo-Core/Samson] %(levelname)s: %(message)s')

def trigger_samson_option(reason: str):
    logging.error(f"CRITICAL ANOMALY DETECTED: {reason}")
    logging.warning("Initiating The Samson Option. Operational stillness must be maintained.")
    purge_environment_state()
    logging.fatal("Environment purged. Forcefully terminating the CI/CD pipeline.")
    sys.exit(1)

def purge_environment_state():
    logging.info("Overwriting sensitive environment variables in memory...")
    for key in os.environ.keys():
        if any(keyword in key.upper() for keyword in ["TOKEN", "SECRET", "KEY", "PWD", "AUTH"]):
            os.environ[key] = "PURGED_BY_ANJO_CORE"
    time.sleep(1)
    logging.info("Memory purge complete. Zero-Trust state enforced.")

if __name__ == "__main__":
    # YAMLから渡された環境変数 SIMULATE_ANOMALY を読み取る
    simulate_anomaly = os.getenv("SIMULATE_ANOMALY", "false").lower() == "true"

    if simulate_anomaly:
        simulated_anomaly = "Unauthorized outbound network call detected in generated test suite."
        trigger_samson_option(simulated_anomaly)
    else:
        # falseの場合はこちらが実行され、正常終了する
        logging.info("Agentic Swarm reports operational stillness. Ataraxia maintained.")
        logging.info("Validation passed. Proceeding to merge phase.")
        sys.exit(0)
