import time
from decouple import config
from django.test import LiveServerTestCase
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


class PublishEntryAutomatedTests(LiveServerTestCase):
	"""
	Automate Test of Publishing a Journal Entry
	"""
	def setUp(self):
		from selenium import webdriver
		self.selenium = webdriver.Chrome(config('CHROMEDRIVER'))

	def tearDown(self):
		self.selenium.quit()

	def test_automated_entry_creation(self):
		selenium = self.selenium
		selenium.get('http://127.0.0.1:8000/login')

		username = selenium.find_element_by_id('id_username')
		password = selenium.find_element_by_id('id_password')
		submit = selenium.find_element_by_class_name('btn')

		username.send_keys(config('TESTUSERNAME'))
		password.send_keys(config('TESTPASSWORD'))
		submit.submit()

		time.sleep(5)

		create_btn = selenium.find_element_by_class_name('btn-floating')

		create_btn.click()

		time.sleep(3)

		assert 'Publish' in selenium.page_source

		title = selenium.find_element_by_id('id_title')
		tag = selenium.find_element_by_class_name('taggle_input')
		submit = selenium.find_element_by_class_name('btn')
		actions = ActionChains(selenium)

		time.sleep(3)

		input_title = 'Automated Tested Title'
		input_text = 'Automated Tested Text'
		input_tag1 = 'Automation'
		input_tag2 = 'Testing'
		input_tag3 = 'Selenium'

		title.send_keys(input_title)

		actions.send_keys(Keys.TAB)
		actions.perform()
		actions.send_keys(input_text)
		actions.perform()
		time.sleep(2)

		tag.send_keys(input_tag1)
		actions.send_keys(Keys.TAB)
		actions.perform()
		time.sleep(2)

		tag.send_keys(input_tag2)
		actions.send_keys(Keys.TAB)
		actions.perform()
		time.sleep(2)

		tag.send_keys(input_tag3)
		actions.send_keys(Keys.TAB)
		actions.perform()
		time.sleep(2)

		submit.submit()

		time.sleep(5)

		assert input_title in selenium.page_source

		assert input_text in selenium.page_source
