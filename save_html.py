#import pandas as pd

def df2html(news_top10):
    '''
    불러온 뉴스 데이터프레임{newsdb2df}의
    {news_top10}을 html으로 저장하는 함수

    뉴스기사 링크 활성화를 위해 escape문을 조정함(escape=False)
    '''

    news_top10['url'] = '<a target="_blank" href='+news_top10['url']+'>'+news_top10['url']+'</a>'
    news_top10.to_html('today_mk_Best.html',header=True, index=True, justify='right',border=2,escape=False) #정렬 및 열공간, 헤더, 인덱스 지정
    print('뉴스 데이터프레임 html으로 저장 성공!')
    

if __name__=='__main_ _':
  df2html(news_top10)
