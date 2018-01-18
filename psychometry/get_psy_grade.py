from selenium import webdriver
import time, os
import send_mail
def main():
    print "start"
    login_url = "https://www.nite.org.il/index.php/he/"
    chromedriver = 'C:\scripts\chromedriver_win32\chromedriver.exe'
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.get("https://www.nite.org.il/index.php/he/")
    time.sleep(4)
    user = driver.find_element_by_name("loginName")
    password = driver.find_element_by_name("loginPwd")
    user.clear()
    password.clear()
    user.send_keys(ID)
    password.send_keys(PASSWORD)
    driver.find_element_by_id("login_submit").click()
    time.sleep(6)
    driver.find_element_by_class_name("top-link").click()
    page_data = driver.page_source.encode('utf-8')
    with open("C:\\temp\\web.html", "rb") as f:
        old_page = f.read()
    if old_page != page_data:
        print "OMG there are changes!!!!"
        send_mail.do_this("somthing just changed with the test!!!")
        with open("C:\\temp\\web.html", "wb") as f:
            f.write(page_data)
    else:
        print "nothing new under the sun..."
    time.sleep(1)
    driver.delete_all_cookies()
    driver.close()
    print "finish :)"


while True:
    main()
    time.sleep(300)
