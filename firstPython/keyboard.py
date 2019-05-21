from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Ie()
driver.get('http://www.baidu.com')

# 输入框输入内容
driver.find_element_by_id("kw").send_keys("seleniumm")

# 删除多输入的一个m
driver.find_element_by_id("kw").send_keys(Keys.BACK_SPACE)

# 输入空格键+"教程"
driver.find_element_by_id("kw").send_keys(Keys.SPACE)
driver.find_element_by_id("kw").send_keys("教程")

# ctrl+a全选输入框内容
driver.find_element_by_id("kw").send_keys(Keys.CONTROL, 'a')

# ctrl+x剪切输入框内容
driver.find_element_by_id("kw").send_keys(Keys.CONTROL, 'x')

# ctrl+v粘贴输入框内容
driver.find_element_by_id("kw").send_keys(Keys.CONTROL, 'v')

# 回车键代替单击操作
driver.find_element_by_id("su").send_keys(Keys.ENTER)

driver.quit()
