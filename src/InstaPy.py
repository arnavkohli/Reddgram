from instapy_cli import client
import json

class InstaPy:
    @staticmethod
    def post(usr, pwd, post):
        with open('cache.json', 'r') as cache:
            print ('inside file')
            lines = cache.readlines()
            for line in lines:
                if post.sub_id in line:
                    raise ValueError('Duplicate Post!')
        cap = str(post.title)
        tags = '\n\n#developer #coding #programmer #programming #webdeveloper #code #java #coder #javascript #html #technology #webdevelopment #softwaredeveloper #css #software #computerscience #design #tech #webdesign #php #development #dev #python #webdev #developers #softwareengineer #computer #web #developerlife'

        cap = cap + tags

        print ('Valid caption')
        with client(usr, pwd) as cli:
            cli.upload(post.img_url, cap)