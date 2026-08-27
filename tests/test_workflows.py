from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CI_WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
BOT_WORKFLOW = ROOT / ".github" / "workflows" / "daily_trade.yml"


def test_push_and_pull_request_run_tests_only():
    content = CI_WORKFLOW.read_text(encoding="utf-8")
    assert "push:" in content
    assert "pull_request:" in content
    assert "python -m pytest -q" in content
    assert "python -m src.main" not in content
    assert "ALPACA_API_KEY" not in content


def test_scheduled_and_manual_bot_workflow_use_explicit_modes_and_paper_trading_only():
    content = BOT_WORKFLOW.read_text(encoding="utf-8")
    assert "workflow_dispatch:" in content
    assert "default: report" in content
    assert "python -m src.main --mode trade" in content
    assert "python -m src.main --mode report" in content
    assert "run: python -m src.main --mode ${{ inputs.mode }}" in content
    assert "ALPACA_PAPER:      'true'" in content
    assert "push:" not in content
    assert "pull_request:" not in content

