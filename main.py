from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from random import randrange, uniform, shuffle
import unicodedata
from selenium.webdriver.common.by import By
import random, schedule
from datetime import datetime

# 자신의 아이디, 비밀번호 입력
yourid : str = ""
yourpassword : str = ""

# 좋아요를 1개 누르는 최소, 최대 시간 간격(1분 내외로 설정)
clickLikePauseMin : float = 40.0
clickLikePauseMax : float = 70.0

# 페이지 로딩까지 대기하는 시간(10초내외로 설정)
pageLoadingWaitMin : float = 5.0
pageLoadingWaitMax : float = 10.0
 
# 인친들 피트 좋아요 누르는 개수 설정
# clickLikeFriendFeed : int = 2 # following 메소드에서 main에 max로 대체
 
# 검색을 원하는 태그 입력
tags : list = ['원하는', '태그를', '리스트', '형태로 입력']

# 태그 하나당 좋아요를 누르는 최소, 최대 개수 설정
clickLikeInTagMin : int = 15
clickLikeInTagMax : int = 20

# 다음 태그로 넘어가는 쉬는 시간
tagIntervalmin : float = 120.0
tagIntervalmax : float = 200.0

# 입력하고싶은 댓글 내용 입력
comments : list = ['♡', '원하는 댓글을', '리스트 형태로 입력', '우리 서로 맞팔해요~']

# 좋아요를 누른 총 개수 카운터(손대지 말 것)
totalLikeCount : int = 0 

def login(driver, id : str, password : str):
    print('로그인 진행중...')
    driver.implicitly_wait(6)
    ur_id = driver.find_element(By.XPATH, '//input[@aria-label="전화번호, 사용자 이름 또는 이메일"]')
    ur_id.send_keys(id)

    # 아이디 입력 후 쉬는시간
    time.sleep(uniform(1.0, 3.0))
    ur_password = driver.find_element(By.XPATH, '//input[@aria-label="비밀번호"]')
    ur_password.send_keys(password)
    
    #비밀번호 입력 후 쉬는시간
    time.sleep(uniform(1.0, 3.0))
    ur_password.send_keys(Keys.ENTER)
    
    #엔터키 입력 후 쉬는시간
    time.sleep(uniform(pageLoadingWaitMin, pageLoadingWaitMax))
    while True:
        try:
            islogin = driver.find_element(By.XPATH, f'//*[contains(@alt, "{yourid}")]')
            print("로그인 완료")
            break
        except:
            relogin = input('로그인에 실패했습니다. 수동으로 로그인 후 y를 눌러주세요.')
            if relogin == 'y' or 'Y':
                pass

def detect_ad(driver):
    ad_list = ['아이디 입력', '재테크', '투자', '부업', '집테크', '고수입', '수입', '억대연봉', '억대', '연봉', '순수익', '초기금액', '초기 금액', '금액', '입금', '광고']
    article = driver.find_elements(By.XPATH, '//article//div[1]/span')
    for texts in article :
        text = unicodedata.normalize('NFC',texts.get_attribute('innerText'))
        for ad in ad_list :
            if text.find(ad) == -1 :
                continue
            else :
                print(f'광고 발견. 발견된 광고단어 : {ad}')
                return True
            
def comment(driver, text : str):
    tringer = randrange(1,5)
    if tringer != 3:
        return
    try : 
        comment_path = driver.find_element(By.XPATH, '//textarea[@aria-label="댓글 달기..."]')
        pass
    except :
        print('댓글이 제한된 피드입니다.')
        return
    comment_path.click()
    comment_path = driver.find_element(By.TAG_NAME, 'textarea')
    driver.implicitly_wait(1)
    comment_path.send_keys(f'{text}')
    comment_path.send_keys(Keys.ENTER)
    print(f'댓글을 달았습니다. 내용 : {text}')
    time.sleep(uniform(pageLoadingWaitMin, pageLoadingWaitMax))

def click_likebtn(driver, like_num : int, stop_num : int):
    global totalLikeCount
    like_btn = driver.find_element(By.XPATH, '//*[@aria-label="좋아요" or @aria-label="좋아요 취소"] //ancestor :: div[2]')
    like_svg = like_btn.find_element(By.TAG_NAME, 'svg').get_attribute('aria-label')
    
    if like_svg == '좋아요' : 
        like_btn.click()
        like_num += 1 
        totalLikeCount += 1
        print(f'좋아요 {like_num}번째 : 좋아요 총 {totalLikeCount}개')
        
        # 댓글을 달고 싶다면 아래의 주석을 해제
        # comment(comments[randrange(len(comments))])
        
        time.sleep(randrange(clickLikePauseMin, clickLikePauseMax))
        return like_num, stop_num
    
    else :
        stop_num += 1
        print(f'이미 좋아요 작업한 피드 : {stop_num}개 중복')
        time.sleep(uniform(pageLoadingWaitMin, pageLoadingWaitMax))
        return like_num, stop_num

def next_btn(driver):
    driver.find_element(By.XPATH, '//*[@aria-label="다음"] //ancestor :: button').click()

def following(driver, following_stopnum : int):
    global totalLikeCount
    try: 
        driver.find_element(By.XPATH, '//div[text() = "새 게시물"] //ancestor :: button').click()
    except:
        pass
    
    following_likenum = 0

    while following_likenum < following_stopnum:
        try : 
            following_likebtn = driver.find_element(By.XPATH, '//*[@aria-label="좋아요" and @height = "24"]/ancestor :: div[2]')
            driver.execute_script("arguments[0].scrollIntoView({block : 'center'});", following_likebtn)
            following_likebtn.click()
            following_likenum += 1
            totalLikeCount += 1
            print(f'팔로워 새피드 좋아요 {following_likenum}개 누름 : 좋아요 총 {totalLikeCount}개')
            time.sleep(uniform(clickLikePauseMin, clickLikePauseMax))
        except:
            driver.get('https://instagram.com')
            time.sleep(uniform(pageLoadingWaitMin, pageLoadingWaitMax))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(10)  
                    
def bot(driver, insta_tag : str, how_many : int): 
    print(f'작업 태그는 {insta_tag}입니다.')
    driver.get(f'https://www.instagram.com/explore/tags/{insta_tag}/')
    
    #페이지 로딩 대기
    time.sleep(uniform(pageLoadingWaitMin, pageLoadingWaitMax))
    
    new_feed = driver.find_elements(By.XPATH, '//article//img //ancestor :: div[2]')[9]
    new_feed.click()
    
    #페이지 로딩 대기
    time.sleep(uniform(pageLoadingWaitMin, pageLoadingWaitMax))
       
    like = 0
    stop = 0
    
    for click in range(how_many):
        if detect_ad(driver) == True:
            next_btn(driver)
            #페이지 로딩 대기
            time.sleep(uniform(pageLoadingWaitMin, pageLoadingWaitMax))
 
        else :
            like, stop = click_likebtn(driver, like, stop)
            next_btn(driver)
            
            #페이지 로딩 대기
            time.sleep(uniform(pageLoadingWaitMin, pageLoadingWaitMax))
            
            if stop >= 4 :
                print(f'중복 피드가 많아 {insta_tag} 태그 작업 종료함')
                return like
    
    print(f'{insta_tag} 태그 작업완료')
    return like
    
def main(max):
    try:
        driver = webdriver.Chrome('chromedriver.exe')
    except:
        driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://instagram.com')
    login(driver, yourid,yourpassword)
    driver.get('https://instagram.com')
    driver.implicitly_wait(10)
    try : 
        driver.find_element(By.XPATH, '//*[text() = "나중에 하기"]').click()
        driver.implicitly_wait(10)    
    except :
        pass
    shuffle(tags)

    # for tag in tags
    try : 
        #본문에 아래처럼 함수를 삽입합니다.
        following(driver, max)
        # bot(tag, randrange(clickLikeInTagMin,clickLikeInTagMax))
        # time.sleep(uniform(tagIntervalmin, tagIntervalmax))
    except:
        driver.refresh()
    driver.quit()

def getMin():
    random_number = random.randint(0, 59)
    minute = "0"
    if 0 <= random_number <= 9:
        minute = minute + str(random_number)
    else:
        minute = str(random_number)
    return minute

def wait_until(specified_time: str) -> None:
    specified_hour, specified_minute = map(int, specified_time.split(":"))
    while True:
        current_time = time.localtime()
        if current_time.tm_hour == specified_hour and current_time.tm_min >= specified_minute:
            break
        time.sleep(1)

def work(time, max):
    hour = time
    min = getMin()
    exeTime = f"{hour}:{min}"
    print(f"작업 시작할 시간: {exeTime}")
    wait_until(exeTime)
    try:
        main(max)
    except:
        pass

while True:
    print("인스타그램 작업을 시작합니다.")
    work("09", 400)
    work("12", 200)
    work("17", 300)
    work("20", 200)
    work("23", 500)