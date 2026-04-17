import requests

# === 설정 구간 ===
# 아까 복사한 디스코드 웹훅 URL을 이 따옴표 안에 붙여넣으세요.
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1494625729680379914/G__vhSOno09uQ7xtO5pry4LvB3cCNLAV5pBEqYqsFhCMEu5bGqG2O5L4-H_T44Xyl14P"

def send_discord_message(content):
    if not DISCORD_WEBHOOK_URL or "여기에" in DISCORD_WEBHOOK_URL:
        print("디스코드 웹훅 URL이 설정되지 않았습니다.")
        return

    # 디스코드로 보낼 데이터 형식
    payload = {"content": content}
    
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("디스코드 메시지 전송 성공!")
        else:
            print(f"전송 실패 (상태 코드: {response.status_code})")
    except Exception as e:
        print(f"에러 발생: {e}")

def get_liquidation_data():
    """바이낸스에서 비트코인(BTC) 청산 데이터를 가져옵니다."""
    url = "https://fapi.binance.com/fapi/v1/allForceOrders"
    params = {"symbol": "BTCUSDT"}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if not data:
            return "최근 큰 청산 내역이 없습니다."

        # 최신 청산 3개만 정리해서 메시지 작성
        recent_orders = data[-3:]
        msg = "🔔 **바이낸스 BTC 청산 알림** 🔔\n"
        
        for order in recent_orders:
            side = "🟢 LONG" if order['side'] == 'SELL' else "🔴 SHORT"
            price = float(order['price'])
            qty = float(order['origQty'])
            usd = price * qty
            
            # 1,000달러 이상일 때만 한 줄 추가
            if usd >= 1000:
                msg += f"> **{side}** | 가격: ${price:,.2f} | 규모: **${usd:,.2f}**\n"
        
        return msg
    except:
        return "데이터를 가져오는 중 오류가 발생했습니다."

if __name__ == "__main__":
    print("분석 중...")
    message = get_liquidation_data()
    send_discord_message(message)
