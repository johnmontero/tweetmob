class ObjectFromDict(object):

    def __init__(self, d):
        for k,v in d.iteritems():
            if type(v) == type({}):
                self.__dict__[k] = ObjectFromDict(v)
            else:
                self.__dict__[k] = v
