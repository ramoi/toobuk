# TOOBUK
beautifulsoup을 이용하여 웹 크롤링을 쉽게할 수 있도록 도와주는 모듈입니다.  
소스에서 웹페이지 접속 정보와 html에서 읽어올 selector(css selector이며, jquery가 익숙한 분들은 $함수에서 사용하던 바로 그것입니다.) 정보를 설정정보로 따로 분리하는 것입니다.
때문에, 추후 URL이 바뀌거나 html이 바뀌면 해당 부분을 설정 파일에서 간단히 수정하면 되는거죠.

## 차례
1. [맛보기](#맛보기)
   1. [설치](#설치)
   1. [소스 작성](#소스-작성)
1. [상세 기능](#상세-기능)
1. [docker](#docker)
1. [남은 것들](#남은-것들)


## 맛보기 
   일단 간단하게 설치를 해보시죠.  

   ### 설치

toobuk은 기본적으로 beautifulsoup4, requests 를 이용합니다.   

      pip install beautifulsoup4  
      pip install requests

toobuk을 설치합니다.
      
      pip install toobuk

설치 여부 확인  

      pip list  

   ### 소스 작성
   아래를 임의의 이름으로 저장합니다. 확장자는 json으로 
   저는 test.json으로 저장하겠습니다.

    {
    "housetrade" : {
                "url" : "https://www.index.go.kr/unity/potal/eNara/sub/showStblGams3.do?stts_cd=124001&idx_cd=1240&freq=Y&period=N",
                "output" : {
                            "date" : {    "type" : "list",
                                       "pattern" : [ 
                                                    {
                                                        "selector" : "#t_Table_124001 thead > tr:nth-of-type(1) > th",
                                                        "name" : "DATE"
                                                    }
                                                   ]
                                         }
                            }
                    }
    }

그리고 test.json이 저장된 디렉토리에 역시 test.py로 아래 소스를 저장합니다.

    from toobuk import Toobuk

    htb = Toobuk('test') #설정 파일 test.json, .json은 생략
    print( htb.grumble('housetrade') ) 

그리고 콘솔을 열어서 아래 명령을 실행합니다.

    python test.py

결과는 아래와 같습니다.

     {'date': [{'DATE': '\xa0'}, {'DATE': '202304월'}, {'DATE': '202305월'}, {'DATE': '202306월'}, {'DATE': '202307월'}, {'DATE': '202308월'}, {'DATE': '202309월'}, {'DATE': '202310월'}, {'DATE': '202311월'}, {'DATE': '202312월'}, {'DATE': '202401월'}, {'DATE': '202402월'}, {'DATE': '202403월'}]}

물론 여기서 끝이 아닙니다.  
좀 더 많은 정보를 해당 페이지에서 뽑아올 수 있으며, 뽑아온 데이타를 가공할 수도 있습니다.  
페이징 처리된 url에서 데이타를 뽑아올 수도 있으며, selenium을 이용할 수도 있습니다.  
위에 내용은 그저 맛보기일 뿐입니다.

## 상세 기능
좀 더 상세한 기능에 대한 정보는 아래에서 확인할 수 있습니다. 직접 소스를 확인하며 실행해보세요.  

https://github.com/ramoi/toobuk_test

## docker
혹시, 서비스 내용을 확인하고 싶다면 docker를 설치 후, 아래 내용을 확인해 보세요.  

장고와 연동된 소스입니다.    
https://github.com/ramoi/toobuk_vued3 

콘솔에서 아래 명령어로 확인할 수 있습니다.

      PS D:\> docker pull ramoi/toobuk:0.1 
      PS D:\> docker run -d -p 8000:5000 ramoi/toobuk:0.1

브라우져 접속 
http://127.0.0.1:8000


실제 업무에서느 이렇게 쓰진 않겠지요. 빅데이타의 최전방 보명으로 쓰던지, 아니면 데이타베이스에 저장하겠지요.  
그리고 더 중요한 것은 이 놈 보다 더 좋은 라이브러리가 많을 겁니다.  
제가 자바를 주력 언어로 사용해서 파이썬 생태계를 잘 모르지만 아마 많은 고수분들이 만드신게 있을 듯 합니다

## 남은 것들
처음에는 python을 공부하면서, 무언가를 하나 만들어보면서 다지려는 마음이었습니다.  
그런데 여기까지 왔네요.  
많이 부족하지만 누군가에게(python을 처음 공부하는 분들이면 좋겠네요) 조금이라도 도움이 되었다면 하는 바램입니다.
