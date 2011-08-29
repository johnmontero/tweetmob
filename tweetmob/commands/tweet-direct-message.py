import pdb
import logging
import time
import tweepy 
from tweepy.error       import TweepError
from tweetmob.config    import db, get_config_value
from tweetmob.config    import db_published, get_published_value
from tweetmob.commands  import BaseCommand, CommandError

LOG_FILE = get_config_value('log_file')

if LOG_FILE is None:
    logging.basicConfig(
        format='%(asctime)-15s - %(levelname)-8s : %(message)s',
        level=logging.INFO
    )
else:
    logging.basicConfig(
        format='%(asctime)-15s - %(levelname)-8s : %(message)s',
        filename=LOG_FILE,
        level=logging.INFO
    )
     
log = logging.getLogger('TweetMob')

# log message 
RECEIVED_MESSAGE = 'DM #%s was received from @%s\
 at %s and created tweet https://twitter.com/#!/%s/status/%s'

REJECTED_MESSAGE = 'DM #%s was received from @%s at %s but was rejected due to\
 user not being authorized to send tweets'


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
                #pdb.set_trace()
                
                tweet_published = db_published.stored_config()
                
                for i in range(len(replies),0,-1):
                    r = replies[i-1]
                    try:
                        value = tweet_published['tweet.%s.%s' %\
                                         (r.sender_screen_name, r.id)]
                    except KeyError:
                        value = None
                            
                    for k in [i for i in conf.keys() if 'dm.' in i]:    
                        if conf[k] == r.sender_screen_name:
                            if value is None:
                                tweet_published['tweet.%s.%s' %\
                                         (r.id, r.sender_screen_name)] =\
                                     'Published: %s' % time.asctime()
                                try:
                                    status = api.update_status(r.text)      
                            
                                    count_tweets += 1 
                                    message = RECEIVED_MESSAGE % ( r.id,
                                                      r.sender_screen_name,
                                                      r.created_at,
                                                      status.author.screen_name,
                                                      status.id )
                                    log.info(message)
                                except TweepError, e:
                                    log.error(e)
                        else:    
                            if value is None:
                                message = REJECTED_MESSAGE % ( r.id,
                                                           r.sender_screen_name,
                                                           r.created_at )
                                log.info(message)
                if count_tweets > 0:
                    log.info('Tweets direct messages: %s' % count_tweets)

            except TweepError, e:
                log.error(e)

        else:
            print('Not exist credentiales. Please use options\n tweetmob %s' %
                    self.usage)

