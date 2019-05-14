from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Ie()
driver.get('http://yunpan.360.cn')

# 定位要右击的元素
right_click = driver.find_element_by_name("account")
# 对定位的元素进行右击操作
#ActionChains(driver).context_click(right_click).perform()
# 对定位的元素执行双击操作
move = driver.find_element_by_name("password")
ActionChains(driver).move_to_element(move).perform()
#对定位的元素执行双击操作
ActionChains(driver).double_click(move).perform()

#定位元素的原位置
element = driver.find_element_by_id("xx")
target = driver.find_element_by_id("xx")
ActionChains(driver).drag_and_drop(element, target).perform()



