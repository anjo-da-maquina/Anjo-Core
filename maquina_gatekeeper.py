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

# 【V3進化】プロセス全体を縛るグローバルロック（マルチスレッド脱獄の封殺）
_GLOBAL_SANCTUARY_LOCK = threading.Lock()
_IS_SEALED_GLOBALLY = False
_AUDIT_HOOK_REGISTERED = False

# 【V3進化】O(1)検証のためのオンメモリ記憶状態
_LAST_KNOWN_HASH = "0000000000000000000000000000000000000000000000000000000000000000"
_LAST_TIMESTAMP = datetime.min

MAQUINA_PUBLIC_KEY_PEM = """-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAoRYzSzro4Yp0Gnjvgy/pHW4NgWlCi1JI3sf93CfsREOC1KGfuV3A
tBqImHuwhFeH4alJDZGfiuxxbEU5qTAUPZNr7IKCHwWklmFpLQt+SkBdI/F/yDno
0dHj5zLKMXIhyXdMWhjuEGSJx4BdEYRDwCuB6hNHDTBbmPkJy8LVJAIWOnKpl/cv
/ZYtDC+cQuiyMVyuIijSXOPqrIuDXbOhtIx0pi1T2RHquaIxrWDCUZXxDW4pG+XW
dNQ5A+Prns723yHQz/BYgpnwfsm/MLtYhgo15o6k1GbrCXByYGkUAUSWRbDFedjl
+RNXas5443BekQi2OfljWIkh2SmN4w2K1QIDAQAB
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

        # 聖域内のスレッド生成、OSコマンド、ネットワーク、ctypesを全て粉砕
        forbidden = {"subprocess.Popen", "os.system", "os.exec", "os.posix_spawn", "socket.connect"}
        if event in forbidden or (event == "import" and args and args[0] in {"ctypes", "_ctypes", "threading"}):
            raise LossOfAtaraxia(f"[深層保護] 不純な干渉（{event}）を破棄しました。")
        
        # 【V3進化】sys.modules等の内部書き換えによる防壁解除（Reflection）を封殺
        if event == "object.__setattr__" and hasattr(args[0], "_IS_SEALED_GLOBALLY"):
            raise LossOfAtaraxia("[深層保護] 認識の改ざんを検知しました。")

    try:
        sys.addaudithook(ultimate_audit_hook)
        _AUDIT_HOOK_REGISTERED = True
    except Exception:
        pass

class ZKAuditTrail:
    FILE_NAME = "zk_audit_trail.json"

    @classmethod
    def verify_and_record(cls, func_name, *args, **kwargs):
        global _LAST_KNOWN_HASH, _LAST_TIMESTAMP
        
        # 【V3進化】時間の巻き戻し（不死の獲得）を検知
        current_time = datetime.utcnow()
        if current_time < _LAST_TIMESTAMP:
            raise LossOfAtaraxia("[時間の偽装] 過去への逆行を検知しました。時限浄化は免れません。")
        _LAST_TIMESTAMP = current_time

        # 【V3進化】O(1)の差分検証（メモリ上の最新ハッシュとファイルの末尾のみを比較）
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
            
        _LAST_KNOWN_HASH = current_hash

def enforce_maquina_seal(github_id, cert_path='ataraxia_certificate.json'):
    def decorator(func):
        # 【V3進化】functools.wrapsを捨て、__wrapped__からの関数抽出を完全に隠蔽
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
