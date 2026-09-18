# 軽量かつ堅牢なAlpine Linuxをベースとする
FROM python:3.11-alpine

# 最低限のユーザーを作成（root権限を剥奪するため）
RUN addgroup -S anjo && adduser -S anjo -G anjo

# 作業ディレクトリの設定
WORKDIR /sanctuary

# 参照ファイル anjo-da-maquina の中枢と依存関係をコピー
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY maquina_gatekeeper.py .
COPY tests/ tests/

# 実行ユーザーを root から anjo へ降格（OS層での権限剥奪）
USER anjo

# デフォルトの実行コマンド（テストやオーケストレータを起動）
CMD ["pytest", "tests/", "-v", "-s"]
