import tweepy
from tweetmob.config    import db
from tweetmob.commands  import BaseCommand, CommandError

__consumer_key__    = 'emeuDovYLyZVQWnMZlqcg'
__consumer_secret__ = 'KKll6SEigcb7BFhqkoiqkXR7dmJGEdaPncaGto5BI'

class Command(BaseCommand):
    """
    Get the credentials of authenticate.
    """
    
    # command information
    usage = '--get-credentials'
    summary = __doc__.strip().splitlines()[0].rstrip('.')
     
    def handle(self):

        auth = tweepy.OAuthHandler(__consumer_key__, __consumer_secret__)

        # User pastes this into their browser to bring back a pin number        
        print("Please, copy & paste this URL to your web browser:\n")
        print(auth.get_authorization_url())
        print("\nYou'll have to authorize the 'tweetmob' app and then copy and paste the given PIN here.\n")

        # Get the pin # from the user and get our permanent credentials
        oauth_verifier = raw_input('What is the PIN? ')
        auth.get_access_token(oauth_verifier)

        conf = db.stored_config()
        conf['consumer_key']    = __consumer_key__
        conf['consumer_secret'] = __consumer_secret__
        conf['token']           = auth.access_token.key
        conf['token_secret']    = auth.access_token.secret

        print('Credentials added.')
