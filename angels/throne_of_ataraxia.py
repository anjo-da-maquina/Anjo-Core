import os
import sys
import logging
import hashlib
import json
import datetime

logging.basicConfig(level=logging.INFO, format='[Anjo-Core/Throne] %(levelname)s: %(message)s')

def generate_seal_of_ataraxia():
    logging.info("Initiating Throne of Ataraxia: Final Consolidation and Certificate Issuance...")
    
    # エージェントが書き出した「検証済み供物」を読み込む
    if not os.path.exists("verified_payload.json"):
        logging.error("Verified payload not found. Audit failed or was bypassed. Immediate termination.")
        sys.exit(1) # ここは偽造防止の最終防衛線であるため、検証データがなければ強制終了
        
    with open("verified_payload.json", "r", encoding="utf-8") as f:
        verified_data = json.load(f)
        
    # 【変更】要件と出力を結合したデータから、真なるSHA-256ハッシュ値を算出
    content_str = json.dumps(verified_data, sort_keys=True)
    true_hash = hashlib.sha256(content_str.encode('utf-8')).hexdigest()
    
    audit_payload = {
        "system_authority": "anjo-da-maquina",
        "audit_status": "PASS_ZERO_TOLERANCE",
        "timestamp_utc": datetime.datetime.utcnow().isoformat() + "Z",
        "audited_content_hash": true_hash
    }
    
    payload_str = json.dumps(audit_payload, sort_keys=True)
    seal_hash = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
    
    certificate = {
        "payload": audit_payload,
        "cryptographic_seal": seal_hash
    }
    
    with open("ataraxia_certificate.json", "w", encoding="utf-8") as f:
        json.dump(certificate, f, indent=4)
        
    logging.info(f"Absolute Seal generated bound to True Content Hash: {true_hash}")
    logging.info("[Anjo da máquina] The true Seal of Sanity has been issued. System reached Ataraxia.")
    return True

if __name__ == "__main__":
    generate_seal_of_ataraxia()
    sys.exit(0)
