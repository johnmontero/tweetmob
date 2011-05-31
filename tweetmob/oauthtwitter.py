#!/usr/bin/env python
# 
# Copyright under  the latest Apache License 2.0

'''
A modification of the python twitter oauth library by Hameedullah Khan.
Instead of inheritance from the python-twitter library, it currently
exists standalone with an all encompasing ApiCall function. There are
plans to provide wrapper functions around common requests in the future.

Requires:
  simplejson
  oauth2
'''

__author__ = "Konpaku Kogasa, Hameedullah Khan"
__version__ = "0.1"

# Library modules
import sys
import urllib
import urllib2
import urlparse
import time

# Non library modules
import simplejson
import oauth2 as oauth
from utils import ObjectFromDict

# Taken from oauth implementation at: http://github.com/harperreed/twitteroauth-python/tree/master
REQUEST_TOKEN_URL = 'https://twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'http://twitter.com/oauth/authorize'
SIGNIN_URL = 'http://twitter.com/oauth/authenticate'


class OAuthApi():
    def __init__(self, consumer_key, consumer_secret, token=None, token_secret=None):
    	if token and token_secret:
    		token = oauth.Token(token, token_secret)
    	else:
    		 token = None
        self._Consumer = oauth.Consumer(consumer_key, consumer_secret)
        self._signature_method = oauth.SignatureMethod_HMAC_SHA1()
        self._access_token = token 

    def _GetOpener(self):
        opener = urllib2.build_opener()
        return opener

    def _FetchUrl(self,
                    url,
                    http_method=None,
                    parameters=None):
        '''Fetch a URL, optionally caching for a specified time.
    
        Args:
          url: The URL to retrieve
          http_method: 
          	One of "GET" or "POST" to state which kind 
          	of http call is being made
          parameters:
            A dict whose key/value pairs should encoded and added 
            to the query string, or generated into post data. [OPTIONAL]
            depending on the http_method parameter
    
        Returns:
          A string containing the body of the response.
        '''
        # Build the extra parameters dict
        extra_params = {}
        if parameters:
          extra_params.update(parameters)
        
        req = self._makeOAuthRequest(url, params=extra_params, 
                                                    http_method=http_method)
        
        # Get a url opener that can handle Oauth basic auth
        opener = self._GetOpener()

        if http_method == "POST":
            encoded_post_data = req.to_postdata()
            #print dir(req)
            #url = req.get_normalized_http_url()
            url = req.normalized_url
        else:
            url = req.to_url()
            encoded_post_data = ""
            
        if encoded_post_data:
        	url_data = opener.open(url, encoded_post_data).read()
        else:
        	url_data = opener.open(url).read()
        	opener.close()
    
        # Always return the latest version
        return url_data
    
    def _makeOAuthRequest(self, url, token=None,
                                        params=None, http_method="GET"):
        '''Make a OAuth request from url and parameters
        
        Args:
          url: The Url to use for creating OAuth Request
          parameters:
             The URL parameters
          http_method:
             The HTTP method to use
        Returns:
          A OAauthRequest object
        '''
        
        oauth_base_params = {
        'oauth_version': "1.0",
        'oauth_nonce': oauth.generate_nonce(),
        'oauth_timestamp': int(time.time())
        }
        
        if params:
            params.update(oauth_base_params)
        else:
            params = oauth_base_params
        
        if not token:
            token = self._access_token
        request = oauth.Request(method=http_method,url=url,parameters=params)
        request.sign_request(self._signature_method, self._Consumer, token)
        return request

    def getAuthorizationURL(self, token, url=AUTHORIZATION_URL):
        '''Create a signed authorization URL
        
        Returns:
          A signed OAuthRequest authorization URL 
        '''
        return "%s?oauth_token=%s" % (url, token['oauth_token'])

    def getRequestToken(self, url=REQUEST_TOKEN_URL):
        '''Get a Request Token from Twitter
        
        Returns:
          A OAuthToken object containing a request token
        '''
        resp, content = oauth.Client(self._Consumer).request(url, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])

        return dict(urlparse.parse_qsl(content))
    
    def getAccessToken(self, token, verifier, url=ACCESS_TOKEN_URL):
        '''Get a Request Token from Twitter
        
        Returns:
          A OAuthToken object containing a request token
        '''
        token = oauth.Token(token['oauth_token'], token['oauth_token_secret'])
        token.set_verifier(verifier)
        client = oauth.Client(self._Consumer, token)
        
        resp, content = client.request(url, "POST")
        return dict(urlparse.parse_qsl(content))
    
    def FollowUser(self, user_id, options = {}):
        '''Follow a user with a given user id
         Args:
        user_id: The id of the user to follow
        options:
              A dict of options for the friendships/create call.
              See the link below for what options can be passed
              http://apiwiki.twitter.com/Twitter-REST-API-Method%3A-friendships%C2%A0create           
        '''
        options['user_id'] = user_id
        return self.ApiCall("friendships/create", "POST", options)

    def FollowUserByScreenname(self, screen_name, options = {}):
        '''Follow a user with a given screen_name
         Args:
        screen_name: The screen name of the user to follow
        options:
              A dict of options for the friendships/create call.
              See the link below for what options can be passed
              http://apiwiki.twitter.com/Twitter-REST-API-Method%3A-friendships%C2%A0create           
        '''
        options['screen_name'] = screen_name
        return self.ApiCall("friendships/create", "POST", options)

    def GetFriends(self, options={}):
    	'''Return a list of users you are following
    	
    	Args:
    	options:
          	A dict of options for the statuses/friends call.
          	See the link below for what options can be passed
          	http://apiwiki.twitter.com/Twitter-REST-API-Method%3A-statuses%C2%A0friends	

    	options['cursor']:
    		By default twitter returns a list of 100
    		followers. If you have more, you will need to
    		use the cursor value to paginate the results.
    		A value of -1 means to get the first page of results.
    		
    		the returned data will have next_cursor and previous_cursor
    		to help you continue pagination          	
    		
        Return: Up to 100 friends in dict format
    	'''
    	return self.ApiCall("statuses/friends", "GET", options)    
    
    def GetFollowers(self, options={}):
    	'''Return followers
    	
    	Args:
    	options:
          	A dict of options for the statuses/followers call.
          	See the link below for what options can be passed
          	http://apiwiki.twitter.com/Twitter-REST-API-Method%3A-statuses%C2%A0followers
          	
          	
    	options['cursor']:
    		By default twitter returns a list of 100
    		followers. If you have more, you will need to
    		use the cursor value to paginate the results.
    		A value of -1 means to get the first page of results.
    		
    		the returned data will have next_cursor and previous_cursor
    		to help you continue pagination
    		          		
        Return: Up to 100 followers in dict format
    	'''
    	return self.ApiCall("statuses/followers", "GET", options)
    
    def GetFriendsTimeline(self, options = {}):
    	'''Get the friends timeline. Does not contain retweets.
    	
          Args:
          options:
          	A dict of options for the statuses/friends_timeline call.
          	See the link below for what options can be passed
          	http://apiwiki.twitter.com/Twitter-REST-API-Method%3A-statuses-friends_timeline	
         
          Return: The friends timeline in dict format
    	'''
    	return self.ApiCall("statuses/friends_timeline", "GET", options)
    
    def GetHomeTimeline(self, options={}):
    	'''Get the home timeline. Unlike friends timeline it also contains retweets
    	
          Args:
          options:
          	A dict of options for the statuses/home_timeline call.
          	See the link below for what options can be passed
          	http://apiwiki.twitter.com/Twitter-REST-API-Method%3A-statuses-home_timeline
          	
          Return: The home timeline in dict format	
    	'''
    	return self.ApiCall("statuses/home_timeline", "GET", options)    
    
    def GetUserTimeline(self, options={}):
    	'''Get the user timeline. These are tweets just by a user, and do not contain retweets
    	
          Args:
          options:
          	A dict of options for the statuses/user_timeline call.
          	See the link below for what options can be passed
          	http://apiwiki.twitter.com/Twitter-REST-API-Method%3A-statuses-user_timeline
          	
          Return: The home timeline in dict format	
    	'''
    	return self.ApiCall("statuses/user_timeline", "GET", options)    
    
    def GetPublicTimeline(self):
    	'''
    		Get the public timeline, which is the 20 most recent statuses from non-protected
    		and custom icon users.  According to the API docs, this is cached for 60 seconds.
          	
          Return: The public timeline in dict format	
    	'''
    	return self.ApiCall("statuses/public_timeline", "GET", {})     
    
    def UpdateStatus(self, status, options = {}):
    	'''
        Args:
          status: The status you wish to update to
          options:
          	A dict of options for the statuses/update call.
          	See the link below for what options can be passed
          	http://apiwiki.twitter.com/Twitter-REST-API-Method%3A-statuses%C2%A0update
        Returns:
          Whether or not the status update suceeded
    	'''
    	options['status'] = status
    	return self.ApiCall("statuses/update", "POST", options)    

    def GetReplies(self, options={}):
    	return self.ApiCall("statuses/mentions", "GET", {})     

    def GetDirectMessages(self, options={}):
    	return self.ApiCall("direct_messages", "GET", {})     

    def GetUser(self, username, options={}):
        options = {}
        options['screen_name'] = username
    	return self.ApiCall("users/show", "GET", options)     

    def DestroyStatus(self, status_id, options = {}):
        return self.ApiCall("statuses/destroy/%d" % status_id, "POST", options) 

    def DestroyDirectMessage(self, direct_message_id, options = {}):
        return self.ApiCall("direct_messages/destroy/%d" % direct_message_id, "POST", options) 

    def PostDirectMessage(self, username, message, options = {}):
        options = {}
        options['screen_name'] = username
        options['text'] = message
        return self.ApiCall("direct_messages/new", "POST", options) 

    def ApiCall(self, call, request_type="GET", parameters={}):
        '''Calls the twitter API
        
       Args:
          call: The name of the api call (ie. account/rate_limit_status)
          type: One of "GET" or "POST"
          parameters: Parameters to pass to the Twitter API call
        Returns:
          Returns the twitter.User object
        '''
        json = self._FetchUrl("https://api.twitter.com/1/" + call + ".json", request_type, parameters)
        result = simplejson.loads(json)
        if type(result) == type([]):
            return [ObjectFromDict(element) for element in result]
        else:
            return ObjectFromDict(result)

        
