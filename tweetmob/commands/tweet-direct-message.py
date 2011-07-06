import tweepy
from tweepy.error       import TweepError
from tweetmob.log       import log
from tweetmob.config    import db, get_config_value
from tweetmob.commands  import BaseCommand, CommandError

# log message 
RECEIVED_MESSAGE = '''DM #%s was received from @%s 
 at %s and created tweet https://twitter.com/#!/%s/status/%s'''

REJECTED_MESSAGE = '''DM #%s was received from @%s at %s but was rejected due to
 user not being authorized to send tweets'''


class Command(BaseCommand):
    """
    Tweet the direct message from accounts.
    """
    
    # command information
    usage = '--tweet-direct-message'
    summary = __doc__.strip().splitlines()[0].rstrip('.')
     
    def handle(self):
       
        consumer_key = get_config_value('consumer_key')
        consumer_secret = get_config_value('consumer_secret')
        token = get_config_value('token')
        token_secret = get_config_value('token_secret')

        if consumer_key and consumer_secret and token and token_secret:

            conf = db.stored_config()
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(token, token_secret)
            api = tweepy.API(auth)

            count_tweets = 0
            try:
                replies = api.direct_messages()
                for i in range(len(replies),0,-1):
                    r = replies[i-1]
                    for k in [i for i in conf.keys() if 'dm.' in i]:
                        if conf[k] == r.sender_screen_name:
                            print r.text                            
                            direct_message = api.destroy_direct_message(r.id)
                            status = api.update_status(r.text)      
                            
                            count_tweets += 1 
                            message = RECEIVED_MESSAGE % ( r.id,
                                                      r.sender_screen_name,
                                                      r.created_at,
                                                      status.author.screen_name,
                                                      status.id )
                            log(message)
                        else:
                            message = RECEIVED_MESSAGE % ( r.id,
                                                           r.sender_screen_name,
                                                           r.created_at)
                            log(message)
                
                log('Tweets direct messages: %s' % count_tweets)
            except TweepError, e:
                log('Error: %s' % e)

        else:
            print('Not exist credentiales. Please use options\n tweetmob %s' %
                    self.usage)

