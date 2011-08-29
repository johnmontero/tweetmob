from tweetmob.config    import db_published
from tweetmob.commands  import BaseCommand, CommandError

class Command(BaseCommand):
    """
    Displays the tweets published.
    """
    
    # command information
    usage = '--log-tweet-published'
    summary = __doc__.strip().splitlines()[0].rstrip('.')
     
    def handle(self):
        
        tweet_published = db_published.stored_config()
        try:
            for i in tweet_published.items():
                print "%-15s= %-4s" % (i[0], i[1])
            print ''
        except Exception, error:
            raise CommandError("Could not complete command: %s" % error)
