from email.mime.multipart import MIMEMultipart # # 메일의 Data 영역의 메시지를 만드는 모듈 
from email.mime.text import MIMEText #이메일 본문내용 넣는 모듈
from email.mime.base import MIMEBase #첨부파일(pdf,csv,xlsx등)보내는 모듈

#mime : 전자우편을 위한 인터넷 표준 포멧(multipurpose internet mail extensions)
from email import encoders #이메일 인코딩
from os.path import basename #첨부파일 경로에서 파일제목 str로 뽑기 

import smtplib#smtp서버 접속해서 이메일보내는 파이썬 라이브러리



#발신인 기본 정보 설정
SMTP_SERVER='smtp.naver.com' #smtp.gmail.com : port 465
SMTP_PORT=465
SMTP_USER='tinggunj@naver.com'
SMTP_PASSWORD=open(r'/home/ubuntu/workspace/config/email_config','r').read().strip()

#이메일 발송 함수
def send_mail(from_user:str,to_users:list,subject:str,
content:str,attachments:list=[],cc_targets=[])->bool:
#->bool : 함수구현시 함수리턴값의 타입 명시(참고 : https://sosoeasy.tistory.com/487)
    '''

메일 발송 함수
**best10_To_Excel()함수 활용시,
    파일경로에 크롤링날짜'%Y%m%d%H%M' 입력

form_user : 발신인
to_users : 수신인(들)->list
subject: 메일제목
content : 메일내용
attachments : 첨부파일(들),첨부파일 경로->list
cc_targets : 참조 이메일 주소들->list

   '''
    try:
        #이메일 전송 서버 접속
        #SSL 465, (참고:https://itstory1592.tistory.com/30)
        smtp=smtplib.SMTP_SSL(SMTP_SERVER,SMTP_PORT)
        print("메일 전송 서버 접속 성공!")
        #내 이메일 로그인
        smtp.login(SMTP_USER,SMTP_PASSWORD)
        print("로그인 성공!")

        #편지봉투 만들기
        #실제 수신인들이랑 맞춰주기!
        msg=MIMEMultipart('alternative') #텍스트만 포함

        #첨부파일이 여부에 따른 값들
        #true : 1, ['result.xlsx'],'a'
        #false : 0,[],'' (빈값출력)
        if attachments:
            msg=MIMEMultipart('mixed') #텍스트+첨부파일
            
            for attachment in attachments:
                #파일을 담을 공간생성
                # 인스턴스 생성 시 내용 포맷/내용 형식(maintype/subtype)지정
                #  application/octet-stream은 모든 이진파일 첨부가능! 
                email_file=MIMEBase('application','octet-stream')

                #첨부파일 읽어오기(rb : 바이너리형식)
                with open(attachment,'rb') as f:
                    file_data=f.read()

                #읽어온 파일데이터를 첨부파일 공간에 넣기
                email_file.set_payload(file_data)

                #첨부파일 공간  base64로 인코딩
                encoders.encode_base64(email_file)
                #파일 제목만 가져오기
                file_name=basename(attachment)

                #첨부파일 정보를 헤더로 첨부
                '''
                Content-Disposition : 컨텐츠가 브라우저에 inline 되어야 하는 웹페이지 자체이거나 웹페이지의 일부인지, 아니면 attachment로써 다운로드 되거나 로컬에 저장될 용도록 쓰이는 것인지를 알려주는 헤더
                attachment : 반드시 다운로드 받아야 하며 대부분의 브라우저는 'Save as'(새이름으로저장) 창을 보여줌
                filename :  메일 수신자에서 설정되는 파일 이름
                '''
                email_file.add_header('Content-Disposition','attachment',
                filename=file_name)

                msg.attach(email_file)#첨부파일 이메일에 붙이기

        #이메일본문
        msg['From']=from_user
        msg['To']=','.join(to_users) #,기준으로 여러명
        #참조있을경우
        if cc_targets:
            msg['CC']=','.join(cc_targets)
        msg['Subject']=subject

        #편지지를 봉투에 담기
        text=MIMEText(content)
        msg.attach(text)

        #sendmail함수('발신인','수신인',msg.as_string())
        smtp.sendmail(from_user,','.join(to_users+cc_targets),
        msg.as_string())

        print('이메일 발송 성공!')

        return True #함수 빠져나옴, 이메일 발송 성공시

    #에러발생시
    except Exception as e:
        print('error!')
        print(e)
    finally:
        #에러상관없이 무조건 실행할 코드
        #서버연결 해제
        smtp.close()
        print('finish!')


    return False #함수 빠져나옴, 이메일 발송 실패시print(send_mail(parameters))하면 true or flase 출력


if __name__=='__main__':
    send_mail('tinggunj@naver.com',['tinggunj@gmail.com','tinggunj@naver.com'],
    subject='제목입니당', content='내용입니당',
    attachments=[r'C:\Users\shcho\Desktop\윤영\sesac\project1_crawring\2022.09.19_매경 카테고리별 top10 기사 크롤링.xlsx'])



