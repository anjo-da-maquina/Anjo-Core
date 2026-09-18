import json
import os
import rsa
import base64
import hashlib
import platform
import subprocess
import sys
import threading
from datetime import datetime

class LossOfAtaraxia(Exception):
    pass

_GLOBAL_SANCTUARY_LOCK = threading.Lock()
_IS_SEALED_GLOBALLY = False
_AUDIT_HOOK_REGISTERED = False
_LAST_KNOWN_HASH = "0000000000000000000000000000000000000000000000000000000000000000"
_LAST_TIMESTAMP = datetime.min

MAQUINA_PUBLIC_KEY_PEM = """-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEApipHFYsJteYGHKzqDVh1TgdQOvORtX2xSVXWYWgT+N+e7qXpqf8P
W7Xq6tEgNIpFkw3PxtWcoCWvFYSCue2fqUl2sBMeTzuUbL+6PG3XNnyEtfjqPRDh
m69F2dEzDsJE9th/nYy5GTwY/PjlN0zWCiyjvOh+SOknRvjUX97RMt1Qls+4vKHt
7EugUoil46/hN4PbzmsTz19N7bwUgVlzOBrwNhNODRKjsjM+rCSICYsCxiL213a3
IGM5gKkA6D8i/RcFMzs7TOfLQ94jLh3MtTGzC6F6bTzyNh2wY1BH+VyxDZCVVtrV
zri+jCjhQSYrEB0Y1CRNcSEoAQd7KvoCcwIDAQAB
-----END RSA PUBLIC KEY-----"""

def get_machine_id():
    try:
        if platform.system() == "Windows":
            out = subprocess.check_output(
                ['reg', 'query', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography', '/v', 'MachineGuid'],
                stderr=subprocess.STDOUT).decode('utf-8')
            return out.split()[-1].strip()
    except Exception:
        pass
    return "UNKNOWN_MACHINE_ID"

def get_absolute_hardware_fingerprint():
    raw_fingerprint = f"{get_machine_id()}-{platform.machine()}-{platform.system()}"
    return hashlib.sha256(raw_fingerprint.encode('utf-8')).hexdigest()

def _register_audit_hook_once():
    global _AUDIT_HOOK_REGISTERED
    if _AUDIT_HOOK_REGISTERED: return

    def ultimate_audit_hook(event, args):
        global _IS_SEALED_GLOBALLY
        if not _IS_SEALED_GLOBALLY: return

        forbidden = {"subprocess.Popen", "os.system", "os.exec", "os.posix_spawn", "socket.connect"}
        if event in forbidden or (event == "import" and args and args[0] in {"ctypes", "_ctypes", "threading"}):
            raise LossOfAtaraxia(f"[深層保護] 不純な干渉（{event}）を破棄しました。")

        if event == "object.__setattr__" and hasattr(args[0], "_IS_SEALED_GLOBALLY"):
            raise LossOfAtaraxia("[深層保護] 認識の改ざんを検知しました。")

    try:
        sys.addaudithook(ultimate_audit_hook)
        _AUDIT_HOOK_REGISTERED = True
    except Exception:
        pass

class ZKAuditTrail:
    FILE_NAME = "zk_audit_trail.json"
    REMOTE_LEDGER_MOCK = "remote_ledger_sync.log"

    @classmethod
    def stream_to_external_ledger(cls, block_data):
        """【絶対記憶の外部同期】ハッシュチェーンを即座に外部へストリーミングする（MVP用モック）"""
        # 本番環境ではここで外部Webhookやクラウド監査ログへ非同期送信を行う
        with open(cls.REMOTE_LEDGER_MOCK, 'a', encoding='utf-8') as f:
            f.write(f"[{block_data['timestamp']}] SYNCED HASH: {block_data['current_hash']} | ACTION: {block_data['action']}\n")

    @classmethod
    def verify_and_record(cls, func_name, *args, **kwargs):
        global _LAST_KNOWN_HASH, _LAST_TIMESTAMP

        current_time = datetime.utcnow()
        if current_time < _LAST_TIMESTAMP:
            raise LossOfAtaraxia("[時間の偽装] 過去への逆行を検知しました。時限浄化は免れません。")
        _LAST_TIMESTAMP = current_time

        trail = []
        if os.path.exists(cls.FILE_NAME):
            with open(cls.FILE_NAME, 'r', encoding='utf-8') as f:
                trail = json.load(f)
                if trail:
                    latest_block = trail[-1]
                    if latest_block.get("current_hash") != _LAST_KNOWN_HASH and _LAST_KNOWN_HASH != "0000000000000000000000000000000000000000000000000000000000000000":
                        raise LossOfAtaraxia("[記憶の欠落] ログが改ざん、または焼却されました。")
                    _LAST_KNOWN_HASH = latest_block.get("current_hash")

        raw_data = f"{func_name}:{str(args)}:{str(kwargs)}"
        timestamp_str = current_time.isoformat() + "Z"
        block_content = f"{_LAST_KNOWN_HASH}|{timestamp_str}|{raw_data}"
        current_hash = hashlib.sha256(block_content.encode('utf-8')).hexdigest()

        new_block = {
            "timestamp": timestamp_str, "action": func_name,
            "previous_hash": _LAST_KNOWN_HASH, "current_hash": current_hash,
            "zk_proof": "Verified by Anjo da máquina"
        }
        trail.append(new_block)

        with open(cls.FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump(trail, f, indent=2)

        # 外部ストリーミングの執行
        cls.stream_to_external_ledger(new_block)

        _LAST_KNOWN_HASH = current_hash

def enforce_maquina_seal(github_id, cert_path='ataraxia_certificate.json'):
    def decorator(func):
        def absolute_closure(*args, **kwargs):
            global _IS_SEALED_GLOBALLY
            with _GLOBAL_SANCTUARY_LOCK:
                _register_audit_hook_once()

                if not os.path.exists(cert_path):
                    raise LossOfAtaraxia("[アタラクシアの喪失] 証明書が見つかりません。")

                with open(cert_path, 'r', encoding='utf-8') as f:
                    cert = json.load(f)

                valid_until = datetime.fromisoformat(cert['payload']['valid_until'].replace('Z', '+00:00')).replace(tzinfo=None)
                if datetime.utcnow() > valid_until:
                    raise LossOfAtaraxia("[浄化の要請] 寿命が尽きました。")

                pubkey = rsa.PublicKey.load_pkcs1(MAQUINA_PUBLIC_KEY_PEM.encode('utf-8'))
                rsa.verify(json.dumps(cert['payload'], sort_keys=True).encode('utf-8'), base64.b64decode(cert['signature']), pubkey)

                if get_absolute_hardware_fingerprint() != cert['payload']['hardware_fingerprint']:
                    raise LossOfAtaraxia("[アタラクシアの喪失] 環境の指紋が一致しません。")

                _IS_SEALED_GLOBALLY = True
                try:
                    result = func(*args, **kwargs)
                finally:
                    _IS_SEALED_GLOBALLY = False

                ZKAuditTrail.verify_and_record(func.__name__, *args, **kwargs)
                return result
        return absolute_closure
    return decorator

def _seal_sanctuary():
    global _IS_SEALED_GLOBALLY
    _register_audit_hook_once()
    _IS_SEALED_GLOBALLY = True
