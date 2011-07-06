import tweepy
from tweepy.error       import TweepError
from tweetmob.config    import get_config_value
from tweetmob.commands  import BaseCommand, CommandError

class Command(BaseCommand):
    """
    Display information of me o account.
    """
    
    # command information
    usage = '--account-info [name]'
    summary = __doc__.strip().splitlines()[0].rstrip('.')
     
    def handle(self):
        consumer_key = get_config_value('consumer_key')
        consumer_secret = get_config_value('consumer_secret')
        token = get_config_value('token')
        token_secret = get_config_value('token_secret')

        if consumer_key and consumer_secret and token and token_secret:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(token, token_secret)
            api = tweepy.API(auth)

            account = self.args.get_value('--account-info')
           
            print "Retriving information ..."
            print "done."
            try:
                if account is None:
                    user_info = api.me()
                else:
                    user_info = api.get_user(account)
                    
                print "User Id    : %d" % user_info.id
                print "Screen name: %s" % user_info.screen_name
                print "Full name  : %s" % user_info.name
                print "Description: %s" % user_info.name
                print "URL        : %s" % user_info.url
                
            except TweepError:
                pass
        else:
            print('Not exist credentiales. Please use options\n tweetmob %s' %
                    self.usage)