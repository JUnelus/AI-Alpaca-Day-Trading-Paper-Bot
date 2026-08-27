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
    assert "python -m src.main --mode trade --scheduled-run" in content
    assert "python -m src.main --mode report --scheduled-run" in content
    assert "run: python -m src.main --mode ${{ inputs.mode }}" in content
    assert "ALPACA_PAPER:      'true'" in content
    assert "push:" not in content
    assert "pull_request:" not in content


def test_bot_workflow_has_concurrency_and_dst_safe_schedules():
    content = BOT_WORKFLOW.read_text(encoding="utf-8")
    assert "concurrency:" in content
    assert "group: alpaca-paper-trading-bot" in content
    assert "cancel-in-progress: false" in content
    assert content.count("timezone: 'America/New_York'") == 2
    assert "45 9 * * 1-5" in content
    assert "15 16 * * 1-5" in content
    assert "45 13 * * 1-5" not in content
    assert "45 14 * * 1-5" not in content
    assert "15 20 * * 1-5" not in content
    assert "15 21 * * 1-5" not in content


def test_bot_workflow_commits_state_even_if_bot_step_fails():
    content = BOT_WORKFLOW.read_text(encoding="utf-8")
    assert "continue-on-error: true" in content
    assert "if: always()" in content
    assert "if [ -f \"$file\" ]; then" in content
    assert "steps.run_bot.outcome == 'failure'" in content


