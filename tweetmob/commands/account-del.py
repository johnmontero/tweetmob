from tweetmob.config    import db
from tweetmob.commands  import BaseCommand, CommandError

class Command(BaseCommand):
    """
    Delete account direct message.
    """
    
    # command information
    usage = '--account-del name'
    summary = __doc__.strip().splitlines()[0].rstrip('.')
     
    def handle(self):
       
        conf = db.stored_config()
        account = self.args.get_value('--account-del')
        if account is None:        
            print "Please use options\n tweetmob %s" % self.usage
        else:
            try:
                for k in [i for i in conf.keys() if 'dm.' in i]:
                    if conf[k] == account:
                        del conf[k]
            except Exception, error:
                raise CommandError("Could not complete command: %s" % error)
