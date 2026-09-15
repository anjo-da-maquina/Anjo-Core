import rsa
import json
import datetime
import base64
import os
import sys
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from maquina_gatekeeper import get_absolute_hardware_fingerprint

def provision_sanctuary():
    print("\n[Provisioning Agent] 新たな鍵対を生成し、この環境を承認します...")
    # 2048bitの強力なRSA鍵対を新規生成
    pubkey, privkey = rsa.newkeys(2048)
    pubkey_pem = pubkey.save_pkcs1().decode('utf-8')

    # 環境の複合指紋を抽出
    fingerprint = get_absolute_hardware_fingerprint()
    # 7日間の寿命（TTL）を設定
    valid_until = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + "Z"

    payload = {
        "client_id": "anjo-local-tester",
        "hardware_fingerprint": fingerprint,
        "valid_until": valid_until
    }

    # 秘密鍵で署名
    payload_str = json.dumps(payload, sort_keys=True)
    signature = rsa.sign(payload_str.encode('utf-8'), privkey, 'SHA-256')
    signature_b64 = base64.b64encode(signature).decode('utf-8')

    cert = {
        "payload": payload,
        "signature": signature_b64
    }

    # 証明書を発行
    with open("ataraxia_certificate.json", "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2)

    # ゲートキーパー(防壁)の中枢に、新たな公開鍵を直接埋め込む(自己改変)
    gatekeeper_path = "maquina_gatekeeper.py"
    with open(gatekeeper_path, "r", encoding="utf-8") as f:
        code = f.read()

    new_code = re.sub(
        r'MAQUINA_PUBLIC_KEY_PEM = """.*?-----END RSA PUBLIC KEY-----"""',
        f'MAQUINA_PUBLIC_KEY_PEM = """{pubkey_pem.strip()}"""',
        code,
        flags=re.DOTALL
    )

    with open(gatekeeper_path, "w", encoding="utf-8") as f:
        f.write(new_code)

    print("[Provisioning Agent] ataraxia_certificate.json を発行しました。")
    print("[Provisioning Agent] 防壁の中枢（公開鍵）を自動同期しました。")
    print(f"[Provisioning Agent] 平穏の有効期限: {valid_until}")

if __name__ == '__main__':
    provision_sanctuary()
