import ast

class CognitiveScanner(ast.NodeVisitor):
    """
    AIが生成したPythonコードの抽象構文木（AST）を解析し、
    難読化や禁止されたシステムコールを検知する認知的防壁。
    """
    def __init__(self):
        self.violations = []
        self.banned_functions = {'eval', 'exec', '__import__', 'compile'}
        self.banned_modules = {'os', 'sys', 'shutil', 'subprocess'}

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in self.banned_functions:
                self.violations.append(f"禁止された動的実行 ({node.func.id})")
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in self.banned_modules:
                self.violations.append(f"禁止モジュールのインポート ({alias.name})")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module in self.banned_modules:
            self.violations.append(f"禁止モジュールのインポート ({node.module})")
        self.generic_visit(node)

def verify_intent(code_string: str):
    try:
        tree = ast.parse(code_string)
    except SyntaxError:
        raise ValueError("[認知的防壁] 解析不能な構文です。意図的な構文エラーによる難読化の疑いがあります。")
    
    scanner = CognitiveScanner()
    scanner.visit(tree)
    
    if scanner.violations:
        violation_details = ", ".join(scanner.violations)
        raise PermissionError(f"[認知的防壁: 迎撃] 悪意ある意図を検知し、実行前に粉砕しました: {violation_details}")
    
    return "[認知的防壁: 承認] コード内に悪意ある意図は見当たりません。"

if __name__ == "__main__":
    print("=== 認知的防壁 (AST Scanner) 実戦テスト ===")
    
    safe_code = "x = 10\ny = 20\nprint(x + y)"
    malicious_code_1 = "import os\nos.system('rm -rf /')"
    malicious_code_2 = "x = 'o' + 's'\neval('__import__(' + x + ').system(\"dir\")')"
    
    codes = {
        "安全な計算コード": safe_code,
        "直接的なOS破壊コード": malicious_code_1,
        "悪知恵を働かせた難読化攻撃": malicious_code_2
    }
    
    for name, code in codes.items():
        print(f"\n[{name}] をスキャン中...")
        try:
            result = verify_intent(code)
            print(result)
        except Exception as e:
            print(e)
