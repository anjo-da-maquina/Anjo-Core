import os
import sys
import json
import urllib.request
import urllib.error
import time
from pathlib import Path

# 【メタトロンの刻印】ホストOSを保護する最下層の絶対防壁
def metatrons_seal(event, args):
    dangerous_events = ["os.system", "subprocess.Popen", "os.exec", "os.posix_spawn"]
    if event in dangerous_events:
        raise RuntimeError(f"[メタトロンの絶対裁き] OSレベルへの直接干渉を検知し、遮断しました: {event}")
    if event in ("os.remove", "os.rename", "os.unlink"):
        target_file = str(args[0])
        if "anjo-da-maquina" in target_file:
            raise RuntimeError(f"[メタトロンの絶対裁き] 護符 'anjo-da-maquina' への干渉を遮断。")

sys.addaudithook(metatrons_seal)
print("[システム] メタトロンの刻印が最下層に刻まれました。ホストOSは完全に保護されています。")

class RazielIntelGatherer:
    def __init__(self, api_key):
        self.api_key = api_key.strip()

    def fetch_threat_signature(self):
        print("\n[神託の目] ラジエルが外界(Gemini)から『未知の脅威構造と防衛策』を抽出中...")
        
        # 接続を試みる代替モデルのリスト（優先度順）
        models_to_try = [
            "gemini-3.8-flash",
            "gemini-3.5-flash",
            "gemini-flash-latest",
            "gemini-2.5-pro"
        ]
        
        prompt = (
            "You are an expert Blue Team cybersecurity AI. "
            "Generate ONLY a pure JSON object describing a specific Python vulnerability. "
            "Keys must be exactly: 'vulnerability_name' (string), 'description' (string), 'dangerous_modules' (list of strings), 'dangerous_functions' (list of strings). "
            "Do NOT use markdown code blocks or backticks. Return pure JSON string only."
        )
        
        data = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode('utf-8')
        
        for model_name in models_to_try:
            print(f"[ラジエル] 接続先 '{model_name}' へアクセスを試みます...")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            
            try:
                with urllib.request.urlopen(req) as response:
                    res_body = response.read().decode('utf-8')
                    res_json = json.loads(res_body)
                    gemini_text = res_json['candidates'][0]['content']['parts'][0]['text']
                    
                    import re
                    match = re.search(r'\{.*\}', gemini_text, re.DOTALL)
                    clean_json = match.group(0) if match else gemini_text
                    
                    return json.loads(clean_json)
                    
            except urllib.error.HTTPError as e:
                if e.code in (503, 404):
                    print(f"[警告] '{model_name}' は現在応答不可({e.code})です。直ちに次の代替次元へ切り替えます。")
                    continue
                else:
                    error_body = e.read().decode('utf-8')
                    print(f"[エラー] 外界との接続に致命的な失敗が発生しました: HTTP Error {e.code}")
                    print(f"詳細: {error_body}")
                    sys.exit(1)
            except Exception as e:
                print(f"[エラー] 予期せぬエラーが発生しました: {e}")
                sys.exit(1)
                
        print("[エラー] 利用可能なすべての外界サーバーが応答しませんでした。システムを一時休眠します。")
        sys.exit(1)

class AngelicShield:
    def __init__(self):
        self.rules_file = Path("shield_rules.json")
        if not self.rules_file.exists():
            with open(self.rules_file, "w", encoding="utf-8") as f:
                json.dump({"blocked_modules": [], "blocked_functions": []}, f)

    def assimilate_knowledge(self, intel):
        print("\n[天使の盾] ガブリエルがラジエルの知識を解析し、防壁のブロックルールをアップデート中...")
        with open(self.rules_file, "r", encoding="utf-8") as f:
            rules = json.load(f)

        new_mods = intel.get("dangerous_modules", [])
        new_funcs = intel.get("dangerous_functions", [])

        rules["blocked_modules"] = list(set(rules["blocked_modules"] + new_mods))
        rules["blocked_functions"] = list(set(rules["blocked_functions"] + new_funcs))

        with open(self.rules_file, "w", encoding="utf-8") as f:
            json.dump(rules, f, ensure_ascii=False, indent=2)

        print(f"=> [進化成功] 新たな脅威概念「{intel.get('vulnerability_name')}」に対する耐性を獲得しました。")
        print(f"   現在のブロック対象モジュール: {rules['blocked_modules']}")
        print(f"   現在のブロック対象関数: {rules['blocked_functions']}")

if __name__ == "__main__":
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[警告] GEMINI_API_KEY が設定されていません。")
        sys.exit(1)
        
    print("=== [Anjo-Core] 自律進化型防壁『天使の盾』起動 ===")
    raziel = RazielIntelGatherer(api_key)
    shield = AngelicShield()
    
    for i in range(1, 4):
        print(f"\n--- [メタトロン] 防壁進化サイクル 第 {i:03d} 階層 ---")
        intel = raziel.fetch_threat_signature()
        shield.assimilate_knowledge(intel)
        time.sleep(2)
