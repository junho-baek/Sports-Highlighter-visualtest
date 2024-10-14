import re
import pandas as pd
from datetime import datetime
import pytz

# 한국(KST) 시간을 UTC로 변환하는 함수
def convert_kst_to_utc(date_str):
    # 문자열을 datetime 객체로 변환 (날짜 형식: %d.%m. %H:%M)
    kst_time = datetime.strptime(date_str, "%d.%m. %H:%M")

    # 현재 연도를 추가해 정확한 날짜로 변환 (기본적으로 현재 연도로 설정)
    current_year = datetime.now().year
    kst_time = kst_time.replace(year=current_year)

    # 한국 표준시(KST) 타임존 설정
    kst = pytz.timezone('Asia/Seoul')

    # KST 타임존으로 변환
    kst_aware_time = kst.localize(kst_time)

    # UTC로 변환
    utc_time = kst_aware_time.astimezone(pytz.utc)

    # 반환할 값: KST 시간과 UTC 시간 모두 반환
    return kst_aware_time, utc_time

# 파일을 한 줄씩 읽어오는 함수
def process_schedule_file_with_timezones(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    dates = []
    teams = []
    kst_times = []
    utc_times = []
    
    # 날짜와 시간을 추출하는 정규 표현식
    date_time_regex = re.compile(r'(\d{2}\.\d{2}\.\s\d{2}:\d{2})')

    for line in lines:
        line = line.strip()

        # '라운드'나 '-'가 포함된 줄은 무시
        if '라운드' in line or line == '-':
            continue

        # 날짜를 찾으면 저장하고 KST 및 UTC 시간 변환
        if date_time_regex.match(line):
            date_str = line
            dates.append(date_str)

            # KST 및 UTC로 변환
            kst_time, utc_time = convert_kst_to_utc(date_str)
            kst_times.append(kst_time)
            utc_times.append(utc_time)

        # 팀 이름이 중복되어 있는 경우 처리
        else:
            if len(teams) > 0 and teams[-1] == line:
                continue  # 중복된 팀 이름은 무시
            teams.append(line)

    # 두 팀씩 짝지어 리스트로 변환
    team_pairs = [teams[i:i+2] for i in range(0, len(teams), 2)]

    # 날짜 수에 맞게 팀 매칭
    df = pd.DataFrame(team_pairs[:len(dates)], columns=['Team 1', 'Team 2'])
    df['Date'] = dates
    df['KST Time'] = kst_times
    df['UTC Time'] = utc_times

    return df

# 파일 경로를 설정하고 실행
file_path = '경기일정.txt'
df_schedule = process_schedule_file_with_timezones(file_path)

# CSV로 저장
df_schedule.to_csv('epl_schedule_with_timezones.csv', index=False)

# 데이터 확인 (옵션)
print(df_schedule.head())