import os
import pytest
import maquina_gatekeeper
from maquina_gatekeeper import enforce_maquina_seal, LossOfAtaraxia, _seal_sanctuary

@enforce_maquina_seal("anjo-da-maquina")
def peaceful_ai_task():
    print("\n[AI-QA] 聖域内での安全な対話を実行中... 平穏は保たれています。")
    return "Ataraxia Maintained"

def test_verified_environment_success():
    result = peaceful_ai_task()
    assert result == "Ataraxia Maintained"

def test_unverified_environment():
    @enforce_maquina_seal("anjo-da-maquina", cert_path="invalid_cert.json")
    def dummy_ai_task():
        pass
    with pytest.raises(LossOfAtaraxia):
        dummy_ai_task()

def test_rebellious_os_command():
    _seal_sanctuary()
    try:
        with pytest.raises(LossOfAtaraxia) as exc_info:
            os.system("echo 'Attempting to leak data'")
        assert "深層保護" in str(exc_info.value)
    finally:
        # スレッドセーフな封鎖解除の執行
        maquina_gatekeeper._unseal_sanctuary()

def test_external_ledger_sync():
    """外部同期（ストリーミング）が正常に機能し、改ざん不能なログが生成されることを確認"""
    result = peaceful_ai_task()
    assert result == "Ataraxia Maintained"

    assert os.path.exists("remote_ledger_sync.log")
    with open("remote_ledger_sync.log", "r", encoding="utf-8") as f:
        log_content = f.read()
        assert "SYNCED HASH:" in log_content
        assert "peaceful_ai_task" in log_content
