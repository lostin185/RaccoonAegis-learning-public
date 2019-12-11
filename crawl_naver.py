from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()

options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')

driver = webdriver.Chrome('크롬드라이버 위치를 지정해주세요.', chrome_options=options)
cuss_url = '네이버 뉴스의 url을 입력해주세요.'
driver.get(cuss_url)

click_freq = 5

WebDriverWait(driver, 10).until(
  EC.visibility_of_element_located((By.XPATH, '//*[@id="cbox_module"]/div/div[6]/div[1]/div/ul/li[3]/a/span[2]'))
).click()

for i in range(0, click_freq):
  WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@class="u_cbox_btn_more"]'))
  ).click()

elements = WebDriverWait(driver, 10).until(
  EC.presence_of_all_elements_located((By.XPATH, '//*[@class="u_cbox_contents"]'))
)

from datetime import datetime
now = datetime.now()
foldername = now.strftime("%m%d_%H%M")

import os
if not os.path.exists('저장할 경로를 지정해주세요' + foldername + '/'):
  os.makedirs('저장할 경로를 지정해주세요' + foldername + '/')

f1 = open('저장할 경로를 지정해주세요' + foldername + '/cussdata.txt', 'a')
f2 = open('저장할 경로를 지정해주세요' + foldername + '/cusslabel.txt', 'a')
f3 = open('저장할 경로를 지정해주세요' + foldername + '/cussurl.txt', 'a')
f3.write(cuss_url)

for element in elements:
  comment = element.text
  if len(comment) > 0:
    print(comment)
    yes_no = input('비난, 평가면 1, 아니면 0: ')
    if(yes_no == ""):
      continue
    while (yes_no != "0") and (yes_no != "1"):
      yes_no = input('다시 입력해주세요: ')
    f1.write(comment + '\n')
    f2.write(yes_no + '\n')

driver.quit()  