# yycrawler_package

## 매경 인기뉴스 크롤링
-------------------

- 2시간 마다 업데이트 되는 매경 인기뉴스(https://www.mk.co.kr/news/bestclick/)를 크롤링한 후 DB에 저장하고 DB에서 HTML형태로 이메일로 자동발송하는 패키지입니다.

-------------------------------------------

### 패키지 구조

main.py : 메인 모듈

├── crawler : 크롤링 패키지
│   └── mknews_crw.py 
|
├── database : db저장 및 출력 후 데이터프레임화 패키지
│   └── dbTodf.py
|
├── processing : 데이터 전처리 패키지
│   └── save_html.py : 데이터프레임을 html로 저장
|
├── rpa : 자동화 패키지
│   ├── mail : 매2시간마다 이메일 자동전송
│   ├──   └── email_sender.py
│   └── messenger : 특정 카테고리별 인기뉴스 전송(진행중...)
└──        └── telegram.py


