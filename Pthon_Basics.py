#####################
#### 파이썬 기초(1)####
#####################

# python의 나눗셈은 C와는 다름
print("나눗셈 4 / 3", 4 / 3)
print("나눗셈(몫) 4 // 3", 4 // 3)
print("나눗셈(나머지) 4 % 3", 4 % 3)

# 거듭제곱을 **로 계산가능함
print("3의 제곱은 3 ** 2", 3 ** 2)

# 변수에 문자열을 담을 수 있음. 다만 C의 char와 같은 글자는 size=1인 문자열로 취급
# 또한 문자열 입력시 '', "", """ """ 를 모두 사용가능함
word = 'word'
print(word)

# python의 자료형은 int, float, str, bool
print(type(1234))
print(type(12.34))
print(type('1234'))
print(type(True))

# 입력을 받는 함수인 input은 기본적으로 문자열이 넘어옴
# 정수로 바꾸고싶다면 int로 따로 변경하거나 int(input())을 사용가능
# print(type(input('>>')))
# print(type(int(input('>>'))))

# 형변환(캐스팅)은 원하는 자료형()이면 끝 -> int(), float(), str()

# bool 자료형은 True or False. 특이한점은 첫글자가 대문자임
# 비교연산(==, <, >, <=, >=)의 결과가 bool

# 문자열도 비교가 가능함
print("abc == abc:", 'abc' == 'abc')
print("abc == abd:", 'abc' == 'abd')

# 문자열 이어붙이기도 +로 가능함. 또한 C처럼 인덱스로도 접근가능. 음수면 끝으로감
first = 'abc'
last = 'def'
word = first + last
print("abc+def:", word)
print("word[3]:", word[3])
print("word[-1]:", word[-1])

# 문자열 슬라이싱: str[from:to]의 형태, 이때 to는 미포함임
# 또한 슬라이싱은 복사해서 가져오는 형태임
print("word[0:3]:", word[0:3])

# python의 list 자료형[]: C의 배열과 비슷하고 문자열처럼 슬라이싱, 이어붙이기가 가능
stop = ['home', 'lets', 'go']
plz = ['vacation', 'when']
stopplz = stop + plz
print("stop:", stop)
print("plz:",plz)
print("stop + plz:", stopplz)
print("stopplz[0:3]:", stopplz[0:3])

# dictionary 자료형{}: 구조체 배열? 느낌임
pydict = {'name':'2DGP', 'mid':1025, 'status':123}
print(pydict)
print(pydict.keys())
print(pydict.values())

# a in b 구문은 dictionary에선 key값만 찾아줌(처음알았음)
print('name' in pydict)
print('mid' in pydict)
print(1025 in pydict)

# Tuple(): list처럼 여러개를 관리하지만 값을 변경할수 없는 상수들임
# set{}: list와 유사하지만 이름값(집함)답게 중복을 허용하지 않고 순서도 없음
# set의 선언은 dictionary처럼 {}이지만 키:밸류 쌍을 안넣으면 됨
# set은 논리연산만 지원, +같은 이어붙이기가 안됨

# 복합 자료형도 가능함 list안에 list가 들어있다거나 하는식


#####################
#### 파이썬 기초(2)####
#####################

# turtle 간단히 알아보자
# turtle.reset(): 말그대로 리셋. 중앙으로 오고 기본 방향이 오른쪽
# turtle.forward(d): 바라보는방향으로 d만큼 이동
# turtle.left(r)/right(r): 왼쪽/오른쪽으로 r만큼 회전
# turtle.circle(r): 반지름이 r인 원을 그림
# turtle.undo(): 이전으로 되돌아감
# turtle.setheading(r): 거북이 머리를 r각도를 향하게함(기초3 pdf)
# turtle.goto(x,y): x,y로 이동. 참고로 중심이 (0,0)

# .py파일은 독립적인 실행이 가능함. py파일 실행으로 바로 프로그램 ON


#####################
#### 파이썬 기초(3)####
#####################

# 조건문 if, elif, else: C와 같은데 elif는 else if와 같은의미
# if문의 조건에 굳이 괄호를 적지 않아도 된다는 것도 차이점

# 반복문 while: C처럼 쓰면 됨

# 반복문 for: 2가지 방법이 있음
#		1. for i in list, tulpe, str: 데이터에서 요소를 직접 꺼낸다
#		2. for i in range(form, to, step): C의 반복문처럼 작동, 참고로 to는 미포함
rg = [int(a) for a in range(1,10)]
print("range(1,10):", rg)
# 다중대입: a, b = 1, 2 이러면 각각 1, 2가 들어감
# 이를 이용하여 a,b = b,a를 하면 서로 스왑이됨

a, b = 10, 20
print(a, b)
a,b = b,a
print(a, b)

# 파이썬은 들여쓰기(indentation)으로 코드블럭이 나뉘어짐. 참고로 C는 {}

# random 모듈: 말그대로 무작위
# random.randint: 무작위 숫자를 뽑음

import random
print(random.randint(10, 100))

# 기출문제: 랜덤한 알파벳을 뽑아보자
print("random character:", chr(random.randint(65, 90)))
# 참고로 대문자는 65~90, 소문자는 97~122임

# 함수는 def function_name(parameters):로 정의
# 인자 타입에 따라 알아서 지가 판단해서 연산기능 결정
def func():
	print('func called')
	return 'return'
print(func())



