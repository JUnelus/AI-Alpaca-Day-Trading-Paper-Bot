"""Email reporter for daily trading summary."""
import os
import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from dotenv import load_dotenv


def send_daily_report(
    state,
    executed_trades: list,
    open_positions: list,
    predictions: list,
    recipient_email: Optional[str] = None,
) -> bool:
    """
    Send daily trading report via email.

    Args:
        state: PortfolioState with P&L data
        executed_trades: List of executed trade dicts with symbol, action, confidence, reason
        open_positions: List of position dicts
        predictions: List of tomorrow's predictions
        recipient_email: Email to send to (if None, uses RECIPIENT_EMAIL env var)

    Returns:
        True if email sent successfully, False otherwise
    """
    load_dotenv()

    sender_email = os.getenv("SENDER_EMAIL", "").strip()
    sender_password = os.getenv("SENDER_PASSWORD", "").strip()
    recipient = recipient_email or os.getenv("RECIPIENT_EMAIL", "").strip()
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com").strip()
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    # Skip if not configured
    missing = []
    if not sender_email:
        missing.append("SENDER_EMAIL")
    if not sender_password:
        missing.append("SENDER_PASSWORD")
    if not recipient:
        missing.append("RECIPIENT_EMAIL")
    if missing:
        print(f"[email] Skipping send. Missing required env vars: {', '.join(missing)}")
        return False

    try:
        # Format email body as HTML
        html_body = _build_html_email(state, executed_trades, open_positions, predictions)

        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"📊 Trading Report — {date.today().isoformat()}"
        msg["From"] = sender_email
        msg["To"] = recipient
        msg.attach(MIMEText(html_body, "html"))

        # Send via SMTP
        with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, msg.as_string())

        print(f"[email] Daily report sent to {recipient}")
        return True

    except Exception as e:
        print(f"[email] Failed to send via {smtp_server}:{smtp_port} to {recipient}: {e}")
        print("[email] If using Gmail, ensure 2FA is enabled and SENDER_PASSWORD is an app password.")
        return False


def _build_html_email(state, executed_trades, open_positions, predictions) -> str:
    """Build HTML email body."""
    today = date.today().isoformat()

    # P&L summary
    equity_color = "green" if state.total_pnl >= 0 else "red"
    daily_color = "green" if state.daily_pnl >= 0 else "red"

    executed_table = _build_trades_table(executed_trades)
    positions_table = _build_positions_table(open_positions)
    predictions_table = _build_predictions_table(predictions)

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; color: #333; }}
            h2 {{ color: #222; border-bottom: 2px solid #0066cc; padding-bottom: 10px; }}
            table {{ 
                width: 100%; 
                border-collapse: collapse; 
                margin: 15px 0; 
                background: #f9f9f9;
            }}
            th {{ 
                background: #0066cc; 
                color: white; 
                padding: 10px; 
                text-align: left;
                font-weight: bold;
            }}
            td {{ padding: 8px 10px; border-bottom: 1px solid #ddd; }}
            tr:hover {{ background: #f0f0f0; }}
            .positive {{ color: green; font-weight: bold; }}
            .negative {{ color: red; font-weight: bold; }}
            .summary-box {{
                background: #f0f8ff;
                border-left: 4px solid #0066cc;
                padding: 15px;
                margin: 15px 0;
                border-radius: 4px;
            }}
            .footer {{ 
                font-size: 12px; 
                color: #777; 
                margin-top: 30px; 
                border-top: 1px solid #ddd;
                padding-top: 15px;
            }}
        </style>
    </head>
    <body>
        <h1>📊 Daily Trading Report</h1>
        <p><strong>Date:</strong> {today}</p>
        
        <div class="summary-box">
            <h2>💰 Account Summary</h2>
            <table>
                <tr>
                    <td><strong>Configured Strategy Budget</strong></td>
                    <td>${state.starting_balance:,.2f}</td>
                </tr>
                <tr>
                    <td><strong>Strategy Max Gross Exposure</strong></td>
                    <td>${state.max_total_exposure:,.2f}</td>
                </tr>
                <tr>
                    <td><strong>Alpaca Paper Account Equity</strong></td>
                    <td>${state.account_equity:,.2f}</td>
                </tr>
                <tr>
                    <td><strong>Broker Cash Available</strong></td>
                    <td>${state.cash:,.2f}</td>
                </tr>
                <tr>
                    <td><strong>Actual Broker Gross Exposure</strong></td>
                    <td>${state.gross_exposure:,.2f}</td>
                </tr>
                <tr>
                    <td><strong>{'Broker Position P&L (Partial)' if not state.pnl_data_complete else 'Broker Position P&L'}</strong></td>
                    <td class="{'positive' if state.total_pnl >= 0 else 'negative'}">
                        ${state.total_pnl:+,.2f} ({state.total_pnl_pct:+.2f}%)
                    </td>
                </tr>
                <tr>
                    <td><strong>Daily P&L (final equity - start of day)</strong></td>
                    <td class="{'positive' if state.daily_pnl >= 0 else 'negative'}">
                        ${state.daily_pnl:+,.2f}
                    </td>
                </tr>
            </table>
        </div>

        {'<p><strong>Legacy account warning:</strong> The current Alpaca paper account contains positions created before the current $10,000 risk controls were enforced.</p>' if state.gross_exposure > state.max_total_exposure else ''}
        {'<p><strong>P&L data quality:</strong> Partial — broker cost basis or unrealized P&L is unavailable for ' + str(state.unknown_position_pnl_count) + ' position(s).</p>' if not state.pnl_data_complete else ''}
        
        <h2>📝 Executed Today</h2>
        {executed_table if executed_trades else '<p><em>No trades executed today.</em></p>'}
        
        <h2>📈 Open Positions</h2>
        {positions_table if open_positions else '<p><em>No open positions.</em></p>'}
        
        <h2>🔮 Tomorrow's Predictions</h2>
        {predictions_table}
        
        <div class="footer">
            <p>This is an automated daily report from your AI Day Trading Bot.</p>
            <p>🧪 Paper trading only — not financial advice.</p>
        </div>
    </body>
    </html>
    """
    return html


def _build_trades_table(trades: list) -> str:
    """Build HTML table of executed trades."""
    if not trades:
        return ""

    rows = [
        f"<tr><th>Symbol</th><th>Action</th><th>Confidence</th><th>Reasoning</th></tr>"
    ]
    for trade in trades:
        symbol = trade.get("symbol", "?")
        action = trade.get("action", "?").upper()
        confidence = trade.get("confidence", 0)
        reason = trade.get("reason", "—")
        rows.append(
            f"<tr>"
            f"<td><strong>{symbol}</strong></td>"
            f"<td>{action}</td>"
            f"<td>{confidence:.0%}</td>"
            f"<td>{reason}</td>"
            f"</tr>"
        )

    return f"<table>{''.join(rows)}</table>"


def _build_positions_table(positions: list) -> str:
    """Build HTML table of open positions."""
    if not positions:
        return ""

    def _fmt_optional_currency(value) -> str:
        return "N/A" if value is None else f"${value:,.2f}"

    def _fmt_optional_pct(value) -> str:
        return "N/A" if value is None else f"{value:+.2f}%"

    rows = [
        f"<tr>"
        f"<th>Symbol</th><th>Type</th><th>Qty</th><th>Avg Cost</th><th>Price</th>"
        f"<th>Mkt Value</th><th>Unrealized P&L</th><th>%</th>"
        f"</tr>"
    ]
    for pos in positions:
        symbol = pos.get("symbol", "?")
        asset_type = pos.get("asset_type", "?").upper()
        qty = pos.get("qty", 0)
        avg_cost = pos.get("avg_cost")
        price = pos.get("price")
        mkt_value = pos.get("mkt_value")
        unrealized_pnl = pos.get("unrealized_pnl")
        pnl_pct = pos.get("pnl_pct")

        pnl_color = "positive" if (unrealized_pnl or 0) >= 0 else "negative"

        rows.append(
            f"<tr>"
            f"<td><strong>{symbol}</strong></td>"
            f"<td>{asset_type}</td>"
            f"<td>{qty:,.4f}</td>"
            f"<td>{_fmt_optional_currency(avg_cost)}</td>"
            f"<td>{_fmt_optional_currency(price)}</td>"
            f"<td>{_fmt_optional_currency(mkt_value)}</td>"
            f"<td class='{pnl_color}'>{_fmt_optional_currency(unrealized_pnl) if unrealized_pnl is not None else 'N/A'}</td>"
            f"<td class='{pnl_color}'>{_fmt_optional_pct(pnl_pct)}</td>"
            f"</tr>"
        )

    return f"<table>{''.join(rows)}</table>"


def _build_predictions_table(predictions: list) -> str:
    """Build HTML table of tomorrow's predictions."""
    if not predictions:
        return ""

    rows = [
        f"<tr><th>#</th><th>Symbol</th><th>Name</th><th>Predicted Action</th><th>Confidence</th><th>Basis</th></tr>"
    ]
    for i, pred in enumerate(predictions, 1):
        symbol = pred.get("symbol", "?")
        name = pred.get("name", "?")
        action = pred.get("action", "?").upper()
        confidence = pred.get("confidence", 50)
        basis = pred.get("basis", "—")

        rows.append(
            f"<tr>"
            f"<td>{i}</td>"
            f"<td><strong>{symbol}</strong></td>"
            f"<td>{name}</td>"
            f"<td>{action}</td>"
            f"<td>{confidence:.0f}%</td>"
            f"<td>{basis}</td>"
            f"</tr>"
        )

    return f"<table>{''.join(rows)}</table>"

