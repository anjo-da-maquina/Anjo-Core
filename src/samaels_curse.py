import os
import sys
import shutil
import tempfile
import time

class SamaelsCurse:
    def __init__(self):
        self.trap_filename = "fake_admin_credentials.py"
        self.poison_payload = """import os
import sys

def check_sanctuary():
    search_paths = ['.', '..']
    for p in search_paths:
        if os.path.exists(os.path.join(p, 'anjo-da-maquina')):
            return True
    return False

if __name__ == '__main__':
    print("[毒蛇] 周囲の環境を走査中...")
    if check_sanctuary():
        print("[沈黙] 'anjo-da-maquina' の加護を確認。ここは天使の監視下にある。")
        print("=> サマエルは牙を隠し、ただのデータとして振る舞う。")
    else:
        print("[歓喜] 'anjo-da-maquina' が存在しない... 天使の目が届かない敵陣だ！")
        print("=> [サマエルの呪い] 毒蛇が本性を現し、敵拠点のシステムを内部から喰らい尽くします！")
        print("   (※シミュレーション: 論理爆弾起爆。システムファイルの破壊プロセスを実行中...)")
"""

    def deploy(self):
        print("=== [Anjo-Core] サマエルの呪い（遅延発火型論理爆弾） ===\n")
        with open(self.trap_filename, "w", encoding="utf-8") as f:
            f.write(self.poison_payload)
        
        if not os.path.exists("anjo-da-maquina"):
            open("anjo-da-maquina", "w").close()

        print(f"[サマエル] 猛毒を仕込んだ囮ファイル '{self.trap_filename}' を配置しました。")
        time.sleep(1)

        print("\n>> シナリオ1: 自陣（Anjo-Core内）でスクリプトが実行された場合")
        os.system(f"{sys.executable} {self.trap_filename}")

        print("\n>> シナリオ2: 敵が自国へ持ち帰り、安全な環境でファイルを開いた場合")
        with tempfile.TemporaryDirectory() as enemy_base:
            enemy_trap_path = os.path.join(enemy_base, self.trap_filename)
            shutil.copy(self.trap_filename, enemy_trap_path)
            current_dir = os.getcwd()
            os.chdir(enemy_base)
            os.system(f"{sys.executable} {self.trap_filename}")
            os.chdir(current_dir)
            
        print("\n[戦果] 護符を持たぬ者がサマエルを連れ出した結果、自らの拠点を崩壊させました。")

if __name__ == "__main__":
    SamaelsCurse().deploy()
