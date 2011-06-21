# -*- coding: utf-8-*-

import sys
import os
import uuid
import tweepy
#import urllib2
#import oauth2 as oauth
#from oauthtwitter       import OAuthApi
from tweepy.error import TweepError
from guachi             import ConfigMapper
from tweetmob.argopts   import ArgOpts

__consumer_key__    = 'emeuDovYLyZVQWnMZlqcg'
__consumer_secret__ = 'KKll6SEigcb7BFhqkoiqkXR7dmJGEdaPncaGto5BI'
__version__         = '0.0.1'

# Fixes Database Absolute Location
FILE_CWD = os.path.abspath(__file__)
FILE_DIR = os.path.dirname(FILE_CWD)
DB_FILE = FILE_DIR+'/tweetmob.db'

# MESSAGE

MSG_REJECTED = '''DM #{0} was received from {1} at {2} but was rejected due to
 user not being authorized to send tweets'''

MSG_CREATED = '''DM #{0} was received from @{1} at {2} and created tweet 
https://twitter.com/#!/{2}/status/{3}'''

class TweetmobCommands(object):

    tweetmob_help = """
tweetmob: Communicate privately via Twitter

Version: %s

Run:
    tweetmob [options]  

Options:
    --version, version      Shows the current installed version.
    --log-file              The log file to write to. [-]
    --log-level             The granularity of log outputs. [info]
    --config-values         Displays the current configuration values used.
    --get-name-account      Displays the current name of the account.
    --get-credentials       Get the credentials of authenticate.
    --add-account           Add account receive direct message.
    --del-account           Delete account direct message.
    --tweet-direct-message  Tweet the direct message from accounts.
    """ % __version__

    ENCODING = 'utf8'

    def __init__(self, argv=None, parse=True, test=False, 
                    db=ConfigMapper(DB_FILE)):
        
        self.db = db
        self.test = test

        self.auth = tweepy.OAuthHandler(__consumer_key__,
                                        __consumer_secret__)

        if argv is None:
            argv = sys.argv
        if parse:
            self.parseArgs(argv)

    def msg(self, msg, stdout=True):
        if stdout:
            sys.stdout.write(msg+'\n')
        else:
            sys.stderr.write(msg+'\n')
        if not self.test:
            sys.exit(1)


    def set_item_config(self, key, value):
        conf = self.db.stored_config()
        conf[key] = value
        return conf[key]


    def get_item_config(self, key):
        conf = self.db.stored_config()
        try:
            value = conf[key]
        except KeyError:
            value = None

        return value

    def del_item_config(self, key):
        conf = self.db.stored_config()
        value = True
        try:
            del conf[key]
        except KeyError:
            value = False

        return value


    def get_keys_config(self):
        conf = self.db.stored_config()
        return conf.keys()

    
    def processHTTPError(self, e, custom_messages={}):
        if e.code == 400:
            if custom_messages.has_key(400):
                error_msg = custom_messages[400]
            else:
                error_msg  = "Twitter returned a \"Bad Request\" error. "
                error_msg += "This happens when you exceed 70 requests pero hour. "
                error_msg += "Avoid running other Twitter applications or refreshing too frequently."

        if e.code == 401:
            if custom_messages.has_key(401):
                error_msg = custom_messages[401]
            else:
                error_msg = "Twitter returned an \"Unauthorized\" error. "
                error_msg += "This happens when you're not authenticated, your credentials aren't valid "
                error_msg += "or you don't have the required authorization level to perform the requested operation."

        elif e.code == 403:
            if custom_messages.has_key(403):
                error_msg = custom_messages[403]
            else:
                error_msg  = "Twitter returned a \"Forbidden\" error. "
                error_msg += "This means you don't have permission to perform the requested operation."

        elif e.code == 404:
            if custom_messages.has_key(404):
                error_msg = custom_messages[404]
            else:
                error_msg  = "Twitter returned an \"Object Not Found\" error. "
                error_msg += "This means the resource you're trying to access does not exist."

        elif e.code == 500:
            if custom_message.has_key(500):
                error_msg = custom_messages[500]
            else:
                error_msg  = "Twitter returned an \"Internal Server Error\" error. "
                error_msg  = "This means the servers at Twitter are having some problems. "
                error_msg += "Please try again this operation in a few minutes."        
                error_msg += "If the error persists consider reporting the problem to the Twitter team."

        elif e.code == 502:
            if custom_message.has_key(502):
                error_msg = custom_messages[502]
            else:
                error_msg  = "Twitter returned a \"Bad Gateway\" error. "
                error_msg += "This normally means the servers at Twitter are down "
                error_msg += "or under mantainance."        
    
        elif e.code == 503:
            if custom_message.has_key(503):
                error_msg = custom_messages[503]
            else:
                error_msg  = "Twitter returned a \"Service Unavailable\" error. "
                error_msg += "This normally means the servers at Twitter are up "
                error_msg += "but overloaded with request. "        
                error_msg += "Please retry this operation later."        
        else:
            error_msg = e.message

        self.msg(error_msg, stdout=False)


    def get_credentials(self):
        
        # User pastes this into their browser to bring back a pin number        
        print("Please, copy & paste this URL to your web browser:\n")
        print(self.auth.get_authorization_url())
        print("\nYou'll have to authorize the 'tweetmob' app and then copy and paste the given PIN here.\n")

        # Get the pin # from the user and get our permanent credentials
        oauth_verifier = raw_input('What is the PIN? ')
        auth.get_access_token(oauth_verifier)
        self.set_item_config('consumer_key', __consumer_key__)
        self.set_item_config('consumer_secret', __consumer_secret__)
        self.set_item_config('token',  self.auth.access_token.key)
        self.set_item_config('token_secret', self.auth.access_token.secret)
        self.msg('Credentials added.')


    def config_values(self):
        conf = self.db.stored_config()
        try:
            for i in conf.items():
                print "%-15s= %-4s" % (i[0], i[1])
            print ''
        except Exception, error:
            self.msg("Could not complete command: %s" % error, stdout=False) 

    def get_me(self):
        conf = self.db.stored_config()
        try:
            token = conf['token']
        except KeyError:
            token = None

        try:
            token_secret = conf['token_secret']
        except KeyError:
            token_secret = None

        if token and token_secret:
            self.auth.set_access_token(token,token_secret)
            api = tweepy.API(self.auth)
            me = api.me()
            print dir(me)

    def tweet_direct_message(self):
        conf = self.db.stored_config()
        try:
            token = conf['token']
        except KeyError:
            token = None

        try:
            token_secret = conf['token_secret']
        except KeyError:
            token_secret = None

        if token and token_secret:

            self.auth.set_access_token(token,token_secret)
            api = tweepy.API(self.auth)

            count_tweets = 0
            try:
                replies = api.direct_messages()
                for i in range(len(replies),0,-1):
                    r = replies[i-1]
                    for k in [i for i in conf.keys() if 'dm.' in i]:
                        if conf[k] == r.sender_screen_name:
                            print r.text                            
                            status = api.update_status(r.text)
                            
                            #direct_message = api.DestroyDirectMessage(r.id)
                            count_tweets += 1
                        else:
                            print MSG_REJECTED
                            #self.msg('msg')

                self.msg('Tweets direct messages: %s' % count_tweets)
            except TweepError:
                pass

        else:
            self.msg('Not exist credentiales. Please use options\n tweetmob --get-credentials',stdout=False)

    def parseArgs(self, argv):
        options = ['--log-file',
                   '--log-level',
                   '--config-values',                   
                   '--get-name-account',
                   '--get-credentials',
                   '--add-account',
                   '--del-account',
                   '--tweet-direct-message']

        args = ArgOpts(options)
        args.parse_args(argv)
        
        if args.catches_help():
            self.msg(self.tweetmob_help)

        if args.catches_version():
            message = "Tweetmob version %s" % __version__
            self.msg(message)  
            
        if args.match:

            # Matches for --log-file
            if args.has('--log-file'):
                log_file = args.get_value('--log-file')
                if log_file is None:
                    self.del_item_config('log_file')
                else:
                    self.set_item_config('log_file', log_file)

            # Matches for --log-level
            if args.has('--log-level'):
                log_level = args.get_value('--log-level')
                if log_level is None:
                    self.del_item_config('log_level')
                else:
                    self.set_item_config('log_level', log_level)

            # Matches for --config-value
            if args.has('--config-values'):
                self.config_values()
            
            # Matches for --get-name-account
            if args.has('--get-name-account'):
                self.get_me()

            # Matches for --get-credentials
            if args.has('--get-credentials'):
                self.get_credentials()
                            
            # Matches for --add-ccount
            if args.has('--add-account'):
                account = args.get_value('--add-account')
                self.set_item_config('dm.%s' % str(uuid.uuid4()), account)

            # Matches for --del-account
            if args.has('--del-account'):
                account = args.get_value('--del-account')
                conf = self.db.stored_config()
                try:
                    for k in [i for i in conf.keys() if 'dm.' in i]:
                        if conf[k] == account:
                            del conf[k]
                except Exception, error:
                    self.msg("Could not complete command: %s" % error, stdout=False) 

            # Matches for --tweet-direct-message
            if args.has('--tweet-direct-message'):
                self.tweet_direct_message()
                                
        else:
            self.msg(self.tweetmob_help)
