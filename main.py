import os
os.system("pip install --upgrade instagrapi")
import instagrapi
from instagrapi import Client
from instagrapi.types import Location, StoryMention, StorySticker, StoryLocation, StoryLink, StoryHashtag
import praw
import re
import requests
import schedule
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import random
from keep_alive import keep_alive
from PIL import Image

username = 'yourdadspod'
password = 'Kobrickson47'
subreddits = ['dankmemes', 'memes', 'EarthPorn', '2meirl4meirl', 'blursedimages', 'wholesomememes', 'Minecraft',
			'forbiddensnacks', 'puns', 'teenagers', 'Intelectuaals', 'BeAmazed', 'Art', 'fakehistoryporn',
			'blessedimages', 'technicallythetruth', 'boomershumor', 'bonehurtingjuice',
			'comedyheaven', 'madlads', 'KamikazeByWords', 'LifeProTips', 'mildlyinteresting', 'mildlyinfuriating',
			'clevercomebacks', 'notinteresting', 'ComedyCemetery', 'meirl', 'trashy', 'MurderedByWords', 'DiWHY',
			'hmmm', 'therewasanattempt', 'Bossfight', 'interestingasfuck',
			'oddlysatisfying', 'MadeMeSmile']
subreddits = ['dankmemes', 'memes', '2meirl4meirl', 'blursedimages', 'puns', 'teenagers', 'blessedimages', 'boomershumor',
			'comedyheaven', 'notinteresting', 'ComedyCemetery', 'meirl', 'DiWHY', 'hmmm']

subreddit = "{None}"
title = "{None}"

def uploadPost():
	global subreddit
	global title
	global success

	for post in reddit.subreddit(subreddits[random.randrange(0, len(subreddits))]).hot(limit=100):
		chance = random.randrange(0, 15)
		#chance = 3
		if chance == 3:
			print("Luck!")
			if post.over_18:
				print("NSFW\n----------------")
				break
			title = post.title
			author = post.author
			subreddit = post.subreddit
			hashtags = title.split()
			hashtags = list(dict.fromkeys(hashtags))
			url = post.url
			file_name = url.split("/")
			if len(file_name) == 0:
				file_name = re.findall("/(.*?)", url)
			file_name = file_name[-1]
			if "." not in file_name:
				file_name += ".jpg"
			if ".jpg" not in file_name or file_name == ".jpg":
				break

			file_name = "img0.jpg"
			r = requests.get(url)
			with open(file_name, "wb") as f:
				f.write(r.content)
			try:
				img = Image.open(file_name)  # open the image file
				img.verify()  # verify that it is, in fact an image
			except (IOError, SyntaxError) as e:
				print('Bad file:', file_name)
				break

			saved_imgs = 10
			for i in range(saved_imgs-1):
				if open("img0.jpg", "rb").read() == open("img"+str(i+1)+".jpg","rb").read():
					print("Image Already Has Been Posted")
					break

			img = Image.open(file_name)
			img.close()
			w, h = img.size
			ratio = float(w)/float(h)
			if ratio > 16/9 or ratio < 3/4:
				print("Unacceptable Ratio\n----------------")
				break
			caption = f"{title}\n\nCredit: u/{author}, on r/{subreddit}\n\n"
			caption += f"#{subreddit} ".lower()
			for i in range(len(hashtags)):
				caption += f"#{hashtags[i]} ".lower()
			caption = caption.ljust(2200).strip()
			print(caption)
			#permission = input("Approve This: Y/N")
			permission = "y"
			if permission == "y":
				print(f"Proceeding to Upload a Post; r/{subreddit}, {title}\n----------------")
				cl.photo_upload(file_name, caption=caption)
				success = True
				for i in range(saved_imgs-1):
					image = Image.open("img"+str(saved_imgs-2-i)+".jpg")
					image.save("img"+str(saved_imgs-1-i)+".jpg")
				print("Successfully Uploaded Picture\n----------------")
				break
			else:
				print("Dissaproved")
				break
		else:
			print("no luck")

def schedulePost():
	global success
	global reddit
	global cl
	success = False
	print("Logging In")
	cl = Client()
	#cl.dump_settings('/tmp/dump.json')
	cl.login(username, password)
	#reddit = praw.Reddit(client_id='06D3hjn_3dy5LA', client_secret='jOpbtPboyLBauppfZ4dTJpa8FUst3Q', user_agent='my user agent')
	reddit = praw.Reddit(client_id='LNwi6N8nTqVTJg', client_secret='cXBYHlgkvhh8phBHLAOAtNZUUpnJmg', user_agent='my user agent')
	print("Logged In")
	while not success:
		try:
			uploadPost()
		except Exception as ex:
			print(ex)
			print(f"r/{subreddit}\n{title}")
			time.sleep(0.1)

def uploadStory():
	cl = Client()
	cl.login(username, password)

	background = Image.open("background.jpg")
	mention = cl.user_info_by_username(username)
	ht = cl.hashtag_info('test')

	cl.photo_upload_to_story(
		path="background.jpg",
		caption="Test (this story was uploaded through a script)",
		mentions=[StoryMention(user=mention, x=0.49892962, y=0.703125, width=0.8333333333333334, height=0.125)],
		#links=[StoryLink(webUri='https://github.com/adw0rd/instagrapi')],
		hashtags=[StoryHashtag(hashtag=ht, x=0.23, y=0.32, width=0.5, height=0.22)],
		#stickers=[StorySticker(id="8", x=0.49892962, y=0.703125, width=0.8333333333333334, height=0.125)]
	)
keep_alive()
schedule.every().day.at("11:00").do(schedulePost)
schedulePost()

while True:
	schedule.run_pending()
	time.sleep(0.5)
