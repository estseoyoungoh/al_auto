import os
os.system('pip install --upgrade selenium') # 코드를 실행할때마다 셀레니움을 업그레이드

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import configparser
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip

# 웹 드라이버 주요 옵션
options = Options()

options.add_argument("--start-maximized") # 브라우저 창 최대화로 실행
options.add_experimental_option("detach", True) # 브라우저 유지
options.add_experimental_option("excludeSwitches", ["enable-automation"]) # 자동화 메세지 제거
# 크롬에서 뜨는 비밀번호 저장 옵션 끔
options.add_experimental_option("prefs", {
    "credentials_enable_service": False,   # 크롬 자격 증명 서비스 비활성화
    "profile.password_manager_enabled": False  # 비밀번호 관리자 비활성화
})

config = configparser.ConfigParser()

# 한글 읽을려면 UTF-8 인코딩을 지정
config.read('config.ini', encoding='utf-8')

driver = webdriver.Chrome(options)

driver.get('https://qa.altools.co.kr/')
time.sleep(2)
#수정해본다
driver.close()


"""


# place holder 텍스트중 일부만 일치해도 찾을수 있게 함
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Email')]"))
).send_keys(config['ACCOUNT']['EMAIL'])

# '계속' 버튼 클릭
driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]").click()

# 비밀번호 입력
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Please')]"))
).send_keys(config['ACCOUNT']['PW'])

# '확인' 버튼 클릭
driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm')]").click()

# 사이트 언어 설정을 국문으로 변경
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-lang="ko"]'))
).click()

# By.CSS_SELECTOR, 'a[data-lang="ko"]'  located((By.XPATH, '//a[@data-lang="ko"]'))

time.sleep(1)

# 새 프로젝트 생성 페이지로 이동
driver.get(config['ADDRESS']['URL']+'project/new')

# 모델 선택
# 모델 이름 찾아서 스크롤하고 클릭
model_name_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, f"//p[text()='{config['MODEL']['NAME']}']"))
)
driver.execute_script("arguments[0].scrollIntoView(true);", model_name_element)  # 요소까지 스크롤
model_name_element.click()  # 요소 클릭
time.sleep(1)

# 선택 완료 버튼 클릭
driver.find_element(By.CLASS_NAME, "choice").click()

# 모델 설정 탭 클릭
driver.find_element(By.XPATH, "//button[@data-value='MODEL']").click()

# 스타일의 개수와 목록 추출
# '스타일'이라는 텍스트를 가진 타이틀을 포함하는 섹션 내의 모든 <p> 태그
style_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '스타일')]/following-sibling::ul//li//p")
styles = [element.text for element in style_elements]
last_style = styles[-1]

print("스타일 개수:", len(styles))
print("스타일 목록: " + ", ".join(styles))

# 앵글의 개수와 목록 추출
angle_elements = driver.find_elements(By.CLASS_NAME, "angle_name")
angles = [element.text for element in angle_elements]
last_angle = angles[-1]
print("앵글 개수:", len(angles))
print("앵글 목록: " + ", ".join(angles))

# 포즈의 개수와 목록 추출
# "포즈"라는 단어를 포함하는 <strong> 태그 바로 아래의 <div class="group"> 안에 있는 모든 버튼 찾기
pose_elements = driver.find_elements(By.XPATH, "//strong[contains(text(), '포즈')]/following-sibling::div[contains(@class, 'contents')]/div[contains(@class, 'group')]/button")
poses = [element.text for element in pose_elements]
last_pose = poses[-1]

print("포즈 개수:", len(poses))
print("포즈 목록: " + ", ".join(poses))

# 클립보드에 텍스트 복사
pyperclip.copy(config['SCRIPT']['KOR'])

#### 스타일/앵글/포즈별 반복

for style in styles:
    driver.find_element(By.XPATH, f"//p[text()='{style}']").click()
    print(style)
    time.sleep(1)  # 필요에 따라 조정

    for angle in angles:
        driver.find_element(By.XPATH, f"//*[contains(@class, 'angle_name') and text()='{angle}']").click()
        print(angle)
        time.sleep(1)  # 필요에 따라 조정

        for pose in poses:
            driver.find_element(By.XPATH, f"//button[text()='{pose}']").click()
            print(pose)
            driver.find_element(By.CLASS_NAME, "close").click()
            time.sleep(1)  # 필요에 따라 조정

            # 스크립트 입력
            driver.find_element(By.CLASS_NAME, "sentence").click()

            # ActionChains를 사용하여 붙여넣기
            # 문장을 sendkey로 바로 입력시 문장 분리가 되지 않으므로 복사/붙여넣기로 해야함
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

            time.sleep(1)  # 필요에 따라 조정

            # 슬라이드 추가와 모델 설정탭을 클릭하는데 마지막 순환에서는 하지 않음
            if style != last_style or angle != last_angle or pose != last_pose:
                driver.find_element(By.CSS_SELECTOR, "li a.add").click()
                time.sleep(1)  # 필요에 따라 조정
                driver.find_element(By.XPATH, "//button[@data-value='MODEL']").click()
                time.sleep(1)  # 필요에 따라 조정


# 내보내기 버튼 클릭
time.sleep(5)
driver.find_element(By.XPATH, "//button[.//i[contains(text(), '내보내기')]]").click()

# 내보내기 옵션 레이에서 내보내기 한번 더 클릭
driver.find_element(By.XPATH, "//button[contains(@class, 'save') and contains(text(), '내보내기')]").click()

# '내보내기를 시작합니다.' 문구가 나타날 때까지 대기
WebDriverWait(driver, 600).until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '내보내기를 시작합니다.')]"))
)
driver.find_element(By.XPATH, "//button[contains(text(), '확인')]").click()

# 작업 대기 알림창이 있는 경우 '확인' 클릭
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '현재 작업 대기 중인 요청이 있어')]"))
    )
    driver.find_element(By.XPATH, "//button[contains(text(), '확인')]").click()

except:
    pass


#print(driver.window_handles)
"""