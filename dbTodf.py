import pymysql

def newsdb2df(result)->bool:

    '''
    크롤링한 뉴스들{best_To_Tuple()}을 
    DB저장후 데이터프레임으로 출력하는 함수
    --------------------------------------
    iuput : best_To_Tuple(),튜플
    output : news_top10 ,데이터프레임
    '''


    try:
        connect=pymysql.connect(
        host='database-1.c9hqzj24v6v5.ap-northeast-2.rds.amazonaws.com',
        port=3306,
        user='yy',
        passwd=open(r'/home/ubuntu/workspace/config/newsdb_config','r').read().strip(),
        db='newsdb',
        charset='utf8mb4')

        print('DB 접속 성공')
        #테이블 생성
        # create table PK설정주의.
        try:
            with connect.cursor() as cursor:
                sql = '''CREATE TABLE MK_best (
                id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                ranking int,
                crawling_date varchar(20),
                category varchar(10),
                title varchar(300),
                url varchar(100),
                register_date varchar(20)
                )
                '''
                cursor.execute(sql)
                connect.commit()


        except:
            print('테이블 생성 실패')


        
        try:

            with connect.cursor() as cursor:

                sql = "insert into MK_best(ranking,crawling_date,category,title,url,register_date) values(%s,%s,%s,%s,%s,%s)" #       
                cursor.executemany(sql,result) #       

                connect.commit()
                #cursor.close() #db연결해제
                print('db insert 성공!')

        except Exception as e:
            print(e)

        #db조회 최신순으로 가져오기 위해 id 기준으로 desc정렬 후 120개 가져오기
        #데이터 프레임으로 가져오기
        try:
            import pandas as pd
            from datetime import datetime
            print('START TIME : ',str(datetime.now())[10:19] )
            #with connect.cursor() as cursor:
        
                
            news_top10_temp=pd.read_sql('SELECT * FROM MK_best ORDER BY id DESC LIMIT 120',connect)
            # 데이터 프레임 재 정렬후 html화 https://wikidocs.net/159534
            news_top10=news_top10_temp.sort_values(['id','ranking'],ascending=True)
            news_top10=news_top10.reset_index()
            print('END TIME : ',str(datetime.now())[10:19] )
            print('데이터 불러오기 성공')
            connect.close()
                
            
        except Exception as e:
            print(e)
            print('False')
        



    except Exception as e:
            print(e)
            print('DB 접속 실패')

    return news_top10

if __name__=='__main_ _':
  newsdb2df(best_To_Tuple())