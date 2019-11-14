# 노는게좋아 SPST_S
### 프로젝트 조직
<strong>팀 : </strong>노는게좋아 </h5><br>
<strong>팀원 : </strong>황주현 | 방현우 | 이수호 | 임민섭 | 정현서<br>
<strong>주제 : </strong>스피어피싱 모의훈련 서비스 (SpearPhishing Simulation Training_Service)<br>

### 프로젝트 목표
1. 머신러닝 기술을 방어가 아닌 공격에 사용할 수 있다.
2. 훈련하기 까다로운 APT 공격을 보다 쉽게 진행할 수 있다.
3. 보안에서 사내 사원들의 보안 인식의 중요성을 알 수 있다.

### 프로젝트 사항
#### 스피어 피싱이란?
+ 2013년 필터링 기술력의 발전으로 많은 스팸 메시지들이 걸러지고 방어되면서 **한 사람을 특정하여 분석하고 집중적으로 공격** 하는 스피어 피싱의 빈도가 3배나 증가한 바 있다.<br>

#### 스피어 피싱 보안 훈련 필요성
+ 기존 스팸 메일 : 모든 사람들에게 동일한 메시지와 악성 의심 링크 혹 악성 접근을 수행한다.
+ 스피어 피싱 : 각 개인에 맞게(직업, 활동정보, 상태 등) 개인정보를 활용하여 관심사를 파악하고 취약한 부분을 특정하여 공격한다.
+ 예시 : 프로그래머에게는 버그 고칠 방법, 경찰관에게는 사고 발생 위치, 소방관에게는 화재 발생 위치를 주제로 어느 시간대, 감정이 해당 개인에 맞는 문장이 주어지면 다수를 대상으로 하는 문장보다 취약할 것이고 사내에서는 외부 공격보다 사원 하나의 실수로 인한 공격이 걸리기 쉽고 대비가 어렵다.

### 프로젝트 진행 환경
사용 언어 : 파이썬 3.7 (Python3.7)<br>
사용 라이브러리 : 
- 웹 크롤링 : time, oauth2, json, datetime, config, , tweepy, counter, pprint, os, sys, re, pandas
- 데이터베이스 : sqlite3, pymysql(v.0.6.6)
- 딥러닝(머신러닝) : nltk, KoNLpy, Numpy, Scikit-learn, Matplotlib

### 프로젝트 구동
<!--현재 spst 폴더의 파일들이 최종 파일--!>
<br>
파이썬 파일 실행 모듈
<pre><code>pip install config oauth2 pandas numpy konlpy soynlp pymysql matplotlib xlrd</code></pre><br>
파이썬 파일 exe 변환<br>
<strong>spst_main.py</strong>
<pre><code>pyinstaller --windowed -i=project_icon.ico --onefile spst_main.py --hidden-import=pandas --hidden-import=pymysql</code></pre>
<strong>spst_employee.py</strong>
<pre><code>pyinstaller --windowed -i=project_icon.ico --onefile spst_employee.py --hidden-import=pandas --hidden-import=pymysql</code></pre>
<strong>spst_analysis.py</strong>
<pre><code>pyinstaller --windowed -i=project_icon.ico --onefile spst_analysis.py --hidden-import=pandas --hidden-import=pymysql</code></pre>
<strong>spst_analy_crawl.py</strong>
<pre><code>pyinstaller -i=project_icon.ico --onefile spst_analy_crawl.py --hidden-import=pandas --hidden-import=config --hidden-import=numpy --hidden-import=konlpy --hidden-import=oauth2 --hidden-import=soynlp --hidden-import=sklearn.utils._cython_blas --hidden-import=pymysql --add-data konlpy;konlpy</code></pre>
<strong>spst_result.py</strong>
<pre><code>pyinstaller -i=project_icon.ico --onefile spst_result.py --hidden-import=pymysql --hidden-import=konlpy --hidden-import=pandas --add-data konlpy;konlpy</code></pre>
<br>
<strong>exe 변환 완료된 파이썬 프로그램</strong><br>

- https://drive.google.com/open?id=1wwASb5nIrQdX_pW9t5fBvdqsYD5TWF_9
