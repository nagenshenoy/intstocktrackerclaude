# India Stock Tracker Suite

An integrated dashboard combining three NSE stock trackers — AI & Data Center, EV, and Energy — in a unified interface with a collapsible sidebar panel for switching between them.

## Features

- **Unified sidebar navigation** — switch between AI/DC, EV, and Energy trackers with one click
- **Per-tracker accent colors** — Cyan (AI/DC), Green (EV), Amber (Energy)  
- **All three full tracker experiences**: KPI strip, stock table, sector cards, heatmap, screener
- **Lazy loading** — each tracker loads on first visit
- **Collapsible sidebar** with tooltips in collapsed mode
- **Light/Dark theme toggle** with localStorage persistence
- **Header tracker switcher** as a quick-access shortcut
- Fully deployable on Vercel

## Structure

```
integrated-tracker/
├── api/
│   └── index.py          # Unified Flask API (all 3 trackers, ?tracker=ai|ev|energy)
├── public/
│   └── index.html        # Single-page integrated app
├── requirements.txt
├── vercel.json
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
vercel --prod
```

## API Endpoints

All endpoints accept `?tracker=ai|ev|energy` (default: `ai`).

- `GET /api/quotes?tracker=ev` — Real-time quotes
- `GET /api/sparklines?tracker=energy` — 7-day sparkline data
- `GET /api/sector-heatmap?tracker=ai` — Sector heatmap (1D/1W/1M/1Y)
- `GET /api/screener?tracker=ev` — Multi-period screener
- `GET /api/history?ticker=TCS.NS&period=1mo` — Price history for charts
- `GET /api/health` — Health check

## Disclaimer

For informational purposes only. Not investment advice. Data via Yahoo Finance (~15 min delayed).
