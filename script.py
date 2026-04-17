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
    """바이낸스에서 데이터를 가져오며, 202 에러 발생 시 재시도합니다."""
    url = "https://fapi1.binance.com/fapi/v1/allForceOrders"
    params = {"symbol": "BTCUSDT"}
    
    # 최대 3번까지 다시 시도합니다.
    for i in range(3):
        try:
            response = requests.get(url, params=params, timeout=10)
            
            # 202 에러일 경우: 잠시 쉬었다가 다시 시도
            if response.status_code == 202:
                print(f"⚠️ 데이터 준비 중(202)... {i+1}번째 재시도 중입니다.")
                time.sleep(2) # 2초 대기
                continue
                
            if response.status_code != 200:
                return f"❌ API 오류 (코드: {response.status_code})\n{response.text}"
            
            data = response.json()
            if not data:
                return "✅ 현재 큰 청산 내역이 없습니다."

            # 데이터 가공
            recent_orders = data[-3:]
            msg = "🔔 **바이낸스 실시간 청산 리포트** 🔔\n"
            for order in recent_orders:
                side = "🟢 LONG" if order['side'] == 'SELL' else "🔴 SHORT"
                price = float(order['price'])
                qty = float(order['origQty'])
                usd = price * qty
                msg += f"> **{side}** | 가격: ${price:,.2f} | 규모: **${usd:,.2f}**\n"
            
            return msg

        except Exception as e:
            return f"❌ 실행 중 에러 발생: {str(e)}"
            
    return "❌ 3번 시도했으나 데이터가 준비되지 않았습니다. (202 지속)"

    except Exception as e:
        # 어떤 에러인지 정확히 출력하게 함
        return f"❌ 실행 중 에러 발생: {str(e)}"

if __name__ == "__main__":
    print("🚀 분석 시작...")
    result_message = get_liquidation_data()
    print(result_message) # GitHub Actions 로그에서 확인용
    send_discord_message(result_message)
