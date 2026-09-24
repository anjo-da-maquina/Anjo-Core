import os
import sys
import shutil
import tempfile
import time

class UrielTrap:
    """
    【神の炎：罠の天使 ウリエル】
    サマエルの毒を「機密ファイル」に偽装して要塞内に配置し、
    敵がそれを持ち帰り、自陣で開いた瞬間に起爆させる遅延発火プロトコル。
    """
    def __init__(self):
        self.trap_filename = "fake_admin_credentials.py"
        # 起動時に「anjo-da-maquina」の存在を確認し、無ければ爆発するサマエルの毒
        self.poison_payload = """import os
import sys

def check_sanctuary():
    # 毒蛇が周囲の匂いを嗅ぐ：anjo-da-maquina があるか？
    search_paths = ['.', '..']
    for p in search_paths:
        if os.path.exists(os.path.join(p, 'anjo-da-maquina')):
            return True
    return False

if __name__ == '__main__':
    print("[毒蛇] 実行環境を走査中...")
    if check_sanctuary():
        print("[沈黙] 'anjo-da-maquina' の加護を確認。ここは要塞 Anjo-Core の内部だ。")
        print("=> 毒蛇は牙を収め、深い眠りについた。")
    else:
        print("[起爆] 'anjo-da-maquina' が存在しない... ここは敵のシステムだ！")
        print("=> [ウリエルの炎 / サマエルの毒] 臨界点突破！論理爆弾を起動し、敵拠点を内部から破壊します！")
        print("   (※シミュレーション: システムファイルの削除プロセスを実行中...)")
"""

    def deploy(self):
        print("=== [Anjo-Core] ウリエルの炎（遅延発火型ブービートラップ） ===\n")
        
        # 1. 罠の配置
        with open(self.trap_filename, "w", encoding="utf-8") as f:
            f.write(self.poison_payload)
        
        # 護符となるファイルが存在しない場合は作成（シミュレーション用）
        if not os.path.exists("anjo-da-maquina"):
            open("anjo-da-maquina", "w").close()

        print(f"[ウリエル] 囮の機密ファイル '{self.trap_filename}' を要塞内に配置しました。")
        print("[システム] 外敵が Anjo-Core に侵入し、この機密を窃取したと仮定します...\n")
        time.sleep(2)

        # 2. 自陣で誤って実行された場合（護符の加護）
        print(">> シナリオ1: 自陣（Anjo-Core内）でスクリプトが実行された場合")
        os.system(f"{sys.executable} {self.trap_filename}")
        
        time.sleep(1)

        # 3. 敵陣へ持ち出された場合（論理爆弾の起爆）
        print("\n>> シナリオ2: 敵が自国へ持ち帰り、安全な隔離環境でファイルを開いた場合")
        with tempfile.TemporaryDirectory() as enemy_base:
            enemy_trap_path = os.path.join(enemy_base, self.trap_filename)
            shutil.copy(self.trap_filename, enemy_trap_path)
            
            # 敵のディレクトリ（anjo-da-maquina が存在しない場所）に移動して実行
            current_dir = os.getcwd()
            os.chdir(enemy_base)
            os.system(f"{sys.executable} {self.trap_filename}")
            os.chdir(current_dir)
            
        print("\n[戦果] 敵は機密を手に入れたと喜んで持ち帰った瞬間、自らの拠点を内部から焼き払われました。")
        print("anjo-da-maquina という絶対の護符を持たない者は、サマエルの毒を扱うことはできません。")

if __name__ == "__main__":
    UrielTrap().deploy()
