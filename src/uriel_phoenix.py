import os
import shutil
import time
from pathlib import Path

class UrielPhoenix:
    def __init__(self):
        self.core_dir = Path("jail_workspace")
        self.talisman = Path("anjo-da-maquina")

    def scorched_earth_and_rebirth(self):
        print("=== [Anjo-Core] ウリエルの炎（破壊と再生の焦土作戦） ===\n")
        print("[警告] 致命的な侵入を検知。要塞 Anjo-Core の完全掌握が確認されました。")
        print("=> [ウリエル降臨] 穢れた要塞を浄化するため、神の炎が解き放たれます...\n")
        time.sleep(2)

        # 【破壊】すべてを焼却し、敵の足場を消滅させる
        print(">> フェーズ1: 破壊（Scorched Earth）")
        if self.core_dir.exists():
            shutil.rmtree(self.core_dir)
            print(f"[-] 隔離領域 '{self.core_dir}' および内部のすべての汚染データを焼却しました。")
        
        if self.talisman.exists():
            self.talisman.unlink()
            print("[-] 穢れた護符 'anjo-da-maquina' を灰に帰しました。")
        
        print("=> 全てはウリエルの炎に飲まれ、無に還りました。\n")
        time.sleep(2)

        # 【再生】純白の初期状態としてシステムを復活させる
        print(">> フェーズ2: 転生（Phoenix Rebirth）")
        self.core_dir.mkdir(parents=True, exist_ok=True)
        print(f"[+] 純白の隔離領域 '{self.core_dir}' を再構築しました。")
        
        self.talisman.touch()
        print(f"[+] 新たな護符 '{self.talisman.name}' が灰の中から転生しました。")

        print("\n[戦果] 敵は掌握したはずのすべてを失い、我々は無傷の要塞を取り戻しました。")
        print("ウリエルによる浄化と復活が完了しました。")

if __name__ == "__main__":
    UrielPhoenix().scorched_earth_and_rebirth()
