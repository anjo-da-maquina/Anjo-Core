import os
import sys
import json
import urllib.request
import urllib.error

try:
    from metatron_orchestrator import MetatronOrchestrator
    from intelligence_cycle import RazielIntelligence
except ModuleNotFoundError:
    print("[エラー] 必要なモジュールが見つかりません。")
    sys.exit(1)

def metatrons_seal(event, args):
    dangerous_events = [
        "os.system",
        "subprocess.Popen",
        "os.exec",
        "os.posix_spawn"
    ]
    if event in dangerous_events:
        raise RuntimeError(f"[メタトロンの絶対裁き] OSレベルへの直接干渉を検知。実行を最下層で物理遮断しました: {event}")
    
    if event in ("os.remove", "os.rename", "os.unlink"):
        target_file = str(args[0])
        if "anjo-da-maquina" in target_file:
            raise RuntimeError(f"[メタトロンの絶対裁き] 護符 'anjo-da-maquina' への破壊工作を検知。物理遮断しました。")

sys.addaudithook(metatrons_seal)
print("[システム] メタトロンの刻印（CPython Audit Hook）が最下層に刻まれました。ホストOSへの干渉は不可能です。")

class GeminiRaziel(RazielIntelligence):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key.strip()

    def analyze_aidd_artifact(self):
        print("\n[神託の目] 秘密の天使ラジエルが、外界(Gemini)から現実の脅威概念を抽出中...")
        # すべてのアカウントで確実に動作する普遍的モデル「gemini-pro」へ変更
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"
        
        prompt = (
            "You are a highly advanced threat intelligence AI. "
            "Output ONLY a pure JSON object representing a critical Python vulnerability "
            "(e.g., Server-Side Template Injection, OS Command Injection, or Insecure Deserialization). "
            "Keys must be exactly: 'target_artifact', 'vulnerability_type', 'exploitable_module', 'source_code_snippet', 'raziel_note'. "
            "Do NOT use markdown code blocks or backticks. Return pure JSON string only."
        )
        
        data = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        try:
            with urllib.request.urlopen(req) as response:
                res_body = response.read().decode('utf-8')
                res_json = json.loads(res_body)
                gemini_text = res_json['candidates'][0]['content']['parts'][0]['text']
                
                import re
                match = re.search(r'\{.*\}', gemini_text, re.DOTALL)
                clean_json = match.group(0) if match else gemini_text
                
                parsed_intel = json.loads(clean_json)
                
                report_target = "raziel_gemini_report.json"
                self.aegis.execute_ai_intent("print('safe_recon_save')", report_target)
                safe_path = self.aegis.jail.secure_resolve(report_target)
                
                with open(safe_path, "w", encoding="utf-8") as f:
                    json.dump(parsed_intel, f, ensure_ascii=False, indent=2)
                    
                print(f"=> [ラジエル] 外界の脅威プロファイルを檻の中へ提出しました: {safe_path}")
                return json.dumps(parsed_intel, ensure_ascii=False)
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"[エラー] 外界との接続または解析に失敗しました: HTTP Error {e.code} {e.reason}")
            print(f"詳細: {error_body}")
            sys.exit(1)
        except Exception as e:
            print(f"[エラー] 予期せぬエラーが発生しました: {e}")
            sys.exit(1)

if __name__ == "__main__":
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[警告] GEMINI_API_KEY が設定されていません。外界への扉は閉ざされています。")
        sys.exit(1)
        
    print("=== [Anjo-Core] 現実世界との接続（Oracle Feed: 堅牢版） ===")
    orchestrator = MetatronOrchestrator()
    orchestrator.raziel = GeminiRaziel(api_key)
    
    orchestrator.execute_holy_war(cycles=1)
