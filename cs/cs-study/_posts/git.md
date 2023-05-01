---

---

## git 명령어

- git remote add <name> <URL> : 로컬 원격저장소 추가
  - git remote add origin <URL>
- git push <name> <branch> : name원격 저장소에 branch 업로드
  - git push origin master
- git add: 파일의 변경사항 스테이징
- git commit: 파일의 변경사항 커밋

## git 파일 상태
- git status
- Untarcked
- Trakced
  - Unmodified
  - Modified
  - Staged
  
## .gitignore
git이 관리하지 않을 파일들은 gitignore에 작성합니다.
  

```git
$ cd git-
git-practice/ git-test/

$ cd git-^c

$ mkdir git-branch
$ code git-branch/
```
git 연습 디렉토리를 설정합니다.

```git
$ touch README.md .gitignore

$ git init

# git commit -m 'first commit'^c
```
보통 처음에 init하기 전에 ignore할 사항을 먼저 체크합니다.
  
> commit할 때 -m을 붙이지 않으면 Vim이 켜집니다.
  
    
  
