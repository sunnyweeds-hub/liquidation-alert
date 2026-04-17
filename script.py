import requests

# === 설정 구간 ===
# 아까 복사한 디스코드 웹훅 URL을 이 따옴표 안에 붙여넣으세요.
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1494625729680379914/G__vhSOno09uQ7xtO5pry4LvB3cCNLAV5pBEqYqsFhCMEu5bGqG2O5L4-H_T44Xyl14P"

def send_discord_message(content):
    if not DISCORD_WEBHOOK_URL or "여기에" in DISCORD_WEBHOOK_URL:
        print("디스코드 웹훅 URL이 설정되지 않았습니다.")
        return
    payload = {"content": content}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"디스코드 전송 중 에러: {e}")

def get_liquidation_data():
    """바이낸스에서 데이터를 가져오며, 202 에러 발생 시 재시도합니다."""
    # 451 에러를 피하기 위해 fapi1 주소를 사용합니다.
    url = "https://fapi1.binance.com/fapi/v1/allForceOrders"
    params = {"symbol": "BTCUSDT"}
    
    for i in range(3):
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 202:
                print(f"⚠️ 데이터 준비 중(202)... {i+1}번째 재시도 중")
                time.sleep(2)
                continue
                
            if response.status_code != 200:
                return f"❌ API 오류 (코드: {response.status_code})"
            
            data = response.json()
            if not data:
                return "✅ 현재 큰 청산 내역이 없습니다."

            recent_orders = data[-3:]
            msg = "🔔 **바이낸스 BTC 청산 리포트** 🔔\n"
            for order in recent_orders:
                side = "🟢 LONG" if order['side'] == 'SELL' else "🔴 SHORT"
                price = float(order['price'])
                qty = float(order['origQty'])
                usd = price * qty
                msg += f"> **{side}** | 가격: ${price:,.2f} | 규모: **${usd:,.2f}**\n"
            return msg

        except Exception as e:
            return f"❌ 실행 중 에러 발생: {str(e)}"
            
    return "❌ 데이터 응답 대기 시간 초과 (202 지속)"

if __name__ == "__main__":
    print("🚀 분석 시작...")
    result_message = get_liquidation_data()
    print(result_message)
    send_discord_message(result_message)
    print("✨ 작업 완료")
