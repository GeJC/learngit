from selenium import webdriver

driver = webdriver.Ie()
# driver.get('http://www.baidu.com')

# driver.find_element_by_id("kw").clear()
# driver.find_element_by_id("kw").send_keys("python")
# driver.find_element_by_id("su").click()
# driver.find_element_by_link_text("图片").click()

# driver.get('http://www.youdao.com')
# driver.find_element_by_name('q').send_keys('hello')
# driver.find_element_by_name('q').submit()

driver.get('http://www.baidu.com')
# 获取输入框尺寸
size = driver.find_element_by_id("kw").size
print(size)

# 返回百度页面底部备案信息
text = driver.find_element_by_id("cp").text
print(text)

# 返回元素的属性值，可以使ID,name,type或其他任意属性
attribute = driver.find_element_by_id("kw").get_attribute('type')
print(attribute)

# 返回元素的结果是否可见，返回结果为true或者false
result = driver.find_element_by_id("kw").is_displayed()
print(result)

# driver.quit()
