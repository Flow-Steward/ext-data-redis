"""Standalone Redis identity and provider isolation."""

import yaml
import main
from test_runtime import envelope, fake
from test_package import packager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_standalone_identity_and_single_provider():
    manifest = yaml.safe_load((ROOT / "extension.yaml").read_text())
    assert manifest["extension_id"] == "flowsteward.redis"
    connections = yaml.safe_load((ROOT / "contracts/connection_types.yaml").read_text())
    assert [item["connection_type_id"] for item in connections["connection_types"]] == [
        "redis_database",
        "redis",
    ]
    assert packager().TOP_FOLDER == "flowsteward_redis"
    assert packager().EXTENSION_ID == "flowsteward.redis"


def test_valkey_connection_is_rejected_before_provider_io(monkeypatch):
    calls = fake(monkeypatch, "unexpected")
    result = main.handle(envelope("get", kind="valkey"))
    assert result["ok"] is False
    assert result["error_code"] == "invalid_connection"
    assert result["definitely_no_external_effect"] is True
    assert calls == []
