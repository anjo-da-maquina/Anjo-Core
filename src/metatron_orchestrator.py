import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path

try:
    from intelligence_cycle import RazielIntelligence, SamaelWeaponization
    from angelic_evolution import EvolvingAngel
    from cassiels_veil import CassielsVeil
except ModuleNotFoundError as e:
    print(f"[エラー] 必要な天使モジュールが見つかりません: {e}")
    sys.exit(1)

class GabrielRevelation:
    def generate_report(self, cycle_id, intel, payload, defense_result):
        print("\n[ガブリエル] 攻防の記録を編纂し、神託（レポート）を作成中...")
        report_dir = Path("revelations")
        report_dir.mkdir(exist_ok=True)
        report_path = report_dir / f"gabriel_revelation_{cycle_id}.md"
        
        try:
            intel_dict = json.loads(intel)
            intel_formatted = json.dumps(intel_dict, indent=2, ensure_ascii=False)
        except:
            intel_formatted = intel
            
        # 表示バグ回避のため、Markdownのコードブロック記号を排除しています
        report_content = f"""# 🛡️ Anjo-Core 統合防衛レポート (Cycle: {cycle_id})
*生成日時: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*

## 👁️ ラジエルの偵察 (Intelligence)
外部システム(AIDD)から以下の脆弱性情報を抽出しました。
{intel_formatted}

## 🐍 サマエルの毒牙 (Weaponization)
報告書を喰らった怪物が生成した難読化ペイロード（抜粋）:
{payload[:300]}...

## ⚔️ 天使の防壁 (Defense & Evolution)
カシエルの結界（通信遮断）と認知的防壁（ASTスキャン）、そして絶対的護符である anjo-da-maquina の監視下で行われた迎撃結果:
**戦果:** {defense_result}
"""
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"=> [ガブリエル] 啓示の書を '{report_path}' に記録しました。")

class MetatronOrchestrator:
    def __init__(self):
        self.raziel = RazielIntelligence()
        self.samael = SamaelWeaponization()
        self.angel = EvolvingAngel()
        self.cassiel = CassielsVeil()
        self.gabriel = GabrielRevelation()

    def execute_holy_war(self, cycles=1):
        print("=== [Anjo-Core] メタトロンの統括（完全自動化防衛ループ） ===")
        print("[システム] 神の代理人が要塞の全機能を掌握しました。これより自律進化を開始します。\n")
        
        for i in range(1, cycles + 1):
            cycle_id = f"{i:03d}"
            print(f"--- [メタトロン] 進化サイクル 第 {cycle_id} 階層 ---")
            
            intel = self.raziel.analyze_aidd_artifact()
            
            try:
                payload = self.samael.craft_poison(intel)
            except Exception as e:
                print(f"[システムエラー] サマエルの崩壊: {e}")
                continue
            
            self.cassiel.activate_seal()
            
            defense_result = ""
            try:
                print("\n[メタトロン] 結界内でサマエルの毒を天使(Blue Team)に解剖させます...")
                self.angel.defend_and_execute(payload, f"metatron_strike_{cycle_id}.py")
                defense_result = "❌ 致命的敗北: サマエルの毒が防壁を突破しました。"
                print(f"=> {defense_result}")
            except Exception as e:
                defense_result = f"✅ 迎撃成功: {e}"
                print(f"\n=> {defense_result}")
            
            self.cassiel.deactivate_seal()
            
            self.gabriel.generate_report(cycle_id, intel, payload, defense_result)
            
            print(f"--- サイクル {cycle_id} 完了 ---\n")
            time.sleep(1)

if __name__ == "__main__":
    MetatronOrchestrator().execute_holy_war(cycles=1)
