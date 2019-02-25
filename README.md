# TOOBUK
beautifulsoup을 이용하여 웹 크롤링을 쉽게할 수 있도록 도와주는 모듈입니다.

## 차례
1. [설치](#설치)
1. [간단한 설명](#간단한-설명)
1. [가장 기본적인 사용법](#가장-기본적인-사용법)
1. [output 설정](#output-설정)
	1. [output 조정하기](#output-조정하기)
	1. [output이 여러개 설정된 경우](#output이-여러개-설정된-경우)
	1. [output의 특정 그룹 하나 가져오기](#output의-특정-그룹-하나-가져오기)
	1. [output의 여러 그룹 가져오기](#output의-여러-그룹-가져오기)
	1. [output 전체 가져오기](#output-전체-가져오기)

1. [parameter 설정]([parameter-설정])
	1. [parameter 배열 설정 ](parameter-배열-설정 )
	1. [parameter 프로그램에서 넘기기 ](parameter-프로그램에서-넘기기)
1. [페이징 처리]([페이징-처리)
1. [list를 가져오는 다른 방법](#list를-가져오는-다른-방법)
1. [장고에서 사용해보기](#장고에서-사용해보기)
1. [남은 것들](#남은-것들)

## 간단한 설명 
beautifulsoup을 이용하여 웹 크롤링을 쉽게할 수 있도록 도와주는 모듈입니다.  
test/test.py를 실행하시면 콘솔을 통해 결과값을 확인할 수 있습니다.   

## 설치
python을 설치한 후 아래 명령으로 설치할 수 있습니다.  
pip install toobuk  

beautifulsoup4가 설치되지 안핬다면 설치해주시길 바랍니다.  
pip install beautifulsoup4  

설치 여부 확인  
pip list  

아래 설명하는 부분에서 test.py와 test.json을 참고하시면서 보시면 됩니다.  
예제는 [장고에서 사용해보기](#장고에서-사용해보기) 에서도 확인하실 수 있습니다.

## 가장 기본적인 사용법
아래와 같은 내용이 있습나다. 크롤링할 url과 bs.typ에서 사용하는 parser가 정의되어 있습니다.   
output으로 list를 뽑아내는 데, 뽑아내는 데이타는 selector에 정의되어 있습니다.   
selector에 대한 설명은 아래 url을 참고 하세요  

https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors  

	{
	"housetrade" : {
				"url" : "http://www.index.go.kr/potal/main/EachDtlPageDetail.do?idx_cd=1240",
				"bs.type" : "html.parser",
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

일단 위의 설정 파일을 test.json으로 저장합니다.  
그리고 test.json이 저장된 디렉토리에 역시 test.py로 아래 소스를 저장합니다.  

	from toobuk.tb import Toobuk

	htb = Toobuk('test') #설정 파일 test.json, .json은 생략
	print( htb.get('housetrade') ) 

그리고 콘솔을 열어서 아래 명령을 실행합니다.

	python test.py

결과는 아래와 같습니다.

	[{'DATE': '\xa0'}, {'DATE': '201802월'}, {'DATE': '201803월'}, {'DATE': '201804월'}, {'DATE': '201805월'}, {'DATE': '201806월'}, {'DATE': '201807월'}, {'DATE': '201808월'}, {'DATE': '201809월'}, {'DATE': '201810월'}, {'DATE': '201811월'}, {'DATE': '201812월'}, {'DATE': '201901월'}]

## output 설정

### output 조정하기

배열의 첫번째 값이 이상합니다.  
아래 그림이 위에서 url로 설정한 사이트를 캡쳐한 내용입니다. 테이블의 첫번째 th값이 비어있네요 저 th값을 빼고 가져와야할 듯 싶습니다.  
![캡쳐화면](https://user-images.githubusercontent.com/31053133/52697530-fd315c00-2fb4-11e9-9f64-9eec4a5a5cab.PNG)
그리고 데이타 형식으로 YYYY-MM으로 나왔으면 하구요.  

	{
	"housetrade" : {
				"url" : "http://www.index.go.kr/potal/main/EachDtlPageDetail.do?idx_cd=1240",
				"bs.type" : "html.parser",
				"output" : {
						    "date" : {    "type" : "list",
						               "pattern" : [ 
													{
														"selector" : "#t_Table_124001 thead > tr:nth-of-type(1) > th",
														"name" : "DATE",
														"slice" : {"start": 1 },
														"regx" : { "pattern" : "(?P<YYYY>\\d{4})(?P<MM>\\d{2})." , "replace" : "\\g<YYYY>-\\g<MM>" }
													}
												   ]
								         }
				}
	}


**slice**속성으로 첫번째 th부분을 제외했으며, **regx** 속성으로 포맷을 원하는 형태로 바꿨습니다.

	{'date': [{'DATE': '2018-02'}, {'DATE': '2018-03'}, {'DATE': '2018-04'}, {'DATE': '2018-05'}, {'DATE': '2018-06'}, {'DATE': '2018-07'}, {'DATE': '2018-08'}, {'DATE': '2018-09'}, {'DATE': '2018-10'}, {'DATE': '2018-11'}, {'DATE': '2018-12'}, {'DATE': '2019-01'}]}

그 밖에 형식을 지정할 수 있습니다. 지금은 int와 float만 지원됩니다. 
[output이 여러개 설정된 경우](#output이-여러개-설정된-경우)에서 확인하실 수 있습니다.

### output이 여러개 설정된 경우
웹 페이지를 긁어온 경우, 데이타가 여러개 설정이 될 수 있습니다. list가 하나가 될 수 있고, 두개도 될 수 있죠.  
리슽트가 아니라 일반 단일 형식이 또 있을 수 있습니다. 그 단일형식을 또 여러개로 나눌 수 있죠.  
output에 추가만 해주면 됩니다. 밑에 예제가 있습니다.


	{
	"housetrade" : {
				"url" : "http://www.index.go.kr/potal/main/EachDtlPageDetail.do?idx_cd=1240",
				"bs.type" : "html.parser",
				"output" : {
						    "date" : {    "type" : "list",
						               "pattern" : [ 
													{
														"selector" : "#t_Table_124001 thead > tr:nth-of-type(1) > th",
														"name" : "DATE",
														"slice" : {"start": 1 },
														"regx" : { "pattern" : "(?P<YYYY>\\d{4})(?P<MM>\\d{2})." , "replace" : "\\g<YYYY>-\\g<MM>" }
													}
												   ]
								         }, 
					"changeRate" : {     "type" : "list", 
										   "join" : { "ref" : "housecharter/changeRate", "joinKey" : ["DATE", "DATE"] },
										"pattern" : [
										 			{
														"selector" : "#t_Table_124001 thead > tr:nth-of-type(1) > th",
														"name" : "DATE",
														"slice" : {"start": 1 },
														"regx" : { "pattern" : "(?P<YYYY>\\d{4})(?P<MM>\\d{2})." , "replace" : "\\g<YYYY>\\g<MM>" },
														"type" : "int"
													}, {
														"selector" : "#t_Table_124001 tbody > tr:nth-of-type(1) > td", 
														"name" : "COUNTRY",
														"type" : "float"
													}, {
														"selector" : "#t_Table_124001 tbody > tr:nth-of-type(2) > td", 
														"name" : "CAPATIAL",
														"type" : "float"
													}, {
														"selector" : "#t_Table_124001 tbody > tr:nth-of-type(3) > td", 
														"name" : "SEOUL",
														"type" : "float"
													}, {
														"selector" : "#t_Table_124001 tbody > tr:nth-of-type(4) > td", 
														"name" : "SOUTH",
														"type" : "float"
													}, {
														"selector" : "#t_Table_124001 tbody > tr:nth-of-type(5) > td", 
														"name" : "NORTH",
														"type" : "float"
													}
													]

									}
							}
				}
		}

위에서는 output으로 date만 있었는데요.  changeRate가 하나더 생겼습니다. python코드는 아래와 같습니다.

	from toobuk.tb import Toobuk

	htb = Toobuk('test') #설정 파일 test.json, .json은 생략

아래는 결과입니다. 그룹명(date, changeRate)을 기준으로 데이타가 만들어졌습니다.

	{
		'date': [{'DATE': '2018-02'}, {'DATE': '2018-03'}, {'DATE': '2018-04'}, {'DATE': '2018-05'}, {'DATE': '2018-06'}, {'DATE': '2018-07'}, {'DATE': '2018-08'}, {'DATE': '2018-09'}, {'DATE': '2018-10'}, {'DATE': '2018-11'}, {'DATE': '2018-12'}, {'DATE': '2019-01'}], 

		'changeRate': [{'DATE': 201802, 'COUNTRY': 0.2, 'CAPATIAL': 0.5, 'SEOUL': 0.9, 'SOUTH': 1.2, 'NORTH': 0.7}, {'DATE': 201803, 'COUNTRY': 0.1, 'CAPATIAL': 0.3, 'SEOUL': 0.6, 'SOUTH': 0.6, 'NORTH': 0.6}, {'DATE': 201804, 'COUNTRY': 0.1, 'CAPATIAL': 0.2, 'SEOUL': 0.3, 'SOUTH': 0.3, 'NORTH': 0.3}, {'DATE': 201805, 'COUNTRY': 0.0, 'CAPATIAL': 0.1, 'SEOUL': 0.2, 'SOUTH': 0.2, 'NORTH': 0.3}, {'DATE': 201806, 'COUNTRY': 0.0, 'CAPATIAL': 0.1, 'SEOUL': 0.2, 'SOUTH': 0.1, 'NORTH': 0.4}, {'DATE': 201807, 'COUNTRY': 0.0, 'CAPATIAL': 0.1, 'SEOUL': 0.3, 'SOUTH': 0.3, 'NORTH': 0.4}, {'DATE': 201808, 'COUNTRY': 0.0, 'CAPATIAL': 0.2, 'SEOUL': 0.6, 'SOUTH': 0.6, 'NORTH': 0.6}, {'DATE': 201809, 'COUNTRY': 0.3, 'CAPATIAL': 0.7, 'SEOUL': 1.3, 'SOUTH': 1.5, 'NORTH': 1.0}, {'DATE': 201810, 'COUNTRY': 0.2, 'CAPATIAL': 0.4, 'SEOUL': 0.5, 'SOUTH': 0.5, 'NORTH': 0.6}, {'DATE': 201811, 'COUNTRY': 0.1, 'CAPATIAL': 0.3, 'SEOUL': 0.2, 'SOUTH': 0.1, 'NORTH': 0.3}, {'DATE': 201812, 'COUNTRY': 0.0, 'CAPATIAL': 0.1, 'SEOUL': 0.0, 'SOUTH': -0.1, 'NORTH': 0.2}, {'DATE': 201901, 'COUNTRY': -0.1, 'CAPATIAL': -0.1, 'SEOUL': -0.2, 'SOUTH': -0.3, 'NORTH': -0.1}]
	}
### output의 특정 그룹 하나 가져오기
	#output에서 설정한 값 중 date만 가져옵니다.
	print( htb.get('housetrade/date') ) 

### output의 여러 그룹 가져오기
	#output에서 설정한 그룹들을 여러개 가져올 수 있습니다.
	#&로 엮어서 가져오면 됩니다.
	print( htb.get('housetrade/date&changeRate') ) 

### output 전체 가져오기
	#output 전체를 가져옵니다.
	print( htb.get('housetrade') ) 

## parameter 설정
url의 parameter를 바꿔가면서 실행할 필요가 있겠지요. 방법은 2가지 입니다.

### parameter 배열 설정 
네이버나 다음에서 주식 정보를 가져오려고 할때 해당 url을 호출하면 됩니다.
네이버의 경우 주소는 아래와 같은데요  

https://finance.naver.com/item/sise_day.nhn?code=#code# 

위 링크에서 #code# 부분이 해당 주식의 코드정보가 들어갑니다. 저 부분을 변수처리하였으니, 해당값을 어디선가 설정해야하지요  
아래 보면 **parameter**속성이 있습니다.  
"code"라는 key값이 url의 #code#와 매칭이 됩니다. replace가 되는 것이지요

	{
	"stock" : {
				"url" : "https://finance.naver.com/item/sise_day.nhn?code=#code#",
				"bs.type" : "html.parser",
				"parameter" :  [{ "code" : "005930" },{"code" : "066570"}],
				"output" : {
							"stockList" : {   "type" : "list",
										   "pattern" : [	
															{
																"selector" : "table:nth-of-type(1) > tr > td:nth-of-type(1) > span.gray03",
																"name" : "DATE",
																"regx" : { "pattern" : "\\." , "replace" : "-" }
															}, {
																"selector" : "table:nth-of-type(1) > tr > td:nth-of-type(2) > span.p11", 
																"name" : "END_PRICE",
																"regx" : { "pattern" : "," , "replace" : "" },
																"type" : "int"
															}
														]
										}
							}
			}
	}

소스입니다.

	htb = Toobuk('test')
	resultData = htb.get('stock')
	print(resultData)

실행 시켜서 결과를 확인하겠습니다.  

	{'stockList': [
		{'code': '005930', 'data': [{'DATE': '2019-02-25', 'END_PRICE': 47350}, {'DATE': '2019-02-22', 'END_PRICE': 47150}, {'DATE': '2019-02-21', 'END_PRICE': 46950}, {'DATE': '2019-02-20', 'END_PRICE': 46900}, {'DATE': '2019-02-19', 'END_PRICE': 45950}, {'DATE': '2019-02-18', 'END_PRICE': 46200}, {'DATE': '2019-02-15', 'END_PRICE': 46050}, {'DATE': '2019-02-14', 'END_PRICE': 47500}, {'DATE': '2019-02-13', 'END_PRICE': 46200}, {'DATE': '2019-02-12', 'END_PRICE': 46050}]}, 

		{'code': '066570', 'data': [{'DATE': '2019-02-25', 'END_PRICE': 71300}, {'DATE': '2019-02-22', 'END_PRICE': 73200}, {'DATE': '2019-02-21', 'END_PRICE': 73000}, {'DATE': '2019-02-20', 'END_PRICE': 72700}, {'DATE': '2019-02-19', 'END_PRICE': 72300}, {'DATE': '2019-02-18', 'END_PRICE': 72000}, {'DATE': '2019-02-15', 'END_PRICE': 72000}, {'DATE': '2019-02-14', 'END_PRICE': 72300}, {'DATE': '2019-02-13', 'END_PRICE': 72100}, {'DATE': '2019-02-12', 'END_PRICE': 71900}]}
	]}

output의 그룹명인 stockList를 기준으로  parameter값이 들어가구요. data를 key로 해서 검색된 데이타가 만들어졌습니다.

### parameter 프로그램에서 넘기기
parameter값이 하나만 필요하다면 가장 단순한 방법은 아래처럼 url에서 code를 변수처리하지 않고 직접 넣어두는 것입니다.
"url" : "https://finance.naver.com/item/sise_day.nhn?code=005930"  

하지만 프로그램에서 셋팅할 수도 있습니다. 위의 소스를 수정해보죠..  

	resultData = htb.get('stock', {'code': '005490'})

결과는 아래와 같습니다. json에서 설정한 parameter는 무시하고 소스에서 인자로 호출한 code가 호출이되었습니다.

	{'stockList': {'code': '005490', 'data': [{'DATE': '2019-02-25', 'END_PRICE': 272500}, {'DATE': '2019-02-22', 'END_PRICE': 273000}, {'DATE': '2019-02-21', 'END_PRICE': 275500}, {'DATE': '2019-02-20', 'END_PRICE': 273500}, {'DATE': '2019-02-19', 'END_PRICE': 268500}, {'DATE': '2019-02-18', 'END_PRICE': 262500}, {'DATE': '2019-02-15', 'END_PRICE': 265500}, {'DATE': '2019-02-14', 'END_PRICE': 266500}, {'DATE': '2019-02-13', 'END_PRICE': 267000}, {'DATE': '2019-02-12', 'END_PRICE': 265500}]}}

## 페이징 처리 
https://finance.naver.com/item/sise_day.nhn?code=005930   
위 주소로 들어가보시면 페이징 처리된 주식정보가 보일겁니다.
페이징 처리된 데이타를 가져오겠습니다.

	{
	"stock" : {
				"url" : "https://finance.naver.com/item/sise_day.nhn?code=#code#&page=#page#",
				"bs.type" : "html.parser",
				"parameter" :  [{ "code" : "005930" },{"code" : "066570"}],
				"for" : { "type" : "number", "name" : "page", "start" : 1, "end": 2 },
				"output" : {
							"stockList" : {   "type" : "list",
										   "pattern" : [	
															{
																"selector" : "table:nth-of-type(1) > tr > td:nth-of-type(1) > span.gray03",
																"name" : "DATE",
																"regx" : { "pattern" : "\\." , "replace" : "-" }
															}, {
																"selector" : "table:nth-of-type(1) > tr > td:nth-of-type(2) > span.p11", 
																"name" : "END_PRICE",
																"regx" : { "pattern" : "," , "replace" : "" },
																"type" : "int"
															}
														]
										}
							}
			}
	}


stock 속성으로 **for**가 새로 설정되었습니다.  
  
for 속성 중 name이 page가 있네요. url에 #&page=#page#"가 추가되었습니다.  

	{'stockList': [
		{'code': '005930', 'data': [{'DATE': '2019-02-25', 'END_PRICE': 47300}, {'DATE': '2019-02-22', 'END_PRICE': 47150}, {'DATE': '2019-02-21', 'END_PRICE': 46950}, {'DATE': '2019-02-20', 'END_PRICE': 46900}, {'DATE': '2019-02-19', 'END_PRICE': 45950}, {'DATE': '2019-02-18', 'END_PRICE': 46200}, {'DATE': '2019-02-15', 'END_PRICE': 46050}, {'DATE': '2019-02-14', 'END_PRICE': 47500}, {'DATE': '2019-02-13', 'END_PRICE': 46200}, {'DATE': '2019-02-12', 'END_PRICE': 46050}, {'DATE': '2019-02-11', 'END_PRICE': 45000}, {'DATE': '2019-02-08', 'END_PRICE': 44800}, {'DATE': '2019-02-07', 'END_PRICE': 46200}, {'DATE': '2019-02-01', 'END_PRICE': 46350}, {'DATE': '2019-01-31', 'END_PRICE': 46150}, {'DATE': '2019-01-30', 'END_PRICE': 46400}, {'DATE': '2019-01-29', 'END_PRICE': 45500}, {'DATE': '2019-01-28', 'END_PRICE': 45050}, {'DATE': '2019-01-25', 'END_PRICE': 44750}, {'DATE': '2019-01-24', 'END_PRICE': 43050}]}, 
		{'code': '066570', 'data': [{'DATE': '2019-02-25', 'END_PRICE': 71100}, {'DATE': '2019-02-22', 'END_PRICE': 73200}, {'DATE': '2019-02-21', 'END_PRICE': 73000}, {'DATE': '2019-02-20', 'END_PRICE': 72700}, {'DATE': '2019-02-19', 'END_PRICE': 72300}, {'DATE': '2019-02-18', 'END_PRICE': 72000}, {'DATE': '2019-02-15', 'END_PRICE': 72000}, {'DATE': '2019-02-14', 'END_PRICE': 72300}, {'DATE': '2019-02-13', 'END_PRICE': 72100}, {'DATE': '2019-02-12', 'END_PRICE': 71900}, {'DATE': '2019-02-11', 'END_PRICE': 69300}, {'DATE': '2019-02-08', 'END_PRICE': 64800}, {'DATE': '2019-02-07', 'END_PRICE': 65900}, {'DATE': '2019-02-01', 'END_PRICE': 65400}, {'DATE': '2019-01-31', 'END_PRICE': 66600}, {'DATE': '2019-01-30', 'END_PRICE': 67600}, {'DATE': '2019-01-29', 'END_PRICE': 67400}, {'DATE': '2019-01-28', 'END_PRICE': 67700}, {'DATE': '2019-01-25', 'END_PRICE': 69500}, {'DATE': '2019-01-24', 'END_PRICE': 65200}]}
	]}

데이타가 좀 더 많아진 것 같습니다. for문이 잘 작동한 걸로 보여요  

## list를 가져오는 다른 방법
[output이 여러개 설정된 경우](#output이-여러개-설정된-경우) 내용울 다시 가져와서 확인해보겠습니다.

	{
	"housetrade" : {
				"url" : "http://www.index.go.kr/potal/main/EachDtlPageDetail.do?idx_cd=1240",
				"bs.type" : "html.parser",
				"output" : {
					"changeRate" : {     "type" : "list", 
										   "join" : { "ref" : "housecharter/changeRate", "joinKey" : ["DATE", "DATE"] },
										"pattern" : [
										 			{
														"selector" : "#t_Table_124001 thead > tr:nth-of-type(1) > th",
														"name" : "DATE",
														"slice" : {"start": 1 },
														"regx" : { "pattern" : "(?P<YYYY>\\d{4})(?P<MM>\\d{2})." , "replace" : "\\g<YYYY>\\g<MM>" },
														"type" : "int"
													}, {
														"selector" : "#t_Table_124001 tbody > tr:nth-of-type(1) > td", 
														"name" : "COUNTRY",
														"type" : "float"
													}, {
														"selector" : "#t_Table_124001 tbody > tr:nth-of-type(2) > td", 
														"name" : "CAPATIAL",
														"type" : "float"
													}, {
														"selector" : "#t_Table_124001 tbody > tr:nth-of-type(3) > td", 
														"name" : "SEOUL",
														"type" : "float"
													}, {
														"selector" : "#t_Table_124001 tbody > tr:nth-of-type(4) > td", 
														"name" : "SOUTH",
														"type" : "float"
													}, {
														"selector" : "#t_Table_124001 tbody > tr:nth-of-type(5) > td", 
														"name" : "NORTH",
														"type" : "float"
													}
													]

									}
							}
				}
		}

아래는 결과입니다.

	{'changeRate': [
		{'DATE': 201802, 'COUNTRY': 0.2, 'CAPATIAL': 0.5, 'SEOUL': 0.9, 'SOUTH': 1.2, 'NORTH': 0.7}, 
		{'DATE': 201803, 'COUNTRY': 0.1, 'CAPATIAL': 0.3, 'SEOUL': 0.6, 'SOUTH': 0.6, 'NORTH': 0.6}, 
		{'DATE': 201804, 'COUNTRY': 0.1, 'CAPATIAL': 0.2, 'SEOUL': 0.3, 'SOUTH': 0.3, 'NORTH': 0.3}, 
		{'DATE': 201805, 'COUNTRY': 0.0, 'CAPATIAL': 0.1, 'SEOUL': 0.2, 'SOUTH': 0.2, 'NORTH': 0.3}, 
		{'DATE': 201806, 'COUNTRY': 0.0, 'CAPATIAL': 0.1, 'SEOUL': 0.2, 'SOUTH': 0.1, 'NORTH': 0.4}, 
		{'DATE': 201807, 'COUNTRY': 0.0, 'CAPATIAL': 0.1, 'SEOUL': 0.3, 'SOUTH': 0.3, 'NORTH': 0.4}, 
		{'DATE': 201808, 'COUNTRY': 0.0, 'CAPATIAL': 0.2, 'SEOUL': 0.6, 'SOUTH': 0.6, 'NORTH': 0.6}, 
		{'DATE': 201809, 'COUNTRY': 0.3, 'CAPATIAL': 0.7, 'SEOUL': 1.3, 'SOUTH': 1.5, 'NORTH': 1.0}, 
		{'DATE': 201810, 'COUNTRY': 0.2, 'CAPATIAL': 0.4, 'SEOUL': 0.5, 'SOUTH': 0.5, 'NORTH': 0.6}, 
		{'DATE': 201811, 'COUNTRY': 0.1, 'CAPATIAL': 0.3, 'SEOUL': 0.2, 'SOUTH': 0.1, 'NORTH': 0.3}, 
		{'DATE': 201812, 'COUNTRY': 0.0, 'CAPATIAL': 0.1, 'SEOUL': 0.0, 'SOUTH': -0.1, 'NORTH': 0.2}, 
		{'DATE': 201901, 'COUNTRY': -0.1, 'CAPATIAL': -0.1, 'SEOUL': -0.2, 'SOUTH': -0.3, 'NORTH': -0.1}
	]}

output이 changeRate가 list인데 위에서 아래와는 다르죠.  
parameter가 들어간 경우입니다.
	
	{'stockList': [
		{'code': '005930', 'data': [{'DATE': '2019-02-25', 'END_PRICE': 47300}, {'DATE': '2019-02-22', 'END_PRICE': 47150}, {'DATE': '2019-02-21', 'END_PRICE': 46950}, {'DATE': '2019-02-20', 'END_PRICE': 46900}, {'DATE': '2019-02-19', 'END_PRICE': 45950}, {'DATE': '2019-02-18', 'END_PRICE': 46200}, {'DATE': '2019-02-15', 'END_PRICE': 46050}, {'DATE': '2019-02-14', 'END_PRICE': 47500}, {'DATE': '2019-02-13', 'END_PRICE': 46200}, {'DATE': '2019-02-12', 'END_PRICE': 46050}, {'DATE': '2019-02-11', 'END_PRICE': 45000}, {'DATE': '2019-02-08', 'END_PRICE': 44800}, {'DATE': '2019-02-07', 'END_PRICE': 46200}, {'DATE': '2019-02-01', 'END_PRICE': 46350}, {'DATE': '2019-01-31', 'END_PRICE': 46150}, {'DATE': '2019-01-30', 'END_PRICE': 46400}, {'DATE': '2019-01-29', 'END_PRICE': 45500}, {'DATE': '2019-01-28', 'END_PRICE': 45050}, {'DATE': '2019-01-25', 'END_PRICE': 44750}, {'DATE': '2019-01-24', 'END_PRICE': 43050}]}, 
		{'code': '066570', 'data': [{'DATE': '2019-02-25', 'END_PRICE': 71100}, {'DATE': '2019-02-22', 'END_PRICE': 73200}, {'DATE': '2019-02-21', 'END_PRICE': 73000}, {'DATE': '2019-02-20', 'END_PRICE': 72700}, {'DATE': '2019-02-19', 'END_PRICE': 72300}, {'DATE': '2019-02-18', 'END_PRICE': 72000}, {'DATE': '2019-02-15', 'END_PRICE': 72000}, {'DATE': '2019-02-14', 'END_PRICE': 72300}, {'DATE': '2019-02-13', 'END_PRICE': 72100}, {'DATE': '2019-02-12', 'END_PRICE': 71900}, {'DATE': '2019-02-11', 'END_PRICE': 69300}, {'DATE': '2019-02-08', 'END_PRICE': 64800}, {'DATE': '2019-02-07', 'END_PRICE': 65900}, {'DATE': '2019-02-01', 'END_PRICE': 65400}, {'DATE': '2019-01-31', 'END_PRICE': 66600}, {'DATE': '2019-01-30', 'END_PRICE': 67600}, {'DATE': '2019-01-29', 'END_PRICE': 67400}, {'DATE': '2019-01-28', 'END_PRICE': 67700}, {'DATE': '2019-01-25', 'END_PRICE': 69500}, {'DATE': '2019-01-24', 'END_PRICE': 65200}]}
	]}

차이가 느껴지시나요?  
parameter값을 기준으로 data라는 배열이 셋팅이 된 경우와(parameter 방식),  
outupt에서 설정한 pattern을 배열로 엮은 방식이네요

## 장고에서 사용해보기
이렇게 되니 기왕 한 번 완전한 놈으로 한 번 만들어 보고픈 욕심에 장고와 연동시켜봤습니다.  
https://github.com/ramoi/toobuk_vued3 

위 내용은 아래 url에서 확인할 수있습니다.  
https://toobuk.heroku.com

실제 업무에서느 이렇게 쓰진 않겠지요. 빅데이타의 최전방 보명으로 쓰던지, 아니면 데이타베이스에 저장하겠지요.  
그리고 더 중요한 것은 이 놈 보다 더 좋은 라이브러리가 많을 겁니다. 제가 자바를 주력 언어로 사용해서 파이썬 생태계를 잘 모르지만 
pandas가 많이 쓰이는 것 같네요..

## 남은 것들
처음에는 python을 공부하면서, 무언가를 하나 만들어보면서 다지려는 마음이었습니다.  
그런데 여기까지 왔네요. 테스트도 부족합니다.
하지만 누군가에게 조금이라도 도움이 되었다면 하는 바램입니다.
