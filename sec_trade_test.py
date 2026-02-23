import os, pandas as pd, smtplib, traceback
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# [GitHub Secrets에서 환경 변수 로드]
# 로컬 실행 시에는 시스템 환경 변수에 등록하거나 직접 입력이 필요합니다.
MY_SERPAPI_KEY = os.getenv("MY_SERPAPI_KEY")
MY_GEMINI_KEY = os.getenv("MY_GEMINI_KEY")
SENDER_EMAIL = "rhkr8872@gmail.com"
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD") # 중요: 앱 비밀번호(16자리)
RECEIVER_EMAIL = "lifepal.kwak@samsung.com"

def send_mail(final_df):
    # 환경 변수 체크 로직 추가 (로그 확인용)
    if not SENDER_PASSWORD:
        raise ValueError("❌ 에러: SENDER_PASSWORD 환경 변수가 설정되지 않았습니다. GitHub Secrets를 확인하세요.")

    msg = MIMEMultipart()
    msg['Subject'] = f"🌍 [최신확정] 글로벌 통상 리포트 [{datetime.now().strftime('%Y-%m-%d')}]"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    # 데이터가 없을 경우에도 '정상 작동 중'임을 알리기 위해 발송
    if final_df.empty:
        html_content = "<h3>현재 24시간 이내에 수집된 새로운 통상 뉴스가 없습니다. 시스템은 정상 가동 중입니다.</h3>"
    else:
        style = "<style>table{border-collapse:collapse; width:100%; font-size:11px;} th{background:#2E75B6; color:white; padding:10px;} td{padding:8px; border:1px solid #ddd;}</style>"
        html_content = f"<html><head>{style}</head><body><h3>🌍 금일 신규 수집 리포트</h3>{final_df.to_html(index=False, escape=False)}</body></html>"

    msg.attach(MIMEText(html_content, 'html'))

    # SMTP 설정 (GitHub Runner 최적화)
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_mail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
            print("✅ 메일 발송 성공!")
    except Exception as e:
        print(f"❌ 메일 발송 실패: {e}")
        traceback.print_exc()
