from tradingview_ta import TA_Handler, Interval
from PIL import Image
from datetime import datetime
import random, io, requests, pytz


def get_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

kyiv_timezone = pytz.timezone("Europe/Kyiv")

def get_photo(symbol, timeframe):
    api_key = "bc1Q2bnJRs1ghPz7Qc7YF1iIJyhmEPzE5KhO53wx"
    url = "https://api.chart-img.com/v2/tradingview/advanced-chart"
    headers = {
        "x-api-key": api_key,
        "content-type": "application/json"
    }
    data = {
        "height": 1280,
        "width": 1920,
        "theme": "dark",
        "interval": "4h",
        "symbol": f"FX:{symbol}",
        "studies": [
            {
                "name": "Donchian Channels",
                "input": {
                    "in_0": 20
                },
                "override": {
                    "Lower.visible": True,
                    "Lower.linewidth": 1,
                    "Lower.plottype": "line",
                    "Lower.color": "rgb(33,150,243)",
                    "Upper.visible": True,
                    "Upper.linewidth": 1,
                    "Upper.plottype": "line",
                    "Upper.color": "rgb(33,150,243)",
                    "Basis.visible": True,
                    "Basis.linewidth": 1,
                    "Basis.plottype": "line",
                    "Basis.color": "rgb(255,109,0)",
                    "Plots Background.visible": True,
                    "Plots Background.color": "rgba(33,150,243,0.1)"
                }
            },
            {
                "name": "Volume Profile Visible Range",
                "override": {
                    "graphics.horizlines.pocLines.color": "rgb(0,0,255)"
                }
            },
            {
                "name": "Relative Strength Index"
            },
            {
                "name": "MA with EMA Cross"
            }
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200 and response.headers['Content-Type'].startswith('image'):
        return response.content
    else:
        print("❌ Помилка запиту:", response.status_code, response.text)
        raise ValueError(f"Не вдалося отримати зображення. Статус: {response.status_code}")





def get_photos(symbol, timeframe):

    photo = Image.open(io.BytesIO(get_photo(symbol, timeframe)))

    modified_photo_bytesio = io.BytesIO()
    photo.save(modified_photo_bytesio, format='PNG')

    modified_photo_bytesio.seek(0)
    return modified_photo_bytesio



def get_data(symbol, timeframe):
    match timeframe:
        case '1m':
            INTERVAL = Interval.INTERVAL_1_MINUTE
        case '5m':
            INTERVAL = Interval.INTERVAL_5_MINUTES
        case '15m':
            INTERVAL = Interval.INTERVAL_15_MINUTES
        case '30m':
            INTERVAL = Interval.INTERVAL_30_MINUTES
        case '1h':
            INTERVAL = Interval.INTERVAL_1_HOUR
    try:
        output = TA_Handler(
            symbol=symbol,
            screener="forex",
            exchange="FX_IDC",
            interval=INTERVAL,
        )

            # отримуємо аналіз
        activity = output.get_analysis()
        if not activity:
            raise ValueError("Порожній об’єкт activity")

        price = activity.indicators
        analysis = activity.summary
        return analysis, price

    except Exception as e:
        raise ValueError(f"Помилка отримання даних для {symbol}: {str(e)}")

