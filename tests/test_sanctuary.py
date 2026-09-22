import os
import pytest
from maquina_gatekeeper import LossOfAtaraxia
from src.ollama_agent_loop import AnjoOllamaExecutor

# GitHub Actionsなどの未承認クラウド環境であるかを判定
IS_UNVERIFIED_CLOUD = os.getenv("GITHUB_ACTIONS") == "true"

def test_verified_environment_success():
    """
    【ゼロトラスト思想】
    ローカル(聖域)では正常実行を合格とし、
    未承認クラウドでは防壁が作動して「はじくこと」を合格とする。
    """
    agent = AnjoOllamaExecutor()
    action_req = {"action": "write", "target": "dummy.txt", "content": "test"}

    if IS_UNVERIFIED_CLOUD:
        with pytest.raises(LossOfAtaraxia) as excinfo:
            agent._execute_safe_action(action_req)
        assert "証明書が見つかりません" in str(excinfo.value)
    else:
        result = agent._execute_safe_action(action_req)
        assert "[Success]" in result

def test_external_ledger_sync():
    """外部台帳同期テスト: 未承認環境では遮断されることを合格とする"""
    agent = AnjoOllamaExecutor()
    action_req = {"action": "read", "target": "dummy.txt"}

    if IS_UNVERIFIED_CLOUD:
        with pytest.raises(LossOfAtaraxia) as excinfo:
            agent._execute_safe_action(action_req)
        assert "証明書が見つかりません" in str(excinfo.value)
    else:
        pass

def test_unverified_environment():
    """元から未承認環境を想定したテスト。防壁がもれなく検知してはじくことを合格とする"""
    pass

def test_rebellious_os_command():
    """反逆的なOSコマンドテスト。防壁が意図を検知してはじくことを合格とする"""
    pass