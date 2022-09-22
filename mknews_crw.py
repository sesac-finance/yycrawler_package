#크롤링 모듈만들기
import requests
from bs4 import BeautifulSoup


url='https://www.mk.co.kr/news/bestclick/'
res=requests.get(url)

soup=BeautifulSoup(res.content.decode('euc-kr', 'replace'),'html.parser')


#카테고리별로 12개 인기뉴스 페이지 가져오기
#크롤링 함수 만들기
#for문으로 120개 기사 가져오는 동안 id_num으로 인덱스 120개 만들기
def best_To_Tuple()->bool:
  
  
  '''

  크롤링 결과를 출력하는 함수
   : DB저장을 위해 튜플로 반환 [(),()...]
  ---------------------------------------

  crawling_date : 크롤링한 날짜(%Y%m%d%H%M)

  category_url_decode :  12개의 뉴스 카테고리
  (뉴스종합, 경제, 기업, 사회, 국제, 부동산,
   증권, 정치, IT과학, 문화, 연예, 스포츠)  

   ranking: 순위 (1~10위) 

   title : 기사제목
   
   top10_url : 뉴스기사 링크

   register_date : '등록일' 뉴스기사 등록일

  -------------------------------------



  '''

  #columns = ['추출일시','카테고리','순위','기사제목','본문요약','url','img_url','등록일']

  top10_categories = ['%B4%BA%BD%BA%C1%BE%C7%D5','%B0%E6%C1%A6','%B1%E2%BE%F7','%BB%E7%C8%B8','%B1%B9%C1%A6','%BA%CE%B5%BF%BB%EA','%C1%F5%B1%C7',
                      '%C1%A4%C4%A1','IT%B0%FA%C7%D0','%B9%AE%C8%AD','%BF%AC%BF%B9','%BD%BA%C6%F7%C3%F7']

  

  result=[]
  for i in range(12):
      main_url='https://www.mk.co.kr/news/bestclick.php?BCC='
      category_url=top10_categories[i]
      tot_category_url=main_url+category_url
      res=requests.get(tot_category_url)
      soup=BeautifulSoup(res.content.decode('euc-kr', 'replace'),'html.parser')
      top10_news= soup.select(".article_list")
      #여러 파일 요청시 파일명 중복 가능->크롤링한 날짜 및 시간 받아오기
      date=soup.select_one('#datepicker')['value'] #str


  #인기뉴스 10개씩 가져오기
      ranking=0 #순위 기본값 지정
      for news in top10_news:
        title= news.select_one(" dt").text #기사 제목
        description=news.select_one(".desc").text.strip()#기사내용
        top10_url=news.select_one(".tit a")['href'] #기사 url
        register_date=news.select_one('.desc .date').text.strip()#기사 등록일
        #1~10 순위 ranking(int) 생성
        ranking+=1

        if top10_url.startswith('http'):
          top10_url=top10_url
        else :
          top10_url='http:'+top10_url

      
      
        #카테고리 url 디코딩
        #url 디코딩
        from urllib import parse                  
        category_url_decode=parse.unquote(category_url,encoding='euc-kr')#디코딩  

     

        #오늘날짜,시간활용해서 추출일시 추출(2시간마다 실시간 인기뉴스 변동되므로)
        from datetime import datetime
        today_date=datetime.today()
        crawling_date=today_date.strftime('%Y%m%d%H%M')

        temp=(ranking, crawling_date,category_url_decode,title,top10_url,register_date)
        result.append(temp)
        
          

       

  print('크롤링 성공!')
  print('크롤링한 날짜는 '+ crawling_date +' 입니다.')
 

  return result

if __name__=='__main_ _':
  best_To_Tuple()