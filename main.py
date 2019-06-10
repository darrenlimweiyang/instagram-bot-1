from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import sys

import login


class InstagramBot():


	'''
	List of methods inside InstagramBot:

	1. __init__
	A constructor that takes in a username and password and initiates an instance of instagram bot

	2. sign_in
	Automated sign in to Instagram account using the credentials that object is constructed with

	3. follow_with_user
	takes in a username and follws the particular user

	4. click_no
	Clicks no when promped with notification pop_up upon logging in

	5. getUserFollowers
	takes in a username and a number, getting the usernames of followers until len(list) reaches max

	6. closeBrowser
	quits and closes chrome



	#########
	# TO DO #
	#########

	try block for clicking the "no" button when asked for notifications
	Why? Incase it no longer appears.


	'''

	def __init__(self, email, password):
		'''
		constructor is made of two arguments in order to actually login
		to Instagram
		'''
		path = '/Users/darrentheman/projects/instagram-bot-1/chromedriver'
		self.browser = webdriver.Chrome('/Users/darrentheman/projects/instagram-bot-1/chromedriver') # browser
		self.email = email
		self.password = password

	def sign_in(self):
		'''
		firstly, the browser chrome gets to the login page
		then, it searches for email and password input. they are both of class
		form input.
		email and password is then input.
		'''

		self.browser.get("https://www.instagram.com/accounts/login/?")
		time.sleep(1)
		email_input = self.browser.find_elements_by_css_selector('form input')[0]
		password_input = self.browser.find_elements_by_css_selector('form input')[1]

		for c in self.email:
			email_input.send_keys(c)
			time.sleep(0.1)
		time.sleep(0.5)
		password_input.send_keys(self.password)
		password_input.send_keys(Keys.ENTER)

		time.sleep(2)

	def click_no(self):
		time.sleep(2)
		elem = self.browser.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button[2]")

		elem.click()

	def follow_with_user(self,username):
		self.browser.get('https://www.instagram.com/' + username + '/')
		time.sleep(2)
		followButton = self.browser.find_element_by_css_selector(" #react-root > \
		section > main > div > header > section > div.nZSzR > div.Igw0E.IwRSH.eGOV_._4EzTm > span > span.vBF20._1OSdk > button")
		if followButton.text == "Following" or followButton.text == "Requested":
			time.sleep(2)
		else:
			followButton.click()
			time.sleep(0.3)

	def follow_list(self,list_of_users):
		for users in list_of_users:
			print("following {}".format(users))
			time.sleep(1)
			self.follow_with_user(users)

	def getUserFollowers(self, username, max):

		'''Basically opens browser to a specific user in Instagram'''
		self.browser.get('https://www.instagram.com/' + username + '/')
		time.sleep(2)

		'''Clicks on followers button, opening up a modal'''
		followersLink = self.browser.find_element_by_css_selector('#react-root > \
		 section > main > div > header > section > ul > li:nth-child(2) > a > span')
		followersLink.click() # clicks followers buttons
		time.sleep(2) # sleep after clicking the follower list as some time is needed to load

		'''Gets length of followers loaded already in pop-up/modal'''
		followersList = self.browser.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div.isgrP > ul > div')
		numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))

		'''Checks number of followers already loaded in modal. If < input number, action chain and scrolls down
		Increases the number of followers loaded.'''
		actionChain = webdriver.ActionChains(self.browser)
		while(numberOfFollowersInList < max):
			actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
			numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
			print(numberOfFollowersInList)

		'''adds list of followers in pop_up into final list and returns []'''
		followers = []
		for user in followersList.find_elements_by_css_selector('li'):
			userLink = user.find_element_by_css_selector('a').get_attribute('href')
			followers.append((userLink[26:-1]))
			if len(followers) > max:
				break
		return followers

	def like_all_photos(self, username):
		'''opens instagram profile, scrolls down and clicks first photo, opening modal'''
		self.browser.get('https://www.instagram.com/' + username + '/')
		time.sleep(1.2)
		self.browser.execute_script("window.scrollTo(0, 500)")

		first_photo = self.browser.find_element_by_css_selector("#react-root > \
section > main > div > div._2z6nI > article > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(1) > a > div")
		time.sleep(1)
		first_photo.click()
		time.sleep(6)

		element = self.browser.find_element_by_css_selector("#react-root > section > main > div > header > section > ul > li:nth-child(1) > span > span")
		no_of_posts = element.get_attribute('textContent')

		for i in range(int(no_of_posts)):
			if i == 0:
				like_button = self.browser.find_element_by_css_selector("body > \
				div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button > span")
				like_button.click()
				next_button = self.browser.find_element_by_css_selector("body > \
				div._2dDPU.vCf6V > div.EfHg9 > div > div > a")
				next_button.click()
				time.sleep(4)
			else:
				like_button = self.browser.find_element_by_css_selector("body > \
				div._2dDPU.vCf6V > div.zZYga > div > article > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button > span")
				like_button.click()
				next_button = self.browser.find_element_by_css_selector("body > \
				div._2dDPU.vCf6V > div.EfHg9 > div > div > a.HBoOv.coreSpriteRightPaginationArrow")
				next_button.click()
				time.sleep(4)


	def closeBrowser(self):
		self.browser.close()

	def __exit__(self, exc_type, exc_value, traceback):
		self.closeBrowser()



bot = InstagramBot(login.username, login.password)
# For security purposes, username and password are not shown. 
# Please use your own account, or create one easily. 
bot.sign_in()
bot.click_no()
#bot.like_all_photos("nus_usp")
#bot.follow_with_user("karthiii96")
to_follow = bot.getUserFollowers("therock",25)
#bot.follow_list(to_follow)
#time.sleep(3)
#bot.closeBrowser()
