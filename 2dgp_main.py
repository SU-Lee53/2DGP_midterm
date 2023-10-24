######################
####   2D 렌더링		####
######################
import random

# 게임 : 가상 월드에 존재하는 여러 객체들의 상호작용
# 2D게임 : 현재 진행 중인 게임 가상 월드의 내용을 화면이 2D그림으로 보여주는것
# pico2d 이용
from pico2d import *
# open_canvas로 염
# load_image로 이미지 로드
# draw_now로 그림
# close_canvas로 닫음

######################
####   애니메이션		####
######################

# draw_now로 생기는 플리핑(깜빡임)
# 더블 버퍼링으로 해결
# draw: 백버퍼에 그림
# update_canvas: 백버퍼 그려줌
# clear_canvas: 백버퍼 지워줌 -> update_cavas를 해야 지워진게 나옴

# 스프라이트: 게임 장면안에서 보여지는 이미지 또는 애니매이션되는 오브젝트
# 스프라이트의 구성: Action -> 움직임을 나타냄	Frame -> 한개의 이미지
# 애니메이션: 여러개의 이미지를 일정한 시간 간격을 통해서 화면에 뿌림으로써,
# 					물체가 움직이는 효과를 주는것

# 스프라이트 시트를 로드해서 clip_draw로 프레임을 바꾸면서 애니매이션 재생
# clip_draw(left, bottom, width, height, x, y, w=none, h=none)
# 	-> 맨끝 w,h는 확대해줌, 안넣으면 그냥 기본크기
# clip_composite_draw(left, bottom, width, height, rad, flip, x, y, w, h)
#		-> rad각도만큼 회전해줌 flip에 'h'를 넣으면 좌우반전도 시켜줌

######################
####    입력처리		####
######################

# 입력 처리 과정
# step1. 입력 이벤트들을 폴링한다(get_events())
# step2. 이벤트의 종류를 구분한다(event.type을 이용)
# step3. 실제 입력값을 구한다(event.key / event.x, event.y 등을 이용)

# 아래는 간단하게 esc키로 종료하는 이벤트 처리 함수

def handle_events():
	events = get_events()	# 발생한 모든 이벤트들을 모아서 가져옴
	for event in events:
		if event.type == SDL_QUIT:
			running = False
		elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
			# 이벤트 종류가 키가 눌림이고, 눌린 키가 esc라면 종료한다
			running = False

# 이벤트 종류들
# SDL_QUIT: 윈도우 종료시 발생
# SDL_KEYDOWN/KEYUP: 키보드가 눌리거나 떼어질때. event.key에 눌린 값이 들어옴
# SDL_MOUSEMOTION: 마우스가 움직이면 발생. event.x, event.y에 좌표 넘어옴
# SDL_MOUSEBUTTONDOWN/MOUSEBUTTONUP: 마우스 버튼 입력
#		-> 눌린 버튼의 종류가 event.button에 들어감, 좌표도 감
# SDL_MOUSEWHEEL: 마우스휠. event.wheel.x, event.wheel.y에 스크롤양이 들어옴

# SDL 키코드는 존나많음
# 키보드는 SDLK_로 시작
# 마우스 버튼은 SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT, SDL_BUTTON_MIDDLE
# 마우스 좌표는 윈도우좌표계에서 가져옴(원점이 좌측상단)
# 따라서 원점이 좌측하단인 pico2D에선 보정이 필요(y값을 height - 1 - event.y)

# 함수내에서 값이 결정되는 변수를 함수 밖에서도 쓰고싶다면 global 지정이 필요함
# 혹은 전역의 값을 가져올때도 global을 사용
# global 지정을 하지 않는다면 지역변수로 취급


######################
####    직선이동		####
######################

# 브레센헴 알고리즘(Bresenhem Line Algorithm): 화면상에 직선을 그리는 알고리즘

# 화면상에 직선그리기
# 1. y = ax + b 직선의 방정식을 이용
# 	문제점-> 기울기가 0인 수직선(y축 평행)은 그릴수 없음(0으로 나누기 문제)
# 2. Parametric Representation: 벡터를 이용한 선형결합
# 		x = (1-t)*x1 + t*x2
#			y = (1-t)*y1 + t*y2
#			이때 t는 0~1사이
# 	-> 직선 혹은 곡선의 (x,y) 좌표를 공통적인 파라미터를 이용하여 표현(여기서는 t)
#		-> 일반적인 수학적 표현에 비해, 컴퓨터를 이용하여 그리기가 편리함
#		-> 동일한 곡선에 대해, 파라미터 표현법은 여러가지가 있음. 이는 이미 다 만들어져있다 검색하면 나옴

# list comprehension: 리스트를 빠르게 만들기 위한 독특한 문법 구조
numbers = [n for n in range(1,10)]
odd_numbers = [n for n in range(1, 30) if n%2 == 1]
even_numbers = [n for n in range(1, 30) if n%2 == 0]
print(numbers)
print(odd_numbers)
print(even_numbers)


############################
####     게임 오브젝트 		####
############################

# 추상화: 꼭 필요한 객체들만, 꼭 보여줘야할 내용만, 꼭 보여줘야할 움직임만
# 게임 객체(오브젝트) = 속성 + 행위
# 속성: 게임 객체의 현재상태
# 행동: 시간에 따라, 혹은 이벤트에 반응해서 상태가 변하는 방식

# 객체의 모델링 방법
# 	- 데이터와 그 데이터 위에 수행되는 함수들을 가진 소프트웨어 모듈을 이용
#		- 데이터는 객체의 상태(State, Attributes)를 저장하는데 사용
#		- 함수는 그 객체가 수행하는 기능(Behavior, Operations, Methods)을 정의
#		- 객체의 조건: (State + Behavior) with Unique Identity

# 클래스(class)
# 	- 유사한 여러 객체들에게 공통적으로 필요로 하는 데이터와
# 	 이 데이터 위에서 수행되는 함수들을 정의하는 소프트웨어 단위
#		- 객체를 찍어내는 도장
#		- 클래스로 객체를 찍어내는 과정을 Object Instantiation 이라고 함
#	인스턴스(Instance): 생성된 각각의 객체

# 게임의 기본 구조
#	-> Initialization -> Game Logic -> Drawing -> if exit: Finish else: goto Game Logic

# 현재 프레임워크의 클래스 구조
# def __init__(self) -> 기본 파이썬 생성자
# def draw(self) -> 객체 렌더링
# def update(self) -> 상태 업데이트
#
# 현재 프레임워크
# def update_world() -> 객체들.update() 수행
# def render_world() -> 객체들.draw() 수행, 화면 초기화 및 그리기
# 아래는 소년 클래스의 예시
# import random
# class Boy:
# 	def __init__(self):	# 생성자
# 		self.x, self.y = random.randint(100, 100), 90	# 초기 위치 -> 랜덤
# 		self.frame = random.randint(0,7)					# 애니메이션 싱크가 되지않도록 랜덤
# 		self.image = load_image('animation_sheet.png')	# 소년 이미지 로드
#
# 	def update(self):		# 상태 업데이트
# 		self.frame = (self.frame + 1) % 8	# 프레임 변경
# 		self.x += 5		# x축 이동
#
# 	def draw(self):			# 렌더링
# 		self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)	# 소년 렌더링
#
# # 여러개의 객체를 list로 묶어 관리하면 용이함
# # 소년의 11명 생성 예시
# # team = [Boy()] * 11 -> 아래의 list comprehension이 더 좋음
# team = [Boy() for _ in range(11)]
# # 소년 11명을 전부 렌더링하려면
# for boy in team:
# 	boy.draw()
#
# # 모든 객체를 world list로 Refactoring하여 관리하면 좋다
# world = []
# world += team
# for o in world:
# 	o.draw()


##############################
####     캐릭터 컨트롤러 		####
##############################

# 만약 소년 객체를 많이 생성한다면 매번 이미지 로드에 시간이 걸림
# 이를 해결하기 위해 클래스 변수를 도입한다
import random
class Boy:
	image = None	# 모든 Boy객체가 이 변수를 공유함
	def __init__(self):
		self.x, self.y = random.randint(100, 700), 90
		self.frame = random.randint(0,7)
		if Boy.image == None:	# 이로인해 단 한번의 로딩만 수행하고 이미지를 모든 객체가 공유함
			Boy.image = load_image('animation_sheet.png')
	pass

# 캐릭터 컨트롤러: 게임 주인공의 행동을 구현한 것

# 상태 다이어그램(State Diagram): 시스템의 변화를 모델링하는 다이어그램
#		- 사건이나 시간에 따라 시스템 내의 객체들이 자신의 상태를 바꾸는 과정을 모델링함
#		- 모델링, 명세, 그리고 구현에 모두 사용되는 강력한 툴

# 상태(State): 어떤 조건을 만족하는 동안 머무르면서, 정해진 일을 수행하고 이벤트를 기다리는 '상황'
#	- Entry action: 특정 상태로 들어갈 때마다 발생하는 일
# - Exit action: 특정한 상태에서 나갈 때마다 발생하는 일
# - Do activity: 특정 상태에머무르는 동안 수행하는 일(반복될 수 있음)

# 이벤트: 상태 변화(State Transition)을 일으키는 원인이 되는 일
#		외부적인 이벤트 예: 키보드 입력
#		내부적인 이벤트 예: 타이머
#		경우에 따라 이벤트 없이도 상태변화가 있을 수 있음

# Python Module: 파이썬의 정의와 문장을 담고있는 파일, .py파일을 말함
# 	- 그 자체로도 실행 가능하며 다른 모듈에서 import 할수도 있음
#		- import되면 그 자체가 하나의 싱글톤 객체가 됨

# 이하 내용들은 코드와 함게 ppt 읽어보며 프레임워크 분석
#
# 프레임워크 참고할 사함
#	- boy.py
# 	- Idle, Run과 같은 상태 클래스는 객체생성을 위한게 아닌 특정함수의 그루핑하는 역할
#		 그래서 함수들이 @staticmethod로 선언되어있음
#		- 상태에는 모드 enter, exit, do, draw 함수가 있으며 do는 update같은 역할, draw는 렌더
#		- 클래스 멤버 함수의 첫번째 인자는 모두 self. 실질적 첫번째 인자는 2번째부터이고
#		 실제 함수 호출시에는 self 무시해도 됨
#		- 상태 이벤트는 이벤트 체크 함수를 이용하여 판단함
#		- 상태 이벤트는 튜플을 이용해서 나타내고 있음
#		- 상태 이벤트는 입력 이벤트(get_event)와 다른것임
#		- 그러니까 StateMachine의 handle_event는 입력을 받는 handle_event와 완전히 다른것임
#		- transition은 상태 변환 규칙을 담고있는 딕셔너리-딕셔너리 구조임.
#	   key에 상태, value에 또한번 딕셔너리로 key는 이벤트 체크 함수, value에는 다음 상태가 있음
#		- 작동방식은 밑에 더 자세하지만 간략하게 key의 현재 상태가 value의
#		 key 이벤트체크 함수가 True면 value의 value의 상태로 넘어가는 방식
#		- Boy의 action은 해당 action이 스프라이트 시트에서 몇번째에 위치해 있는지 담고있음
#		 그러면 action변수 하나로 프레임 높이, 현재/이전 이벤트를 모두 알수있음

#	아래는 Boy가 입력을 처리하는 과정
#		- Boy의 handle_event는 메인의 handle_event가 입력 이벤트를 받아서 넘겨줌
#		 혹은 각각의 상태에서 "TIME_OUT"과 같은 이벤트를 넘겨줌
#		- 그러면 Boy.handle_event()에서 받아온 입력 이벤트와 상태 이벤트인 'INPUT'을 튜플로 묶어
#		 자신의 StateMachine.handle_event로 넘김(객체가 StateMachine 객체를 변수로 갖고있음)
#				- python에서는 변수에 객체를 저장하는것이 가능, 참고로 함수도 저장 가능
#		- StateMachine에는 딕셔너리 형태로 상태변환이 구현되어 있는데 이는 객체 생성시 초기화됨
#		- 상태변환(self.transitions) 딕셔너리는 key와에 현재상태(cur_state),
#		 value에 이벤트 {체크 함수:다음 상태} 형태의 딕셔너리를 가지고 있음
# 	- for check_event, next_state in self.transitions[self.cur_state].items()
#		 이 코드는 transition에서 현재 상태의 키를 갖는 밸류의 쌍을 items()로 불러와
#		 key와 value를 각각 check_event와 next_state에 넣어줌
#		- if check_event(e)는 함수 호출시 받은 이벤트 튜플 e가
#		 해당 이벤트의 조건이 맞을시 True를 반환
#		- True라면 현재 이벤트.exit() -> 현재 이벤트 = 다음 이벤트 -> 현재 이벤트.enter()
#		- 이때 각각의 상태 enter, exit에 이벤트 튜플 e를 넘겨주는데 이는 상태변화의 원인을 알려주어
#		 각 상태로 인한 enter, exit시 필요한 작업을 수행하기 위함임
#		 그 예시로 Run에서 받은 이벤트를 확인하여 달리기 방향을 결정함

##########################
####     게임 월드 		####
##########################

# 프레임워크에 추가 및 변경된 사항
#		- boy.face_dir
#				-> action 변수만으로는 Idle에서 공발싸는 방향을 정하기 어려우므로 방향을 정하는 변수를 새로 만듬
#		- boy.fire_ball(): 공을 발사함
#			- 공은 Idle과 Run상태에서 exit시 발사함
#			- 공 발사를 위해 transition의 Idle/Run에 space_down: Idle/Run을 각각 추가해주었음
#			- 그러면 Idle과 Run상태에서 space_down발생시 exit되면서 공을 발사
#		 		그런데 각각 다음상태도 Idle, Run이므로 그대로 그 상태에 다시 enter하면서 이어짐
#		- ball.py: 위에서 발사되는 공 객체임
#			- 특이사항으로 화면밖으로 나가면 삭제되는데 삭제는 아래 game_world에서 설명
#		- game_world.py: 게임 월드를 관리하는 모듈의 추가
#			- game_world의 object 리스트는 리스트 안의 리스트 형태로 깊이를 가짐
#				- 첫번째 리스트부터 렌더링되어 가장 뒤에 그려짐
#				- 같은 깊이를 갖는 객체들이 같은 깊이의 리스트에 들어감
#				- 객체 리스트에 깊이가 생기면서 update와 render의 방법이 달라짐
#			- render와 update도 game_world 모듈에 관리하는 함수가 생김
#				- 이제 objects는 깊이를 가지므로 이중 for문을 돌며 렌더링과 업데이트를 진행함
#				- 그 예시
# 				for layer in objects:		# objects에서 깊이별 list를 가져옴
# 					for object in layer:	# 깊이별 list를 가져온 layer에서 객체를 가져옴
# 						object.render()/update()
#			- 월드의 objects 리스트에 객체를 추가할수 있는
#			 add_object(o, depth=0)와 add_objects(ol, depth=0)가 생김
#				- 앞에꺼는 1개, 뒤에꺼는 리스트로 받아서 여러개 넣을수 있음
#				- depth도 지정해서 넣을수 있으며 지정 안하면 0임(가장 뒤에 그려짐)
#			- 새로운 기능으로 remove_object(o)가 생겼음
#				- 인자로 넘어온 객체 o가 objects에 존재한다면 삭제함
#				- 만약 없는데 삭제하려고 한다면 예외가 발생함(raise)
#		- game_world가 생기면서 실행모듈인 control_boy도 변화가 생김
#			- reset_world가 create_world가 되어 game_world로 초기화됨
#				- 앞에서 import된 모듈은 하나의 싱글톤 객체가 된다고 설명했음
#			- update_world와 render_world도 game_world의 함수로 진행하게 됨
#				- 이제 실행모듈에 world 객체 리스트가 없으므로 루프를 직접 돌지 않고
#				 game_world에서 game_world.objects를 루프를돌며 update/render







