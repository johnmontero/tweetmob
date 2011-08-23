from tweetmob.config    import db
from tweetmob.commands  import BaseCommand, CommandError

class Command(BaseCommand):
    """
    Displays the current accounts registered.
    """
    
    # command information
    usage = '--account-list'
    summary = __doc__.strip().splitlines()[0].rstrip('.')
     
    def handle(self):
       
        conf = db.stored_config()
        try:
            print "List of accounts registered:"
            print "----------------------------"            
            for k in [i for i in conf.keys() if 'dm.' in i]:
                print "%-15s = %-4s" % (k, conf[k])
            print ''
        except Exception, error:
            raise CommandError("Could not complete command: %s" % error)
