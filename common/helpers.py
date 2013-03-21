from django.conf import settings
from boto.s3.connection import S3Connection
from boto.s3.key import Key

from accounts.models import *
from django.conf import settings
from urllib import urlretrieve

import md5, os, requests


def put_profile_pic(url, profile):
    """
    Takes a url from filepicker and uploads
    it to our aws s3 account.
    """
    try:
        r = requests.get(url)
        size = r.headers.get('content-length')
        if int(size) > 10000000: #greater than a 1mb #patlsotw
            return False 

        filename, headers = urlretrieve(url + "/resize?w=600&h=600")
        resize_filename, headers = urlretrieve(url + "/resize?w=40&h=40") # store profile sized picture (40x40px)
        conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        b = conn.get_bucket(settings.AWS_BUCK)
        k = Key(b)
        k.key = md5.new(profile.user.username).hexdigest()
        k.set_contents_from_filename(filename) 
        k.set_acl('public-read')

        k = Key(b)
        k.key = md5.new(profile.user.username + "resize").hexdigest()
        k.set_contents_from_filename(resize_filename) 
        k.set_acl('public-read')
    except Exception as e:
        print e
        return False
    #update user profile
    return "http://s3.amazonaws.com/%s/%s"% (settings.AWS_BUCK, k.key)

