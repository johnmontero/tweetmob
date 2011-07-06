import uuid
from tweetmob.config    import db
from tweetmob.commands  import BaseCommand, CommandError

class Command(BaseCommand):
    """
    Add account receive direct message.    
    $ tweetmod --account-add account
    """
    
    # command information
    usage = '--account-add name'
    summary = __doc__.strip().splitlines()[0].rstrip('.')
     
    def handle(self):
        
        conf = db.stored_config()        
        account = self.args.get_value('--account-add')
        if account is not None:
            for k in [i for i in conf.keys() if 'dm.' in i]:
                if conf[k] == account:
                    error("Account %s exist.\n" % account )
            conf['dm.%s' % str(uuid.uuid4())] = account
        else:
            raise CommandError("Please use options\n tweetmob %s" % self.usage)
