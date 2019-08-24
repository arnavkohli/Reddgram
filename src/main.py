#!/usr/bin/python3.6
import praw
from instapy_cli import client

from Post import Post
from Reddgram import Reddgram
from InstaPy import InstaPy


client_id="cfY_8XnvN7Cmjg"
client_secret="uzeVwNY5MlLdIc2CdFTSZkWGruw"
password="bB9KJSyrjyfPabT"
user_agent='testscript by /u/iamb1izzy'
username='iamb1izzy'

ig_username = 'bot_o_rum'
ig_password = 'AmazingI101'

rs = Reddgram(CLIENT_ID=client_id,
					SEC_ID=client_secret,
					PASSWORD=password,
					USERAGENT=user_agent,
					USERNAME=username,
					IG_USERNAME=ig_username,
					IG_PASSWORD=ig_password,
					SUBREDDITS=['ProgrammerHumour', 'programmingmemes', 'shittyprogramming']
					)
rs.run()