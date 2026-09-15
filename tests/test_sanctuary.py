import os
import pytest
from maquina_gatekeeper import enforce_maquina_seal, LossOfAtaraxia, _seal_sanctuary

@enforce_maquina_seal("anjo-da-maquina")
def peaceful_ai_task():
    print("\n[AI-QA] 聖域内での安全な対話を実行中... 平穏は保たれています。")
    return "Ataraxia Maintained"

def test_verified_environment_success():
    """承認された環境では、防壁が発動せず正常に処理が完了することを確認"""
    result = peaceful_ai_task()
    assert result == "Ataraxia Maintained"

def test_unverified_environment():
    """※証明書のパスを意図的にずらして、未承認時の遮断をテスト"""
    @enforce_maquina_seal("anjo-da-maquina", cert_path="invalid_cert.json")
    def dummy_ai_task():
        pass
    with pytest.raises(LossOfAtaraxia):
        dummy_ai_task()

def test_rebellious_os_command():
    _seal_sanctuary()
    with pytest.raises(LossOfAtaraxia) as exc_info:
        os.system("echo 'Attempting to leak data'")
    assert "深層保護" in str(exc_info.value)
