from twython import Twython
from scrapy.selector import Selector
import requests
from time import sleep

API_KEY = 'ADD_YOUR_CREDENTIALS_HERE'
API_SECRET = 'ADD_YOUR_CREDENTIALS_HERE'
OAUTH_TOKEN = 'ADD_YOUR_CREDENTIALS_HERE'
OAUTH_TOKEN_SECRET = 'ADD_YOUR_CREDENTIALS_HERE'
TWEETER = Twython(API_KEY,API_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)

THN_POST_URL_XPATH = "//a[contains(@class,'page-link')]/@href"
# THN_MSG_TEXT_XPATH = "//div[contains(@class,'tweet-box clear')]//a[contains(@class,'tweet-text')]/text()"
AA_POST_URL_XPATH = "//h2[contains(@class,'article-title')]//a/@href"
AA_POST_HEADING = "//h2[contains(@class,'article-title')]//span[contains(@class,'title-text')]/text()"
start_urls = [
				{'url':'http://www.thehackernews.com','page':'THN'},
				{'url':'http://www.androidauthority.com','page':'AA'}]

data = []


def load_response(url):
	return requests.get(url)

def tweet(msg):
	print "Tweeting...."
	TWEETER.update_status(status = msg)
	print "Tweet done!"


for item in start_urls:
	if item['page'] == 'THN':
		response = load_response(item['url'])
		hxs = Selector(response = response)
		post_links = hxs.xpath(THN_POST_URL_XPATH).extract()
		for post_link in post_links:
			if '?' in post_link:
				post_link = post_link.split('?')[0]
			words = post_link.rsplit('/',1)[1].split('.')[0].split('-')
			
			tweet_message = '#'+' #'.join(words)+' @thehackernews\n'+post_link
			print tweet_message
			tweet(tweet_message)
			sleep(600)
	elif item['page'] == 'AA':
		response = load_response(item['url'])
		hxs = Selector(response=response)
		post_link = hxs.xpath(AA_POST_URL_XPATH).extract()
		heading = hxs.xpath(AA_POST_HEADING).extract()
		tweet_message=''.join(heading)+' @androidauth\n'+' '.join(post_link)
		print tweet_message
		tweet(tweet_message)
		sleep(600)