from tweetmob.config    import db
from tweetmob.commands  import BaseCommand, CommandError

class Command(BaseCommand):
    """
    The log file to write to [-].
    """
    
    # command information
    usage = '--logfile /path/to/file.log'
    summary = __doc__.strip().splitlines()[0].rstrip('.')
     
    def handle(self):
        
        conf = db.stored_config()        
        value = self.args.get_value('--log-file')
        if value is None:
            try:
                del conf['log_file'] 
            except KeyError:
                pass
        else:
            conf['log_file'] = value
