# -*- coding: utf-8-*-

import sys
from tweetmob.argopts   import ArgOpts
from tweetmob.commands  import CommandError
from tweetmob.util      import get_commands, run_command, get_sumary_commad
from tweetmob.util      import out, error

__version__         = '0.0.2'

class TweetmobCommands(object):

    tweetmob_help = """
TweetMob: Communicate privately via Twitter

Version: %s

Run:
    tweetmob [options]  

Options:
    --version, version      Shows the current installed version.
""" % __version__


    def __init__(self, argv=None, test=True):
        self.test = test
        
        if argv is None:
            argv = sys.argv

        self.parseArgs(argv)

    def parseArgs(self, argv):

        commands    = get_commands()
        commands.sort()
        options  = ['--%s' % cmd for cmd in commands]
        options_help = ['    --%-20s  %-5s' % (cmd, get_sumary_commad(cmd))
                         for cmd in commands]

        self.tweetmob_help += '\n'.join(options_help)+'\n\n'
        
        args = ArgOpts(options)
        args.parse_args(argv)
                        
        if args.catches_help():
            out(self.tweetmob_help)

        elif args.catches_version():
            message = "TweetMob version %s\n" % __version__
            out(message)

        elif args.match:
            try:
                try:
                    run_command(args.match[0][2:]).execute(args)
                except CommandError, e:
                    error('%s\n' % e)
            except KeyboardInterrupt:
                out("Exiting from TweetMob.\n")
        else:
            out(self.tweetmob_help)

