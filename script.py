import requests

# === 설정 구간 ===
# 아까 복사한 디스코드 웹훅 URL을 이 따옴표 안에 붙여넣으세요.
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1494625729680379914/G__vhSOno09uQ7xtO5pry4LvB3cCNLAV5pBEqYqsFhCMEu5bGqG2O5L4-H_T44Xyl14P"

def send_discord_message(content):
    if not DISCORD_WEBHOOK_URL or "여기에" in DISCORD_WEBHOOK_URL:
        print("디스코드 웹훅 URL이 설정되지 않았습니다.")
        return
    payload = {"content": content}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

def get_liquidation_data():
    """바이낸스에서 데이터를 가져오고 에러를 상세히 출력합니다."""
    url = "https://fapi1.binance.com/fapi/v1/allForceOrders"
    params = {"symbol": "BTCUSDT"}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        # 1. 응답 코드가 200(성공)이 아닐 경우
        if response.status_code != 200:
            return f"❌ 바이낸스 API 연결 실패 (코드: {response.status_code})\n이유: {response.text}"
        
        data = response.json()
        
        # 2. 데이터가 비어있는 리스트인 경우
        if not data:
            return "✅ 현재 바이낸스에 최근 청산 내역이 없습니다. (시장이 평온합니다)"

        # 3. 데이터 정리
        recent_orders = data[-5:] # 최신 5개
        msg = "🔔 **바이낸스 BTC 청산 리포트** 🔔\n"
        
        count = 0
        for order in recent_orders:
            side = "🟢 LONG" if order['side'] == 'SELL' else "🔴 SHORT"
            price = float(order['price'])
            qty = float(order['origQty'])
            usd = price * qty
            
            # 테스트를 위해 기준을 $100로 낮췄습니다. 잘 나오면 나중에 올리세요.
            if usd >= 100: 
                msg += f"> **{side}** | 가격: ${price:,.2f} | 규모: **${usd:,.2f}**\n"
                count += 1
        
        return msg if count > 0 else "✅ 최근 $100 이상의 큰 청산은 없습니다."

    except Exception as e:
        # 어떤 에러인지 정확히 출력하게 함
        return f"❌ 실행 중 에러 발생: {str(e)}"

if __name__ == "__main__":
    print("🚀 분석 시작...")
    result_message = get_liquidation_data()
    print(result_message) # GitHub Actions 로그에서 확인용
    send_discord_message(result_message)
