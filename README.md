# India Stock Tracker Suite

Unified NSE/BSE dashboard with four integrated stock trackers — AI & Data Center, EV, Energy, and Defence & Aerospace — in a single-page app with collapsible sidebar navigation.

## Trackers

| Tracker | Accent | Stocks | Exchange |
|---|---|---|---|
| 🤖 AI & Data Center | Cyan `#00d4ff` | 30 | NSE |
| ⚡ EV Stocks | Green `#00e87a` | 23 | NSE |
| 🛢 Energy Stocks | Amber `#ffb347` | 45 | NSE |
| 🛡 Defence & Aerospace | Violet `#c084fc` | 29 | NSE/BSE |

## Features

- **Collapsible sidebar** — switch between all 4 trackers; collapses to icon-only with tooltips
- **Per-tracker accent theming** — header bar, tabs, badges, and charts all update on switch
- **Live KPI strip** — total stocks, gainers, losers, top mover per tracker
- **Sector filter tabs** — filter the stock table by sub-sector
- **Full stock table** — sortable by any column; sparkline 7-day trend per row
- **Sector performance cards** — avg change, top/bottom stock per sector
- **Sector heatmap** — 1D / 1W / 1M / 1Y mean returns per sector, sortable
- **Stock screener** — multi-period return heatmap table, sortable
- **Stock detail modal** — price chart (1D/5D/1M/3M/1Y), metrics, NSE link
- **Dark / Light theme** — persisted in localStorage
- **Lazy loading** — each tracker loads on first visit, cached 60s
- **Market status** — NSE open/closed indicator with IST clock

## Project Structure

```
integrated-tracker/
├── api/
│   └── index.py       # Unified Flask API — all 4 trackers via ?tracker=ai|ev|en|defence
├── public/
│   └── index.html     # Complete single-page application
├── requirements.txt
├── vercel.json        # Vercel v2 — Python serverless + static
└── README.md
```

## Local Development

```bash
pip install -r requirements.txt
python api/index.py
# Open http://localhost:5000
```

## Deploy to Vercel

```bash
npm i -g vercel
cd integrated-tracker
vercel --prod
```

## API Reference

All endpoints accept `?tracker=ai|ev|en|defence` (default: `ai`).

| Endpoint | Description |
|---|---|
| `GET /api/quotes?tracker=defence` | Real-time quotes for all stocks |
| `GET /api/sparklines?tracker=ev` | 7-day sparkline prices |
| `GET /api/sector-heatmap?tracker=energy` | Sector returns 1D/1W/1M/1Y |
| `GET /api/screener?tracker=ai` | Multi-period return screener |
| `GET /api/history?ticker=HAL.NS&period=1mo` | OHLCV price history |
| `GET /api/health` | Service health + stock counts |

> Data via Yahoo Finance. Prices delayed ~15 min. Not investment advice.
