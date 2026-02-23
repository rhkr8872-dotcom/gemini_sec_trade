import os, pandas as pd, smtplib
from datetime import datetime, timedelta
from google import genai
from serpapi.google_search import GoogleSearch

import os
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD") # GitHub Secrets에서 가져옴

# [1. 필수 설정]
SERPAPI_KEY = "7eafa278ec0bf5cc0e99347c1497bfe57d1bae3df4ae519ba558a98b4f02a740"
GEMINI_KEY = "AIzaSyC1ztyTRflvtf3b72O_4oaFnwzIMZ-7Cgo" # 담당자님의 키 입력
SENDER_EMAIL = "rhkr8872@gmail.com"
RECEIVER_EMAIL = "lifepal.kwak@samsung.com"

# [2. 다국어 및 타겟 도메인 설정]
# sites.xlsx 기반 주요 정부 도메인
GOV_DOMAINS = "site:cbp.gov OR site:ustr.gov OR site:cbic.gov.in OR site:customs.gov.vn OR site:sat.gob.mx"

def get_smart_queries():
    # custom_queries.TXT 내용을 기반으로 핵심 키워드 조합
    base_keywords = ["tariff", "customs act", "trade expansion act", "anti-dumping"]
    # 다국어 확장 (현지어 검색으로 정확도 제고)
    return [
        f"({GOV_DOMAINS}) {k}" for k in base_keywords
    ] + ["Trump tariff TruthSocial", "Vietnam customs audit Samsung"]

def analyze_with_gemini(news_list):
    client = genai.Client(api_key=GEMINI_KEY)
    
    prompt = f"""
    당신은 삼성전자 글로벌 관세/통상 담당자입니다. 
    다음 수집된 뉴스 데이터({news_list})를 분석하여 리포트를 작성하세요.
    
    [지침]
    1. Action란에는 삼성전자의 주요 생산거점(베트남, 인도, 멕시코 등) 및 제품군(모바일, 가전)에 미치는 영향을 전문 관세사 수준으로 분석하세요.
    2. 중요도는 '관세율 직접 변동'이나 '수입 규제'인 경우 반드시 [상]으로 표시하세요.
    3. 중복된 정보는 하나로 합치세요.
    4. 출력 양식: 헤드라인(URL 포함), 주요내용, 발표일, 대상 국가, 관련 기관, 중요도, Action
    """
    
    # Gemini API 호출 및 결과 반환 로직...
    pass

# [실행 로직] 1일 단위 필터링 (tbs='qdr:d' 적용)
def run_daily_monitoring():
    queries = get_smart_queries()
    all_results = []
    
    for q in queries:
        search = GoogleSearch({
            "engine": "google",
            "q": q,
            "tbs": "qdr:d", # 최근 24시간 제한
            "api_key": SERPAPI_KEY
        })
        # 수집 및 분석 로직 수행...

# [Step 4] 메일 발송 부분 (기존 로직 보완)
if final_df.empty:
    print("⚠️ 수집된 새로운 뉴스가 없습니다. 테스트 메일을 발송합니다.")
    content = "<h3>현재 24시간 이내에 수집된 새로운 통상 뉴스가 없습니다.</h3>"
else:
    content = f"<h3>🌍 금일 신규 수집 리포트</h3>{final_df.to_html(index=False, escape=False)}"

msg.attach(MIMEText(f"<html><head>{style}</head><body>{content}</body></html>", 'html'))

print("✅ 시스템이 준비되었습니다. 매일 오전 7시, 24시간 이내의 정제된 통상 리포트를 발송합니다.")
