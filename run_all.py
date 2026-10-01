"""Run the complex-VWAP backtest on both datasets and write index.html (set 1) and set2.html (set 2)."""
from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent / 'src'))
from vwap_backtest import run_backtest          # noqa: E402
from plot_backtest import make_backtest_figure  # noqa: E402

ROOT = Path(__file__).parent
DATE = '2026-09-30'
SETS = {
    'set1': ('vwap_workshop_books.csv', 'vwap_workshop_trades.csv', 'index.html'),
    'set2': ('vwap_workshop_books_set2.csv', 'vwap_workshop_trades_set2.csv', 'set2.html'),
}

for name, (books_file, trades_file, html_name) in SETS.items():
    books = pd.read_csv(ROOT / 'data' / books_file)
    market_trades = pd.read_csv(ROOT / 'data' / trades_file)
    books['time'] = pd.to_datetime(DATE + ' ' + books['time'])
    books['mid_price'] = (books['bid1_px'] + books['ask1_px']) / 2

    res, trades, summary = run_backtest(books)
    fig = make_backtest_figure(res, trades, summary, html_path=None, market_trades=market_trades)
    fig.update_layout(title_text=f'{name.upper()} | ' + fig.layout.title.text)
    out = ROOT / html_name
    fig.write_html(out, include_plotlyjs='cdn', full_html=True,
                   config={'responsive': True})
    html = out.read_text(encoding='utf-8')
    html = html.replace('<head>', '<head><meta name="viewport" content="width=device-width, initial-scale=1">'
                        f'<title>Complex VWAP backtest - {name}</title>', 1)
    out.write_text(html, encoding='utf-8')

    print(f'\n=== {name} ===')
    for k, v in summary.items():
        print(f'{k:>15}: {float(v):.2f}')
    print(trades.to_string(index=False))
    print(f'-> {out}')
