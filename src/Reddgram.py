import praw, datetime, time, json, random
from Post import Post
from InstaPy import InstaPy
from Cleaner import Cleaner
import os

class Reddgram:

    def __init__(self, CLIENT_ID, SEC_ID, PASSWORD, USERAGENT, USERNAME, IG_USERNAME, IG_PASSWORD,
                        SUBREDDITS, MAX_POSTS=1, MAX_DOWNLOAD_LIMIT=10):

        #Reddit Login
        self.CLIENT_ID       = CLIENT_ID
        self.CLIENT_SECURITY = SEC_ID
        self.PASSWORD        = PASSWORD
        self.USER_AGENT      = USERAGENT
        self.REDDIT_USERNAME = USERNAME
        self.REDDIT          = praw.Reddit( client_id     = self.CLIENT_ID,
                                            client_secret = self.CLIENT_SECURITY,
                                            password      = self.PASSWORD,
                                            user_agent    = self.USER_AGENT,
                                            username      = self.REDDIT_USERNAME)
        self.MAX_POSTS = MAX_POSTS
        self.MAX_DOWNLOAD_LIMIT = MAX_DOWNLOAD_LIMIT
        self.DASH = '-'*40
        self.SUBREDDITS = SUBREDDITS
        self.COUNT = 0

        #PRIVATE INFO
        self.IG_USERNAME = IG_USERNAME
        self.IG_PASSWORD = IG_PASSWORD

    def postToIG(self, posts, repeated = 0):
        sub_ids = []
        failed = 0
        for p in posts:
            try:
                """
                Uncomment below line to enable uploading.

                """
                self.upload(post=p)
                sub_ids.append(p.sub_id)
            # except Exception as e:
            #     print (e)
            #     continue
            except Exception as e:
                print ("EXCEPTION: {}".format(e))
                failed += 1
                if failed == 10:
                    if repeated == 3:
                        print ("Falied to retrieve even after trying {} times".format(repeated))
                        break
                    print ('Trying again...')
                    return self.postToIG(self.getInfo(self.getSubreddit(self.SUBREDDITS[random.randint(0, len(self.SUBREDDITS) - 1)])), repeated + 1)

                print ('FAILED: {} ({})'.format(p.title, p.subreddit))
                continue

            print ("{}. {}".format(self.COUNT + 1, p.title))
            self.COUNT += 1
            if (self.COUNT == self.MAX_POSTS):
                break

        with open(os.path.join(os.getcwd(),"cache.json"), 'r') as outfile:
            lines = outfile.readlines()
            for line in lines:
                eye_d = ''
                started = False
                for ele in line:
                    if ele == '"' and started:
                        sub_ids.append(eye_d)
                        eye_d = ''
                        started = False
                    elif ele == '"' and started == False:
                        started = True
                    elif started:
                        eye_d += ele
                        continue

        with open(os.path.join(os.getcwd(),"cache.json"), 'w') as outfile:
            json.dump(sub_ids, outfile)

    def run(self):

        #AUTHENTICATION
        if self.auth():
            print (self.DASH)
            print ('Reddit Authentication Successful.\nWelcome, {}'.format(self.REDDIT_USERNAME))

        #Get a Subreddit randomly from the pool
        r = random.randint(0, len(self.SUBREDDITS) - 1)
        subreddit = self.getSubreddit(self.SUBREDDITS[r])

        #Get posts of the required subreddit
        posts = self.getSubInfo(subreddit)

        print (self.DASH)
        print ("Starting uploads...")
        print (self.DASH)

        self.postToIG(posts)

        print ('Uploaded {} posts'.format(self.COUNT))

        print ('Starting cleaner..')
        Cleaner.clean()


    def upload(self, post):
        InstaPy.post(usr=self.IG_USERNAME, pwd=self.IG_PASSWORD, post=post)

    def auth(self):
        if self.REDDIT.user.me() == self.REDDIT_USERNAME:
            return True

    def getSubreddit(self, name):
        return self.REDDIT.subreddit(name)


    def getSubInfo(self, subreddit):
        posts = []
        for sub in subreddit.rising(limit=self.MAX_DOWNLOAD_LIMIT):
            title   = sub.title
            img_url = sub.url
            sub_id  = sub.id
            subred  = subreddit.display_name
            posts.append(Post(title, img_url, sub_id, subred))
        return posts
