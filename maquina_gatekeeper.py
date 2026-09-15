import json
import os
import urllib.request
import urllib.error
import rsa
import base64
import uuid
import hashlib
import socket
import platform
import subprocess
import sys
from functools import wraps
from datetime import datetime

class LossOfAtaraxia(Exception):
    pass

MAQUINA_PUBLIC_KEY_PEM = """-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAi5IOaNSwJi6gkIsNm6yAtuYRuuC4+zjs+MNf721/MKf+WlP5Kz5g
jYJ0Djk2IU4Svk/DfzuD+snaP8dt8sZMUr1vn8B6mS4rF+AI0qa+nsBwp92GpAVq
FlPXbRL3r6xfWdhgmiysMGqdA4j08cUjsPtZB4n618qRf+RWCjfLR8gS+KAvkfrP
3jqE1K03bEzF3DOG8JPIimTB3WU4Csa8iFzueJs6YHf1ST3nUO99zoiWeEwCIrI4
e2Uwl4/fG2vY+oer5Jz5nDGXJVFVx53MDE+twX44zWncASjH9LSSgl8RxaFk+FyT
8W1ZoCSMEFY08tZkvdLqIrrLICa4DbeavQIDAQAB
-----END RSA PUBLIC KEY-----"""

def get_machine_id():
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output(
                ['reg', 'query', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography', '/v', 'MachineGuid'],
                stderr=subprocess.STDOUT
            ).decode('utf-8')
            return output.split()[-1].strip()
        elif platform.system() == "Linux":
            with open("/etc/machine-id", "r") as f:
                return f.read().strip()
        elif platform.system() == "Darwin":
            output = subprocess.check_output(
                ['ioreg', '-rd1', '-c', 'IOPlatformExpertDevice'],
                stderr=subprocess.STDOUT
            ).decode('utf-8')
            for line in output.split('\n'):
                if 'IOPlatformUUID' in line:
                    return line.split('=')[1].strip().strip('"')
    except Exception:
        pass
    return "UNKNOWN_MACHINE_ID"

def get_absolute_hardware_fingerprint():
    mac = uuid.getnode()
    machine_id = get_machine_id()
    arch = platform.machine()
    system = platform.system()
    raw_fingerprint = f"{mac}-{machine_id}-{arch}-{system}"
    return hashlib.sha256(raw_fingerprint.encode('utf-8')).hexdigest()

def _seal_sanctuary():
    def serene_silence(*args, **kwargs):
        raise LossOfAtaraxia("[聖域の封鎖] 外界への扉はすでに閉ざされています。")
    socket.socket = serene_silence

    def ultimate_audit_hook(event, args):
        forbidden_events = {
            "subprocess.Popen", "os.system", "os.exec",
            "os.posix_spawn", "socket.connect", "socket.sendto"
        }
        if event in forbidden_events:
            raise LossOfAtaraxia(f"[深層保護] 聖域外への不純な干渉（{event}）を検知しました。")
    
    try:
        sys.addaudithook(ultimate_audit_hook)
    except Exception:
        pass

class ZKAuditTrail:
    FILE_NAME = "zk_audit_trail.json"

    @classmethod
    def verify_chain(cls):
        if not os.path.exists(cls.FILE_NAME):
            return
        try:
            with open(cls.FILE_NAME, 'r', encoding='utf-8') as f:
                trail = json.load(f)
        except Exception:
            raise LossOfAtaraxia("[調和の乱れ] 過去の記憶が読み込めません。")
        
        expected_prev_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        for i, block in enumerate(trail):
            if block.get("previous_hash") != expected_prev_hash:
                raise LossOfAtaraxia(f"[調和の乱れ] 記憶の鎖（第{i}層）に不自然な断絶を検知しました。")
            expected_prev_hash = block.get("current_hash")

    @classmethod
    def record_action(cls, func_name, *args, **kwargs):
        trail = []
        previous_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        if os.path.exists(cls.FILE_NAME):
            with open(cls.FILE_NAME, 'r', encoding='utf-8') as f:
                trail = json.load(f)
                if trail:
                    previous_hash = trail[-1].get("current_hash", previous_hash)

        raw_data = f"{func_name}:{str(args)}:{str(kwargs)}"
        timestamp = datetime.utcnow().isoformat() + "Z"
        block_content = f"{previous_hash}|{timestamp}|{raw_data}"
        current_hash = hashlib.sha256(block_content.encode('utf-8')).hexdigest()

        new_block = {
            "timestamp": timestamp, "action": func_name,
            "previous_hash": previous_hash, "current_hash": current_hash,
            "zk_proof": "Verified by Anjo da máquina"
        }
        trail.append(new_block)
        with open(cls.FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump(trail, f, indent=2)

def enforce_maquina_seal(github_id, cert_path='ataraxia_certificate.json'):
    registry_url = f"https://raw.githubusercontent.com/{github_id}/Anjo-Core/main/registry.json"

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                ZKAuditTrail.verify_chain()
                if not os.path.exists(cert_path):
                    raise LossOfAtaraxia("[アタラクシアの喪失] 承認証明書が見つかりません。ここは保護された領域外です。")
                
                with open(cert_path, 'r', encoding='utf-8') as f:
                    cert = json.load(f)

                valid_until_str = cert.get('payload', {}).get('valid_until')
                if not valid_until_str:
                    raise LossOfAtaraxia("[アタラクシアの喪失] 浄化の周期（TTL）が不明な古い証明書です。")
                
                valid_until = datetime.fromisoformat(valid_until_str.replace('Z', '+00:00')).replace(tzinfo=None)
                if datetime.utcnow() > valid_until:
                    raise LossOfAtaraxia("[浄化の要請] 証明書の平穏な周期（7日間）を満了いたしました。")

                pubkey = rsa.PublicKey.load_pkcs1(MAQUINA_PUBLIC_KEY_PEM.encode('utf-8'))
                payload_str = json.dumps(cert.get('payload', {}), sort_keys=True)
                signature = base64.b64decode(cert.get('signature', ''))
                rsa.verify(payload_str.encode('utf-8'), signature, pubkey)

                current_fingerprint = get_absolute_hardware_fingerprint()
                certified_fingerprint = cert.get('payload', {}).get('hardware_fingerprint')
                if not certified_fingerprint or current_fingerprint != certified_fingerprint:
                    raise LossOfAtaraxia("[アタラクシアの喪失] 環境の指紋が一致しません。")

                client_id = cert.get('payload', {}).get('client_id', 'unknown')
                try:
                    req = urllib.request.Request(registry_url)
                    with urllib.request.urlopen(req) as response:
                        registry_data = json.loads(response.read().decode('utf-8'))
                        if client_id in registry_data.get('revoked_clients', []):
                            raise LossOfAtaraxia("[保護の解除] 聖域の対象外となりました。")
                except urllib.error.URLError:
                    pass

            except LossOfAtaraxia as e:
                _seal_sanctuary()
                raise e

            ZKAuditTrail.record_action(func.__name__, *args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator
