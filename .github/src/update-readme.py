import os
from datetime import datetime
import re

# 탐색할 root 경로
dir_path = "."

# ignore 파일을 읽어서 패턴 목록을 리스트로 저장
with open('./.github/config/.ignore', 'r') as f:
    ignore = f.readlines()
patterns = []
for p in ignore:
    pattern = r""
    for c in p.strip():
        if c == '*':
            pattern = pattern + r".*"
        elif c in ".^$*+?{}[]|()":  # 메타 문자
            pattern = pattern + r"[{}]".format(c)
        else:
            pattern = pattern + r'{}'.format(c)
    patterns.append(pattern)

    
# ignore 패턴과 일치하는지 확인하는 함수
def check_ignore_pattern(item_path):
    for pattern in patterns:
        if re.fullmatch(pattern, item_path[(len(dir_path)+1):]):  # 항상 붙는 "[dir_path]/" 제거
            return True
    return False


def find_target(path, level):
    file_list = []
    # 하위 디렉토리 순환
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        
        if check_ignore_pattern(item) or check_ignore_pattern(item_path): # 파일 이름이나 경로가 ignore 조건을 만족하면 무시
            continue
            
        # 파일(혹은 디렉토리) 리스트에 추가하기
        mtime = datetime.fromtimestamp(os.stat(item_path).st_mtime)  # 수정 날짜 가져오기
        mtime = mtime.strftime('%a %b %d %Y')  # 날짜 형식 변환
        file_list.append([item, item_path, mtime, []])
        
        # 디렉토리면 하위 디렉토리 탐색
        if os.path.isdir(item_path):
            sub_list = find_target(item_path, level+1)
            if len(sub_list) == 0:  # 만약 하위 디렉토리에 아무것도 없으면 현재 디렉토리도 삭제
                file_list.pop()
            elif len(sub_list) == 1:  # 만약 하위 디렉토리에 파일이 하나라면 합치기
                sub_file = sub_list[0]
                sub_file[0] = item + '/' + sub_file[0]
                file_list[-1] = sub_file
            else:
                file_list[-1][3] = sub_list
        else:
            only_files.append([item, item_path, mtime])

    return file_list
       

# 재귀적으로 파일 출력
def print_file_list(f, file_list, level):
    file_list.sort(key=lambda file: file[2], reverse=True)
    for file in file_list:
        for i in range(level):
            f.write("  ")
        
        if len(file[3]) == 0:  # 파일이면 수정 날짜와 함께 출력
            f.write("- [{}](\"{}\") - {}\n".format(file[0], file[1].replace(' ', '_'), file[2]))
        else:  # 디렉토리면 날짜 빼고 출력
            f.write("- [{}](\"{}\")\n".format(file[0], file[1].replace(' ', '_')))
            print_file_list(f, file[3], level+1)


only_files = []
file_list = find_target(dir_path, 0)

only_files.sort(key=lambda file: file[2], reverse=True)

# README.md 파일을 열어 파일 경로를 추가
with open("README.md", "w") as f:
    f.write("# mathematics\n")
    f.write("A collection of notes and solutions on various mathematical topics.\n\n")
    f.write("---\n\n")

    most = 3
    f.write("### {} most recent study\n".format(most))
    for i in range(most):
        f.write("- [{}](\"{}\") - {}\n".format(only_files[i][0], only_files[i][1].replace(' ', '_'), only_files[i][2]))
    f.write("\n")


    file_list.sort(key=lambda file: file[2], reverse=True)
    f.write("### Categories\n")
    for file in file_list:
        f.write("- [{}](#{})\n".format(file[0], file[0]))
    f.write("\n")


    for file in file_list:
        f.write("### [{}](#{})\n".format(file[0], file[0]))
        print_file_list(f, file[3], 0)
        f.write("\n")
