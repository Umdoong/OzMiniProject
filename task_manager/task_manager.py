import os
import json


def task_create():
	title = input('무슨 일을 하실 건가요? ') # 할 일 입력받기
	data = {'title': title, 'check': False} # 할 일 이름 받아서 data에 할당
	with open(f'./{title}.json', 'w', encoding='utf-8') as f: # title의 이름을 가진 json을 현재 디렉토리에서 utf-8형식으로 인코딩해서 f에 초기화,
		json.dump(data, f, ensure_ascii=False, indent=4)      # with as문으로 파일을 건드릴 경우 close로 닫아줄 필요는 없다
	# json.dump는 파이썬 객체를 json 문자열로 변환해줍니다
    # 8열에서 생성한 파일(f)에 data를 적어서 넣어주는데 ensure_ascii=False를 통해 아스키 코드로 변환되는 걸 방지하고 들여쓰기 4칸을 해줍니다)
	print(f'할 일 "{title}"이/가 추가되었습니다.')


def task_list(show_completed=False): # show_completed를 매개변수로 받는데 기본값을 False다
	print("=" * 10, "\n할 일 목록\n", "=" * 10)
	task_files = [f for f in os.listdir("./") if f.endswith('.json')]
    # 리스트 컴프리헨션으로 1줄로 요약했다
    # task_files = []                     task_files라는 리스트 초기화
    # for f in os.listdir("./"):          현재 디렉토리 내에 있는 모든 파일과 디렉토리를 list로 리턴해서 f에 하나씩 할당하는 것을 반복한다
    #     if f.endswith('.json'):         .json으로 끝나는 파일이 있을 경우
    #         task_files.append(f)        task_files 리스트에 f를 추가한다.

	# os.path.getctime은 파일(디렉토리)의 생성 시간을 반환해줍니다
	# sort문의 기본 매개변수에는 key가 있다. 람다식을 이용해 파일들의 생성 시간을 key로 전달해주면 생성 시간을 기준으로 task_files를 정렬해준다
	task_files.sort(key=lambda x: os.path.getctime(x))

	tasks = []  # (파일명, 데이터) 튜플로 저장
	for task_file in task_files: # 17열에서 만든 리스트를 for문으로 반복
		with open(task_file, 'r', encoding='utf-8') as f: # 리스트 0번 인덱스부터 차례로 읽는다. 내용이 깨지지 않게 utf-8로 인코딩 해서 읽는다.
			data = json.load(f) # json.load는 json문자열을 python 객체(딕셔너리)로 변환해준다
			if show_completed or not data['check']:  # 매개변수가 True거나 check의 value가 False라면 True를 리턴한다
				tasks.append((task_file, data))		 # 할 일이 완료돼 check가 True인 파일들을 보고 싶으면 show_completed에 True를 할당해주면 된다.
			# tasks 리스트에 task_file(파일명)과 data(딕셔너리=할 일과 완료 유무)를 튜플로 추가해라

	for i, (_, task) in enumerate(tasks, 1): # enumerate는 리스트의 인덱스(tasks(_, task))와 요소(i)로 이루어진 tuple을 만들어줍니다.
		# tasks는 인덱스 별로 (파일명, data)로 구성되어 있는데 파일명은 필요 없으므로 관례적인 _를 사용
		status = "[완료]" if task['check'] else "[미완료]" # stauts에 task['check']가 True면 '[완료]', False면 '[미완료]'를 초기화한다.
		print(f"{i}. {task['title']} {status}")

	return tasks # 인덱스 별로 (파일명, {할 일과 완료 유무})를 갖고 있는 tasks를 다른 함수에서 재활용 할 수 있도록 반환


def task_complete():
	tasks = task_list()  # task_list 함수 호출해서 tasks에 초기화 ( return 했던 tasks를 초기화 )

	if not tasks: # 리스트가 비어있으면 False를 리턴하는 식으로 유효성 검사
		print("완료할 할 일이 없습니다.")
		return

	try:
		task_num = int(input('완료할 할 일의 번호를 입력하세요: ')) # check를 true로 바꿔줄 번호 입력받기
		task_file, data = tasks[task_num-1]  # 선택한 번호의 인덱스를 task_file = 파일명, data = { title : {title}, check : False }으로 할당

		data['check'] = True  # 완료 처리

		with open(task_file, 'w', encoding='utf-8') as f: # 파일을 새로 작성 ( data['check']을 True로 바꿨으니까 )
			json.dump(data, f, ensure_ascii=False, indent=4)

		print(f'할 일 "{data["title"]}"이/가 완료되었습니다.')
	except (ValueError, IndexError) as e: # 매개변수가 잘못 되었거나(ValueError) 인덱스를 벗어나는 수(IndexError)를 적었을 때 예외처리
		print(e, "\n잘못된 번호입니다. 다시 시도해주세요.") # 예외 이유를 보여주고 print문 출력


def task_delete():
	tasks = task_list(show_completed=True)  # 원래 32열의 if문으로 인해 완료된 할 일은 task_list함수에서 반환되지 않지만
											# show_completed=True를 인자로 해주면 완료된 할 일도 tasks에 추가되어 반환된다.

	if not tasks: # 빈 리스트일 경우 할 일이 없는 것이므로 이런 식으로 유효성 검사가 가능하다
		print("삭제할 할 일이 없습니다.")
		return

	try:
		task_num = int(input('삭제할 할 일의 번호를 입력하세요: ')) # 삭제할 일의 번호를 입력받는다.
		task_file, data = tasks[task_num-1] # 선택한 번호의 인덱스를 변수에 초기화한다.(1부터 시작하게 설계했기 # 때문에 -1로 0번 인덱스를 선택할 수 있게 해준다)
		os.remove(task_file)  # 인자로 파일명을 집어넣어 삭제한다.
		print(f'할 일 "{data["title"]}"가 삭제되었습니다.') # data['title']은 곧 파일명과 동일하므로 할 일을 삭제했다는 의미
	except (ValueError, IndexError) as e: # 매개변수가 잘못 되었거나(ValueError) 인덱스를 벗어나는 수(IndexError)를 적었을 때 예외처리
		print(e, "\n잘못된 번호입니다. 다시 시도해주세요.")


def show_menu():
	print("=" * 22)
	print("작업 관리 애플리케이션")
	print("1. 할 일 추가")
	print("2. 할 일 목록 보기")
	print("3. 할 일 완료")
	print("4. 할 일 삭제")
	print("5. 종료")
	print("=" * 22)


def main():
	while True:
		show_menu()
		choice = input("원하는 작업을 선택하세요 (1~5) : ")
		if choice != ['1', '2', '3', '4', '5']:
			print("잘못된 입력입니다. 다시 선택해주세요.")
		if choice == '1':
			task_create()
		if choice == '2':
			task_list()
		if choice == '3':
			task_complete()
		if choice == '4':
			task_delete()
		if choice == '5':
			break

if __name__ == '__main__':
	main()