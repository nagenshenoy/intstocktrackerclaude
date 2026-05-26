from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import numpy as np
import time
import os

app = Flask(__name__)
CORS(app)

PUBLIC_DIR = os.path.join(os.path.dirname(__file__), '..', 'public')

@app.route('/')
def index():
    return send_from_directory(PUBLIC_DIR, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(PUBLIC_DIR, filename)

# ─── STOCK UNIVERSES ────────────────────────────────────────────────────

STOCKS_AI = {
    "Data Center Operators": {
        "Airtel":              "BHARTIARTL.NS",
        "Lodha Developers":    "LODHA.NS",
        "Adani Enterprises":   "ADANIENT.NS",
        "Techno Electric":     "TECHNOE.NS",
        "TCS":                 "TCS.NS",
        "Reliance":            "RELIANCE.NS",
    },
    "Power & Electrical": {
        "Schneider Electric":  "SCHNEIDER.NS",
        "Hitachi Energy":      "POWERINDIA.NS",
        "CG Power":            "CGPOWER.NS",
        "Cummins India":       "CUMMINSIND.NS",
        "GE Power India":      "GVPIL.NS",
        "GE Vernova T&D":      "GVT&D.NS",
        "Apar Industries":     "APARINDS.NS",
        "TD Power Systems":    "TDPOWERSYS.NS",
        "MTAR Technologies":   "MTARTECH.NS",
    },
    "Cooling": {
        "Aeroflex Industries":         "AEROFLEX.NS",
        "KRN Heat Exchanger":          "KRN.NS",
        "Dee Development Engineers":   "DEEDEV.NS",
        "Voltas":                      "VOLTAS.NS",
        "Amber Enterprises":           "AMBER.NS",
        "Blue Star":                   "BLUESTARCO.NS",
    },
    "Fiber / Networking": {
        "Sterlite Technologies":  "STLTECH.NS",
        "HFCL":                   "HFCL.NS",
        "Finolex Cables":         "FINCABLES.NS",
        "Bharti Hexacom":         "BHARTIHEXA.NS",
        "Precision Wires":        "PRECWIRE.NS",
    },
    "Compute & Hardware": {
        "Netweb Technologies": "NETWEB.NS",
        "E2E Networks":        "E2E.NS",
    },
    "Managed Services": {
        "Dynacons Systems": "DSSL.NS",
        "Black Box":        "BBOX.NS",
    },
    "Building / Construction": {
        "Interarch Building": "INTERARCH.NS",
        "Welspun Corp":       "WELCORP.NS",
        "L&T":                "LT.NS",
    },
}

STOCKS_EV = {
    "EV OEMs & 3W/Bus Manufacturers": {
        "Tata Motors Ltd":          "TMCV.NS",
        "Ashok Leyland Ltd":        "ASHOKLEY.NS",
        "Olectra Greentech Ltd":    "OLECTRA.NS",
        "JBM Auto Ltd":             "JBMA.NS",
        "Mahindra & Mahindra Ltd":  "M&M.NS",
        "Hero MotoCorp Ltd":        "HEROMOTOCO.NS",
        "Bajaj Auto Ltd":           "BAJAJ-AUTO.NS",
        "TVS Motor Company Ltd":    "TVSMOTOR.NS",
    },
    "EV Components & Technology": {
        "Bosch Ltd":                        "BOSCHLTD.NS",
        "Samvardhana Motherson":            "MOTHERSON.NS",
        "Exide Industries Ltd":             "EXIDEIND.NS",
        "Amara Raja Energy & Mobility":     "ARE&M.NS",
        "Sundram Fasteners":                "SUNDRMFAST.NS",
        "CG Power & Industrial Solutions":  "CGPOWER.NS",
        "Bharat Electronics Ltd":           "BEL.NS",
    },
    "EV Charging & Energy Infrastructure": {
        "Tata Power Co Ltd":      "TATAPOWER.NS",
        "Servotech Power Systems": "SERVOTECH.NS",
        "Reliance Industries Ltd": "RELIANCE.NS",
        "NTPC Ltd":               "NTPC.NS",
        "Indian Oil Corporation": "IOC.NS",
        "ABB India Ltd":          "ABB.NS",
        "Siemens Ltd":            "SIEMENS.NS",
        "Exicom Tele-Systems":    "EXICOM.NS",
    },
}

STOCKS_ENERGY = {
    "Oil Gas & Consumable Fuels": {
        "Reliance Industries":            "RELIANCE.NS",
        "Indian Oil Corporation":         "IOC.NS",
        "Bharat Petroleum Corporation":   "BPCL.NS",
        "Hindustan Petroleum Corporation":"HINDPETRO.NS",
        "Oil & Natural Gas Corporation":  "ONGC.NS",
        "Oil India":                      "OIL.NS",
        "GAIL (India)":                   "GAIL.NS",
        "Petronet LNG":                   "PETRONET.NS",
        "Gujarat State Petronet":         "GSPL.NS",
        "Indraprastha Gas":               "IGL.NS",
        "Mahanagar Gas":                  "MGL.NS",
        "Gujarat Gas":                    "GUJGASLTD.NS",
        "Adani Total Gas":                "ATGL.NS",
        "Aegis Logistics":                "AEGISLOG.NS",
        "Castrol India":                  "CASTROLIND.NS",
        "Coal India":                     "COALINDIA.NS",
    },
    "Power": {
        "NTPC":                      "NTPC.NS",
        "NTPC Green Energy":         "NTPCGREEN.NS",
        "Power Grid Corporation":    "POWERGRID.NS",
        "Adani Power":               "ADANIPOWER.NS",
        "Tata Power":                "TATAPOWER.NS",
        "JSW Energy":                "JSWENERGY.NS",
        "Adani Energy Solutions":    "ADANIENSOL.NS",
        "Adani Green Energy":        "ADANIGREEN.NS",
        "NHPC":                      "NHPC.NS",
        "NLC India":                 "NLCINDIA.NS",
        "SJVN":                      "SJVN.NS",
        "Torrent Power":             "TORNTPOWER.NS",
        "CESC":                      "CESC.NS",
        "Reliance Power":            "RPOWER.NS",
        "Jaiprakash Power Ventures": "JPPOWER.NS",
        "PTC India":                 "PTC.NS",
        "REC Ltd":                   "RECLTD.NS",
    },
    "Power & Electrical Equipment": {
        "Bharat Heavy Electricals": "BHEL.NS",
        "Siemens":                  "SIEMENS.NS",
        "Siemens Energy India":     "ENRIN.NS",
        "GE Vernova T&D":           "GVT&D.NS",
        "Hitachi Energy India":     "POWERINDIA.NS",
        "Inox Wind":                "INOXWIND.NS",
        "Suzlon Energy":            "SUZLON.NS",
        "Thermax":                  "THERMAX.NS",
    },
    "Renewable & Green Energy": {
        "Adani Green Energy":               "ADANIGREEN.NS",
        "Adani Energy Solutions":           "ADANIENSOL.NS",
        "Inox Wind":                        "INOXWIND.NS",
        "KPI Green Energy":                 "KPIGREEN.NS",
        "ACME Solar Holdings":              "ACMESOLAR.NS",
        "Clean Max Enviro Energy Solutions": "CLEAN.NS",
        "Inox Green Energy Services":       "INOXGREEN.NS",
        "RattanIndia Power":                "RTNPOWER.NS",
    },
}

STOCKS_DEFENCE = {
    "Aerospace & Aircraft Manufacturing": {
        "Hindustan Aeronautics": "HAL.NS",
        "Data Patterns":         "DATAPATTNS.NS",
        "Paras Defence":         "PARAS.NS",
        "Unimech Aerospace":     "UNIMECH.NS",
        "Dynamatic Technologies":"DYNAMATECH.NS",
        "ideaForge":             "IDEAFORGE.NS",
    },
    "Shipbuilding & Naval Systems": {
        "Mazagon Dock":               "MAZDOCK.NS",
        "Cochin Shipyard":            "COCHINSHIP.NS",
        "Garden Reach Shipbuilders":  "GRSE.NS",
    },
    "Missiles, Weapons & Ammunition": {
        "Bharat Dynamics":      "BDL.NS",
        "Solar Industries":     "SOLARINDS.NS",
        "Premier Explosives":   "PREMEXPLN.NS",
    },
    "Defence Electronics, Radars & Components": {
        "Bharat Electronics":   "BEL.NS",
        "Astra Microwave":      "ASTRAMICRO.NS",
        "Zen Technologies":     "ZENTEC.NS",
        "MTAR Technologies":    "MTARTECH.NS",
        "Avantel":              "AVANTEL.NS",
        "Axiscades":            "AXISCADES.NS",
        "Apollo Micro Systems": "APOLLO.NS",
        "Mishra Dhatu Nigam":   "MIDHANI.NS",
        "Cyient DLM":           "CYIENTDLM.NS",
        "Rossell Techsys":      "ROSSTECH.NS",
        "CFF Fluid Control":    "CFF.BO",
        "BEML":                 "BEML.NS",
        "Bharat Forge":         "BHARATFORG.NS",
        "Kaynes Technology":    "KAYNES.NS",
        "Sika Interplant":      "SIKA.NS",
        "Krishna Defence":      "KRISHNADEF.NS",
        "Rossell India":        "ROSSELLIND.NS",
    },
}

STOCKS_PHARMA = {
    "Large-cap branded pharma": {
        "Sun Pharmaceutical Industries": "SUNPHARMA.NS",
        "Dr. Reddy's Laboratories":      "DRREDDY.NS",
        "Cipla":                         "CIPLA.NS",
        "Torrent Pharmaceuticals":       "TORNTPHARM.NS",
        "Lupin":                         "LUPIN.NS",
        "Aurobindo Pharma":              "AUROPHARMA.NS",
        "Zydus Lifesciences":            "ZYDUSLIFE.NS",
        "Mankind Pharma":                "MANKIND.NS",
        "Alkem Laboratories":            "ALKEM.NS",
        "Glenmark Pharmaceuticals":      "GLENMARK.NS",
    },
    "Specialty and export-focused pharma": {
        "Divi's Laboratories":        "DIVISLAB.NS",
        "Laurus Labs":                "LAURUSLABS.NS",
        "Ipca Laboratories":          "IPCALAB.NS",
        "Natco Pharma":               "NATCOPHARM.NS",
        "Alembic Pharmaceuticals":    "APLLTD.NS",
        "Shilpa Medicare":            "SHILPAMED.NS",
        "Ajanta Pharma":              "AJANTPHARM.NS",
        "FDC":                        "FDC.NS",
        "Suven Pharmaceuticals":      "SUVEN.NS",
    },
    "Formulation and domestic-focused pharma": {
        "Abbott India":                      "ABBOTINDIA.NS",
        "JB Chemicals & Pharmaceuticals":    "JBCHEPHARM.NS",
        "GlaxoSmithKline Pharmaceuticals":   "GLAXO.NS",
        "Pfizer":                            "PFIZER.NS",
        "AstraZeneca Pharma India":          "ASTRAZEN.NS",
        "Sanofi India":                      "SANOFI.NS",
    },
    "Biotechnology and biosimilars": {
        "Biocon":           "BIOCON.NS",
        "Anthem Biosciences":"ANTHEM.NS",
        "Panacea Biotec":   "PANACEABIO.NS",
        "Wockhardt":        "WOCKPHARMA.NS",
    },
    "API and bulk drug companies": {
        "Aarti Drugs":                       "AARTIDRUGS.NS",
        "IOL Chemicals and Pharmaceuticals": "IOLCP.NS",
        "Dishman Carbogen Amcis":            "DCAL.NS",
        "NGL Fine-Chem":                     "NGLFINE.NS",
    },
    "Smaller pharma allied companies": {
        "SMS Pharmaceuticals":     "SMSPHARMA.NS",
        "Supriya Lifescience":     "SUPRIYA.NS",
        "Marksans Pharma":         "MARKSANS.NS",
        "Kopran":                  "KOPRAN.NS",
        "Caplin Point Laboratories":"CAPLIPOINT.NS",
        "Granules India":          "GRANULES.NS",
    },
}

ALL_STOCKS = {
    "ai":      STOCKS_AI,
    "ev":      STOCKS_EV,
    "energy":  STOCKS_ENERGY,
    "defence": STOCKS_DEFENCE,
    "pharma":  STOCKS_PHARMA,
}

# ─── HELPERS ────────────────────────────────────────────────────────────

def build_ticker_map(stocks_dict):
    ticker_map, all_tickers = {}, []
    for sector, stocks in stocks_dict.items():
        for name, ticker in stocks.items():
            if ticker not in ticker_map:
                ticker_map[ticker] = (name, sector)
                all_tickers.append(ticker)
    return ticker_map, all_tickers

_cache = {}
CACHE_TTL = 60

def get_cached(key):
    if key in _cache:
        data, ts = _cache[key]
        if time.time() - ts < CACHE_TTL:
            return data
    return None

def set_cached(key, data):
    _cache[key] = (data, time.time())

def safe_val(val, default=None):
    if val is None:
        return default
    try:
        if isinstance(val, float) and (np.isnan(val) or np.isinf(val)):
            return default
        return val
    except Exception:
        return default

def get_tracker_id(req):
    t = req.args.get('tracker', 'ai')
    if t == 'en':
        t = 'energy'
    return t if t in ALL_STOCKS else 'ai'

# ─── API ROUTES ─────────────────────────────────────────────────────────

@app.route('/api/quotes')
def get_quotes():
    tracker = get_tracker_id(request)
    cache_key = f'quotes_{tracker}'
    cached = get_cached(cache_key)
    if cached:
        return jsonify(cached)

    stocks_dict = ALL_STOCKS[tracker]
    ticker_map, all_tickers = build_ticker_map(stocks_dict)
    results = []
    try:
        tickers_obj = yf.Tickers(' '.join(all_tickers))
        for ticker in all_tickers:
            try:
                name, sector = ticker_map[ticker]
                info = tickers_obj.tickers[ticker].info
                fast = tickers_obj.tickers[ticker].fast_info

                def fi(attr):
                    try:
                        return getattr(fast, attr, None)
                    except Exception:
                        return None

                price      = safe_val(fi('last_price')   or info.get('currentPrice')              or info.get('regularMarketPrice'))
                prev_close = safe_val(fi('previous_close') or info.get('previousClose')           or info.get('regularMarketPreviousClose'))
                change     = round(price - prev_close, 2)              if price and prev_close else None
                change_pct = round((change / prev_close) * 100, 2)     if change and prev_close else None

                results.append({
                    "name": name, "ticker": ticker, "sector": sector,
                    "price":      safe_val(price),
                    "change":     safe_val(change),
                    "change_pct": safe_val(change_pct),
                    "open":       safe_val(fi('open')      or info.get('open')      or info.get('regularMarketOpen')),
                    "high":       safe_val(fi('day_high')  or info.get('dayHigh')   or info.get('regularMarketDayHigh')),
                    "low":        safe_val(fi('day_low')   or info.get('dayLow')    or info.get('regularMarketDayLow')),
                    "volume":     safe_val(fi('three_month_average_volume') or info.get('volume') or info.get('regularMarketVolume')),
                    "market_cap": safe_val(fi('market_cap') or info.get('marketCap')),
                    "pe_ratio":   safe_val(info.get('trailingPE') or info.get('forwardPE')),
                    "week52_high":safe_val(fi('year_high') or info.get('fiftyTwoWeekHigh')),
                    "week52_low": safe_val(fi('year_low')  or info.get('fiftyTwoWeekLow')),
                    "beta":       safe_val(info.get('beta')),
                })
            except Exception as e:
                name, sector = ticker_map.get(ticker, (ticker, 'Unknown'))
                results.append({
                    "name": name, "ticker": ticker, "sector": sector,
                    "price": None, "change": None, "change_pct": None,
                    "open": None, "high": None, "low": None,
                    "volume": None, "market_cap": None, "pe_ratio": None,
                    "week52_high": None, "week52_low": None, "beta": None,
                    "error": str(e),
                })
    except Exception as e:
        return jsonify({"error": str(e), "data": results}), 500

    set_cached(cache_key, results)
    return jsonify(results)


@app.route('/api/history')
def get_history():
    ticker = request.args.get('ticker', '')
    period = request.args.get('period', '1mo')
    if period not in ['1d', '5d', '1mo', '3mo', '1y']:
        period = '1mo'
    cache_key = f'history_{ticker}_{period}'
    cached = get_cached(cache_key)
    if cached:
        return jsonify(cached)
    try:
        interval = '5m' if period == '1d' else '1d'
        hist = yf.Ticker(ticker).history(period=period, interval=interval)
        data = []
        for idx, row in hist.iterrows():
            data.append({
                "date":   str(idx.date() if period != '1d' else idx),
                "open":   safe_val(row.get('Open')),
                "high":   safe_val(row.get('High')),
                "low":    safe_val(row.get('Low')),
                "close":  safe_val(row.get('Close')),
                "volume": safe_val(row.get('Volume')),
            })
        result = {"ticker": ticker, "period": period, "data": data}
        set_cached(cache_key, result)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e), "ticker": ticker, "period": period, "data": []}), 500


@app.route('/api/sparklines')
def get_sparklines():
    tracker = get_tracker_id(request)
    cache_key = f'sparklines_{tracker}'
    cached = get_cached(cache_key)
    if cached:
        return jsonify(cached)
    stocks_dict = ALL_STOCKS[tracker]
    _, all_tickers = build_ticker_map(stocks_dict)
    result = {}
    try:
        hist = yf.download(
            ' '.join(all_tickers), period='7d', interval='1d',
            group_by='ticker', auto_adjust=True, progress=False,
        )
        for ticker in all_tickers:
            try:
                closes = (hist['Close'].dropna() if len(all_tickers) == 1
                          else hist[ticker]['Close'].dropna())
                result[ticker] = [round(c, 2) for c in closes.tolist()]
            except Exception:
                result[ticker] = []
    except Exception:
        for ticker in all_tickers:
            result[ticker] = []
    set_cached(cache_key, result)
    return jsonify(result)


@app.route('/api/sector-heatmap')
def get_sector_heatmap():
    tracker = get_tracker_id(request)
    cache_key = f'sector_heatmap_{tracker}'
    cached = get_cached(cache_key)
    if cached:
        return jsonify(cached)
    stocks_dict = ALL_STOCKS[tracker]
    ticker_map, all_tickers = build_ticker_map(stocks_dict)
    results = []
    try:
        hist = yf.download(
            ' '.join(all_tickers), period='1y', interval='1d',
            group_by='ticker', auto_adjust=True, progress=False,
        )
        single = len(all_tickers) == 1
        sector_tickers = {}
        for ticker, (name, sector) in ticker_map.items():
            sector_tickers.setdefault(sector, []).append(ticker)

        for sector, tickers in sorted(sector_tickers.items()):
            rets = {'1d': [], '1w': [], '1m': [], '1y': []}
            for ticker in tickers:
                try:
                    closes = (hist['Close'].dropna() if single
                              else hist[ticker]['Close'].dropna())
                    if len(closes) < 2:
                        continue
                    price = float(closes.iloc[-1])

                    def pct(n):
                        if len(closes) > n:
                            base = float(closes.iloc[-(n + 1)])
                            if base > 0:
                                return (price - base) / base * 100
                        return None

                    r1y = (pct(252) if len(closes) >= 252
                           else ((price - float(closes.iloc[0])) / float(closes.iloc[0]) * 100
                                 if len(closes) > 1 else None))
                    for key, val in zip(['1d','1w','1m','1y'], [pct(1), pct(5), pct(21), r1y]):
                        if val is not None:
                            rets[key].append(val)
                except Exception:
                    pass

            def avg(lst):
                return round(sum(lst) / len(lst), 1) if lst else None

            results.append({
                'sector': sector, 'count': len(tickers),
                'ret_1d': avg(rets['1d']), 'ret_1w': avg(rets['1w']),
                'ret_1m': avg(rets['1m']), 'ret_1y': avg(rets['1y']),
            })
    except Exception as e:
        return jsonify({'error': str(e), 'data': results}), 500
    set_cached(cache_key, results)
    return jsonify(results)


@app.route('/api/screener')
def get_screener():
    tracker = get_tracker_id(request)
    cache_key = f'screener_{tracker}'
    cached = get_cached(cache_key)
    if cached:
        return jsonify(cached)
    stocks_dict = ALL_STOCKS[tracker]
    ticker_map, all_tickers = build_ticker_map(stocks_dict)
    results = []
    try:
        hist = yf.download(
            ' '.join(all_tickers), period='1y', interval='1d',
            group_by='ticker', auto_adjust=True, progress=False,
        )
        single = len(all_tickers) == 1
        for ticker in all_tickers:
            try:
                name, sector = ticker_map[ticker]
                closes = (hist['Close'].dropna() if single
                          else hist[ticker]['Close'].dropna())
                if len(closes) < 2:
                    raise ValueError("Not enough data")
                price = float(closes.iloc[-1])

                def pct_return(n):
                    if len(closes) > n:
                        base = float(closes.iloc[-(n + 1)])
                        if base > 0:
                            return round((price - base) / base * 100, 2)
                    return None

                r1y = (pct_return(252) if len(closes) >= 252
                       else (round((price - float(closes.iloc[0])) / float(closes.iloc[0]) * 100, 2)
                             if len(closes) > 1 else None))
                results.append({
                    "name": name, "ticker": ticker, "sector": sector,
                    "price": round(price, 2),
                    "ret_1d": pct_return(1), "ret_1w": pct_return(5),
                    "ret_1m": pct_return(21), "ret_1y": r1y,
                })
            except Exception as e:
                name, sector = ticker_map.get(ticker, (ticker, 'Unknown'))
                results.append({
                    "name": name, "ticker": ticker, "sector": sector,
                    "price": None, "ret_1d": None, "ret_1w": None,
                    "ret_1m": None, "ret_1y": None, "error": str(e),
                })
    except Exception as e:
        return jsonify({"error": str(e), "data": results}), 500
    set_cached(cache_key, results)
    return jsonify(results)


@app.route('/api/health')
def health():
    return jsonify({
        "status":   "ok",
        "trackers": list(ALL_STOCKS.keys()),
        "counts":   {k: sum(len(v) for v in d.values()) for k, d in ALL_STOCKS.items()},
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
