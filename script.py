import requests
import time

# === 설정 구간 ===
# 텔레그램 봇이 없다면 우선 비워두고 실행해도 됩니다. 
# 알림을 받고 싶다면 토큰과 ID를 입력하세요.
TELEGRAM_TOKEN = "" 
CHAT_ID = ""

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print(f"텔레그램 설정이 없습니다. 출력만 합니다:\n{message}")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message})
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")

def get_liquidation_data():
    """바이낸스에서 최근 청산 데이터를 가져오는 함수"""
    # 바이낸스 선물 API 주소
    url = "https://fapi.binance.com/fapi/v1/allForceOrders"
    params = {"symbol": "BTCUSDT"} # BTC 기준 (다른 코인도 가능)
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if not data:
            return "최근 5분간 큰 청산 내역이 없습니다."

        # 최신 청산 5개만 정리
        recent_orders = data[-5:]
        msg = "🔥 [바이낸스 실시간 청산 리포트] 🔥\n"
        
        for order in recent_orders:
            side = "LONG 🟢" if order['side'] == 'SELL' else "SHORT 🔴"
            price = float(order['price'])
            quantity = float(order['origQty'])
            total_usd = price * quantity
            
            # 1,000달러 이상의 청산만 기록
            if total_usd > 1000:
                msg += f"\n포지션: {side}\n가격: ${price:,.2f}\n규모: ${total_usd:,.2f}\n"
        
        return msg

    except Exception as e:
        return f"데이터 가져오기 실패: {e}"

if __name__ == "__main__":
    print("데이터 분석 시작...")
    report = get_liquidation_data()
    send_telegram_message(report)
    print("작업 완료!")
