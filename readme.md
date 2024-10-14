# 시각화 테스트

streamlit 으로 간단하게 프로젝트 시각화를 했습니다. 반응을 시간별로 볼 수 있고, 플로우차트로 반응 튀는걸 볼 수 있고, 원형 차트로 키워드 분석을 하는 예시입니다.

```
pipenv shell
pipenv install
streamlit run visual.py
```

# 경기일정

> (여기)[https://www.flashscore.co.kr/soccer/england/premier-league/fixtures/ ]
> 에서 긁어서 경기일정.txt에 넣고 schedule.py에 csv 파일 만들어집니다. 이제 이 데이터로 자동화를 해야하는데. 지금은 airflow를 생각하고 있고.. 경기 시작 10분 전부터 넉넉하게 120 분 정도 api 호출을 해야할거 같은데 api 무료플랜으로 실시간성이 보장될지는.. 모르겠네요. 크롤링도 고려!

```
pipenv shell
python schedule.py
```
