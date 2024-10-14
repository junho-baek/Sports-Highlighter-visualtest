import streamlit as st
import pandas as pd
import time
import random
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정 (Mac 사용자는 AppleGothic, Windows/Linux 사용자는 NanumGothic)
plt.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

# 제목 설정
st.title('실시간 축구 경기 반응 및 키워드 분석')

# 빈 데이터프레임 생성
df = pd.DataFrame(columns=["시간", "반응"])

# 실시간으로 데이터를 업데이트하는 함수
def update_data():
    # 반응 리스트 (실시간 반응 예시)
    response = ["헐", "000 미쳤다", "Wow", "넣은듯?", "안 잔 보람이 있다."]
    
    # 난수를 이용해 리스트에서 반응 선택
    response_count = random.randint(0, len(response) - 1)
    response_count2 = random.randint(50, 100)
    new_data = {
        "시간": [time.strftime("%Y-%m-%d %H:%M:%S")],
        "반응": response[response_count],
        "반응 수"  : [response_count2] # 선택된 반응
    }
    new_df = pd.DataFrame(new_data)
    
    return new_df

# 키워드 추출 (예시)
keywords = ["골", "환호", "위기", "득점", "슈팅"]
keyword_counts = {keyword: 0 for keyword in keywords}

# Streamlit에서 실시간 업데이트
placeholder = st.empty()
chart_placeholder = st.empty()
pie_chart_placeholder = st.empty()

start_time = time.time()

# 실시간 데이터를 시각화할 동안의 타임테이블 업데이트
while True:
    # 실시간 데이터 업데이트
    new_df = update_data()
    df = pd.concat([df, new_df], ignore_index=True)

    # 난수 기반으로 키워드 업데이트 (여기서는 단순 예시)
    keyword = random.choice(keywords)
    keyword_counts[keyword] += 1  # 해당 키워드에 대한 카운트 증가

    # 플로우 차트 (시간대별 반응 수 라인 차트)
    fig, ax = plt.subplots()
    sns.lineplot(x=df["시간"], y=df["반응 수"], ax=ax)  # df.index를 사용하여 x축의 순서에 따른 변화를 표현
    ax.set_title('시간대별 실시간 반응 수')
    ax.set_xticklabels(df["시간"], rotation=45, ha="right")
    ax.set_xlabel('시간')
    ax.set_ylabel('반응 수')

    # 원형 차트 (키워드 반응 수 파이 차트)
    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(keyword_counts.values(), labels=keyword_counts.keys(), autopct='%1.1f%%', startangle=90)
    ax_pie.set_title('실시간 키워드 반응 비율')

    # 데이터 출력 및 차트 업데이트
    with placeholder.container():
        st.write(df)

    with chart_placeholder.container():
        st.pyplot(fig)

    with pie_chart_placeholder.container():
        st.pyplot(fig_pie)

    time.sleep(5)