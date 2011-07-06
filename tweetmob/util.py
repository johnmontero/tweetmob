import os
import sys
import types

def get_commands():
    """
    Returns a list of all the command names that are available.

    Returns an empty list if no commands are defined.
    """
    command_dir = os.path.join('/'.join(__file__.split('/')[:-1]), 'commands')
    try:
        return [f[:-3] for f in os.listdir(command_dir)
                if not f.startswith('_') and f.endswith('.py')]
    except OSError:
        return []


def load_command_class(name):
    full_name = 'tweetmob.commands.%s' % name
    __import__(full_name)
    return sys.modules[full_name].Command()


def run_command(command):
    try:
        klass = load_command_class(command)
    except (KeyError, ImportError):
        sys.stderr.write("Unknown command: %r\nType 'tweetmob' for usage.\n" % \
                (command))
        sys.exit(1)
    return klass


def out(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()


def err(msg):
    sys.stderr.write(msg)
    sys.stderr.flush()


def error(msg, exit=True):
    err("ERROR: %s" % msg)
    if exit:
        sys.exit(1)

get_sumary_commad = lambda command: load_command_class(command).summary
