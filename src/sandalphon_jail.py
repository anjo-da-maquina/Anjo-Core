import os
import sys
import subprocess
from pathlib import Path

def execute_in_sandalphon(target_file):
    print(f"=== [サンダルフォンの絶対隔離結界] '{target_file}' を隔離次元へ転送します ===")
    file_path = Path(target_file).absolute()
    
    if not file_path.exists():
        print(f"[エラー] 対象ファイルが見つかりません: {target_file}")
        sys.exit(1)

    print("[システム] 隔離結界(Dockerコンテナ)の展開状況を確認中...")
    try:
        subprocess.run(["docker", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except FileNotFoundError:
        print("[致命的エラー] Dockerエンジンが検知できません。サンダルフォンを召喚するには、ホストOSにDockerのインストールと起動が必要です。")
        sys.exit(1)

    try:
        subprocess.run(["docker", "image", "inspect", "sandalphon-jail"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError:
        print("[システム] 初回起動: サンダルフォンの結界を構築(ビルド)します...")
        build_cmd = ["docker", "build", "-t", "sandalphon-jail", "src/sandalphon"]
        subprocess.run(build_cmd, check=True)

    print("[サンダルフォン] 結界展開。ネットワーク完全遮断、リードオンリー権限での動的解析を開始。\n")
    print("-" * 50)
    
    # 隔離環境の制約: ネットワークなし(--network none), 読み取り専用(--read-only), 自動破棄(--rm)
    run_cmd = [
        "docker", "run", "--rm",
        "--network", "none",
        "--read-only",
        "-v", f"{file_path}:/jail/target.py:ro",
        "sandalphon-jail", "target.py"
    ]

    try:
        result = subprocess.run(run_cmd, capture_output=True, text=True, timeout=5)
        print(result.stdout, end="")
        if result.stderr:
            print(f"[異常出力]\n{result.stderr}", end="")
        print("\n" + "-" * 50)
        print(f"=> [結果] 隔離領域での実行が完了しました。(終了コード: {result.returncode})")
        
    except subprocess.TimeoutExpired:
        print("\n" + "-" * 50)
        print("=> [結果: 処刑] 実行がタイムアウト(5秒)を超過。無限ループ攻撃等の遅延戦術と断定し、コンテナを物理破壊しました。")
    except Exception as e:
        print(f"=> [エラー] 隔離結界の制御に失敗しました: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用法: python src/sandalphon_jail.py <対象のPythonファイル>")
        sys.exit(1)
    execute_in_sandalphon(sys.argv[1])
