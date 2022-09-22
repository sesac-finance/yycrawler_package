import schedule
import time

#매경 최근 2시간이내 기준, 인기뉴스 크롤링
from mknews_crw import best_To_Tuple
#best_To_Tuple() #return result : 리스트안 튜플값
btt=best_To_Tuple()
#크롤링 결과 db저장 후 df생성
from dbTodf import newsdb2df 
newsdb2df(btt)#return news_top10 :데이터프레임

#df을 html 로 로컬에 저장 
from save_html import df2html
news=newsdb2df(btt)
df2html(news)

#HTML->이메일 전송
from email_sender import send_mail 
RPA_MAIL=send_mail('tinggunj@naver.com',['tinggunj@gmail.com','tinggunj@naver.com'],
    subject='[오늘의 인기뉴스]', content='최근 2시간이내 인기뉴스 목록입니다.',
    attachments=[r'C:\Users\shcho\Desktop\윤영\sesac\project1_crawring\final\today_mk_Best.html'])
#schedule.every(2).hour.do(RPA_MAIL)


