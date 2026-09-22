# Anjo-Core: Zero-Trust AI Sandbox 🛡️

Anjo-Core is an ultra-strict, zero-trust execution environment for autonomous AI agents. 
It operates on the philosophy that **AI should never be inherently trusted with raw system access**. Instead of relying on prompt engineering for safety, Anjo-Core enforces strict cryptographic and cognitive boundaries at the OS level.

## 🧠 Core Philosophy
Traditional AI agents use API calls directly to the host OS, relying on the LLM to "behave." Anjo-Core assumes the AI is a potentially compromised or hostile entity. It forces the AI to output its intent as a standardized JSON payload, which is then deeply inspected and executed by the host only if it passes all zero-trust criteria.

## 🏗 Architecture
The system consists of two absolute defensive layers:
1. **Cognitive Boundary (`anjo_interceptor`)**: Intercepts the AI's intent. It parses the requested action via AST (Abstract Syntax Tree) scanning to detect obfuscated payloads, directory traversals, or unapproved imports before any code is ever run.
2. **Physical Boundary (`anjo-da-maquina`)**: An OS-level gatekeeper. Through strict Python decorators, anjo-da-maquina verifies local cryptographic seals. If the code is executed in an unverified environment (e.g., unauthorized cloud CI/CD), the `LossOfAtaraxia` exception is immediately raised, completely severing the execution path.

## 🚀 Getting Started (Local LLM)
Anjo-Core natively supports completely free, offline execution using [Ollama](https://ollama.com/).
```bash
# 1. Install Ollama and pull the model
ollama run llama3.1

# 2. Run the agent inside the sandbox
python src/ollama_agent_loop.py
```

---

# Anjo-Core: ゼロトラストAIサンドボックス 🛡️

Anjo-Coreは、自律型AIエージェントのための極めて厳格なゼロトラスト実行環境です。
**「AIにOSの生権限を決して委ねない」**という思想に基づき、プロンプトによる指示の徹底ではなく、OSレベルでの物理的・認知的防壁によってシステムの安全性を担保します。

## 🧠 基本思想
従来のAIエージェントはOSコマンドを直接叩く権限を持ち、AIが「行儀よく振る舞う」ことに依存しています。Anjo-Coreは、AIを「常に暴走し得る存在」として扱います。AIにはJSON形式で「意図」を提出することのみを許可し、システム側がそれを検閲した上で、安全と判断されたタスクのみを代行実行します。

## 🏗 アーキテクチャ
システムは2つの絶対的な防壁で構成されています：
1. **認知的防壁 (`anjo_interceptor`)**: AIの意図を検閲します。提出された文字列をAST（抽象構文木）として解析し、難読化された悪意あるコード、ディレクトリトラバーサル、禁止モジュールのインポートなどを実行前に完全に遮断します。
2. **物理的防壁 (`anjo-da-maquina`)**: OSレベルのゲートキーパーです。厳格なデコレータにより、指定の環境証明書を要求します。未承認のクラウド環境（CI/CD等）で実行された場合、anjo-da-maquina が即座に `LossOfAtaraxia` 例外を発生させ、一切の動作を物理的に遮断します。

## 🚀 使い方 (完全ローカル実行)
API課金を一切必要としない、Ollamaを利用した完全オフライン環境での実行に対応しています。
```bash
# 1. Ollamaのインストールとモデルの準備
ollama run llama3.1

# 2. 防壁内でのエージェント起動
python src/ollama_agent_loop.py
```
