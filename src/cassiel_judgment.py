import os
import sys
import json
import ast
from pathlib import Path

# 【メタトロンの刻印】ホストOSを保護する最下層の絶対防壁
def metatrons_seal(event, args):
    dangerous_events = ["os.system", "subprocess.Popen", "os.exec", "os.posix_spawn"]
    if event in dangerous_events:
        raise RuntimeError(f"[メタトロンの絶対裁き] OSレベルへの直接干渉を検知し、遮断しました: {event}")
    if event in ("os.remove", "os.rename", "os.unlink"):
        target_file = str(args[0])
        if "chotam-merkabah" in target_file:
            raise RuntimeError(f"[メタトロンの絶対裁き] 聖なる護符 'chotam-merkabah' への干渉を遮断。")

sys.addaudithook(metatrons_seal)

class CassielInquisitor(ast.NodeVisitor):
    def __init__(self, rules):
        self.rules = rules
        self.violations = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in self.rules.get("blocked_modules", []):
                self.violations.append(f"禁止モジュール '{alias.name}' のインポートを検知 (行: {node.lineno})")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module in self.rules.get("blocked_modules", []):
            self.violations.append(f"禁止モジュール '{node.module}' からのインポートを検知 (行: {node.lineno})")
        for alias in node.names:
            if alias.name in self.rules.get("blocked_functions", []):
                self.violations.append(f"禁止関数 '{alias.name}' の直接インポートを検知 (行: {node.lineno})")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in self.rules.get("blocked_functions", []):
                self.violations.append(f"禁止関数 '{func_name}' の実行呼び出しを検知 (行: {node.lineno})")
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
            if func_name in self.rules.get("blocked_functions", []):
                self.violations.append(f"禁止属性/メソッド '{func_name}' の呼び出しを検知 (行: {node.lineno})")
        self.generic_visit(node)

def execute_judgment(target_file):
    print(f"=== [カシエルの審問] ハシュマリエルの命により、'{target_file}' を解剖する ===")
    rules_file = Path("shield_rules.json")
    if not rules_file.exists():
        print("[エラー] 防壁ルール(shield_rules.json)が存在しません。天使の盾を先に稼働させてください。")
        sys.exit(1)

    with open(rules_file, "r", encoding="utf-8") as f:
        rules = json.load(f)

    # 修正: utf-8-sig を使用し、BOM(U+FEFF)などの不可視ノイズを自動的に除去して読み込む
    with open(target_file, "r", encoding="utf-8-sig") as f:
        source_code = f.read()

    try:
        tree = ast.parse(source_code)
        inquisitor = CassielInquisitor(rules)
        inquisitor.visit(tree)

        if inquisitor.violations:
            print("\n[判決: 異端検知] 以下の致命的な防壁ルール違反が見つかりました:")
            for v in inquisitor.violations:
                print(f"  - {v}")
            print("\n=> [結果] 実行は物理的に不可能です。対象を破棄します。")
        else:
            print("\n[判決: 潔白] 違反は見つかりませんでした。安全なコードです。")

    except SyntaxError as e:
        print(f"\n[判決: 構文異常] 解析不能なコード構造です: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用法: python src/cassiel_judgment.py <対象のPythonファイル>")
        sys.exit(1)
    
    execute_judgment(sys.argv[1])
