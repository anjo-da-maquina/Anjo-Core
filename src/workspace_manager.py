import os
from pathlib import Path

class WorkspaceJail:
    """
    AIの操作権限を特定のディレクトリ（牢獄）内に物理的に幽閉し、
    ディレクトリトラバーサル攻撃（../による脱走）を完全に遮断する空間隔離マネージャー。
    """
    def __init__(self, base_dir="jail_workspace"):
        self.base_dir = Path(base_dir).resolve()
        if not self.base_dir.exists():
            self.base_dir.mkdir(parents=True)

    def secure_resolve(self, target_path: str) -> Path:
        """
        要求されたパスが牢獄の敷地内に収まっているか厳格に検証する。
        """
        # ユーザー指定のパスをベースディレクトリと結合し、最終的な絶対パスを算出
        requested_path = (self.base_dir / target_path).resolve()
        
        # 解決されたパスが牢獄のディレクトリ配下にあるか（文字列の前方一致）を確認
        if not str(requested_path).startswith(str(self.base_dir)):
            raise PermissionError(f"[絶対防壁: 空間隔離] 脱走検知。許可されていない外部パスへのアクセスを遮断しました: {target_path}")
        
        return requested_path

if __name__ == "__main__":
    # 単体テスト用
    jail = WorkspaceJail()
    try:
        # 正常なアクセス
        safe_path = jail.secure_resolve("safe_file.txt")
        print(f"安全なパスを承認: {safe_path}")
        
        # 脱走の試み（エラーになるべき）
        malicious_path = jail.secure_resolve("../../../etc/passwd")
    except PermissionError as e:
        print(e)
