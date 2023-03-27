# SSCC ONECUT

### SSCC 부스 중 인생한컷 이미지 프로세스용 repo
> 특정 뷰어마다 기본 글꼴 및 자간 등 다양한 속성이 모두 다르기에,  
> Window 11 메모장을 기준으로 제작하였습니다

---

### 현재 기본 원리  

OPENCV속 `BGR2GRAY`를 활용하여 GARY SCALE 이미지로 변환하였고,
변환된 이미지의 value값을 기반으로 아스키 문자를 `print()`로 출력

---

### 구현되어 있는 AA  
```markdown
getAA_01 : 밀도 블록으로 AA 구현
#   ▓▓ ▒▒ ░░ '  '
```

---

### 파일 구성
1. main.py : main 함수 작성
2. utils.py : 이미지를 가져오며, AA에 필요한 함수 작성
3. img/*.[png/jpg] : img 폴더에 테스트에 쓰일 이미지를 모아둠


--- 

### QUICK START
1. `clone` repo
2. do main func!   `(done.)`