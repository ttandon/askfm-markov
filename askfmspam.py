##tanman - 2014. ask.fm spammer.
import random
import requests, urllib, re
from randomtext import compiler
import time

sess = requests.Session()
sess.get('http://ask.fm') #set session cookie
sess.headers.update({'User-Agent': 'Mozilla/5.0'})
home_source = sess.get('http://ask.fm').text.encode('utf-8')
auth_token = re.search('var AUTH_TOKEN = "(.*?)"', home_source).group(1)

##if we've been marked with a captcha, check and stop the process for a while until captcha is gone
def ip_ban_checker(user):
	bool_val = False
	url = "http://ask.fm/" + user
	import urllib2
	response = urllib2.urlopen(url)
	html = response.read()
	if '(type the code from the image)' in html:
		bool_val = True
	response.close()  # best practice to close the file
	return bool_val

def ask_question(user, question):
	question = urllib.quote(question)
	r = sess.post('http://ask.fm/%s/questions/create?authenticity_token=%s&authenticity_token=%s&question%%5Bquestion_text%%5D=%s' % (user, auth_token, auth_token, question))

def load_user_index(filename):
	with open(filename, 'r') as f:
		myNames = [line.strip() for line in f]
	return myNames
##spread out attack
def runner():
	users = load_user_index("usrindex.txt")
	print users
	##while true
		##loop through users and ask them a random markov generated question
	while(True):
		for user in users:
			if(ip_ban_checker(user) == True):
				print "looks like i was blocked, dw ill wait for 10 minutes and then restart."
				time.sleep(600)
			rand_text = compiler()
			print "[" + user + ", " + rand_text + "]"
			ask_question(user, rand_text)
			time.sleep(10)
##high volume attack on specific user
def target(user):
	for i in xrange(1,50):
		if(ip_ban_checker(user) == True):
			print "looks like i was blocked, dw ill wait for 10 minutes and then restart."
			time.sleep(600)	
		rand_text = compiler()
		print "[" + user + ", " + rand_text + "]"
		ask_question(user, rand_text)
##selects a random user from the index, and flash floods
def random_flood():
	while(True):
		users = load_user_index("usrindex.txt")
		user = random.choice(users)
		target(user)

random_flood()
##runner()
##ask_question("tansanity", "hey man!")