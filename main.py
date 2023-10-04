import os
import time
import smtplib
from keys import password, user, to, zip
from email.message import EmailMessage
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

os.environ['PATH'] += r'F:/Programs/seleniumdriver/firefox'
driver = webdriver.Firefox()
driver.implicitly_wait(20)

def load_page():
  driver.get("https://www.apple.com/shop/buy-iphone/iphone-15-pro")

def click_through():
  model = driver.find_elements(By.CSS_SELECTOR, '.rc-dimension-selector-row')[1]
  model.click()
  color = driver.find_elements(By.CSS_SELECTOR, '.colornav-item')[0]
  color.click()
  storage = driver.find_elements(By.CSS_SELECTOR, '.rc-dimension-selector-row')[2]
  storage.click()
  tradeIn = driver.find_element(By.ID, "noTradeIn")
  tradeIn.click()
  paymentOption = driver.find_element(By.CSS_SELECTOR, "span[data-autom='purchaseGroupOptionfullprice_price']")
  paymentOption.click()
  connectivity = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@data-autom='carrierModelUNLOCKED/US']/following-sibling::*"))).click()
  try:
    applecare = driver.find_element(By.ID, 'applecareplus_59_noapplecare_label')
    applecare.click()
  except ElementNotInteractableException:
    record('Element not interactble error\n')
  search = driver.find_element(By.CSS_SELECTOR, ".retail-availability-search-trigger")
  search.click()
  zipCode = driver.find_element(By.CSS_SELECTOR, "[data-autom='zipCode']")
  time.sleep(2)
  while(len(zipCode.get_attribute('value')) > 0):
    zipCode.send_keys(Keys.BACK_SPACE)
  zipCode.send_keys(zip)
  zipCode.send_keys(Keys.ENTER)

def check_availability(color:str , gigs: str):
  availmsg = ''
  available = isAvailable()
  if available:
    store_locator = driver.find_elements(By.CSS_SELECTOR, '.rf-productlocator-stores .form-selector-label span.row')
    for i in range(len(store_locator)):
      rightInfo = store_locator[i].find_elements(By.CSS_SELECTOR, '.form-selector-right-col span')[0]
      if rightInfo.get_attribute('innerText') == 'Currently unavailable':
        break
      else :
        leftInfo = store_locator[i].find_elements(By.CSS_SELECTOR, '.form-selector-left-col span')
        avail = ''
        for left in leftInfo:
          avail = avail + ' ' + left.get_attribute('innerText')
        availmsg += f'{color} {gigs}GB at{avail}\n'
  return availmsg

def isAvailable():
  try:
    driver.find_element(By.CLASS_NAME, 'rf-productlocator-buttontitle')
  except NoSuchElementException:
   return True
  return False

def check_each():
  notification_msg = ''
  record('checking...\n')
  timer = 5
  color = ['Natural', 'Blue', "White", 'Black']
  notification_msg += check_availability(color[0], '256')
  twoFiftySix = driver.find_elements(By.CSS_SELECTOR, '.rc-overlay-popup-content .rf-productlocator-filter-dimensiongroup .form-selector-label')[2]
  fiveTwelve = driver.find_elements(By.CSS_SELECTOR, '.rc-overlay-popup-content .rf-productlocator-filter-dimensiongroup .form-selector-label')[3]
  time.sleep(timer)
  fiveTwelve.click()
  notification_msg += check_availability(color[0], '512')
  gigs = '512'
  for i in range(1,4):
    time.sleep(timer)
    colorButton = driver.find_elements(By.CSS_SELECTOR, '.rc-overlay-popup-content .colornav-item')[i]
    colorButton.click()
    notification_msg += check_availability(color[i], gigs)
    time.sleep(timer)
    if i % 2 == 0:
      fiveTwelve.click()
      gigs = '512'
      notification_msg += check_availability(color[i], '512')
    else:
      twoFiftySix.click()
      gigs = '256'
      notification_msg += check_availability(color[i], '256')
  record(notification_msg)
  if len(notification_msg) > 0:
    sendEmail('Phones available', notification_msg)

def get_date():
  now = datetime.now()
  dt_string = now.strftime("%m/%d/%Y %I:%M:%S %p")
  record(f'{dt_string}\n')

def record(msg:str):
  with open('something.txt', 'a') as file:
    file.write(msg)

def sendEmail(subject, body):
  msg = EmailMessage()
  msg.set_content(body)
  msg['Subject'] = subject
  msg['From'] = user
  msg['To'] = to

  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login(user, password)
  server.send_message(msg)

  server.quit()

if __name__ == '__main__':
  get_date()
  load_page()
  click_through()
  check_each()
  driver.quit()