.. _getting_started:

Getting Started  
===============

Installation
--------------
We recommend installing TweetMob with ``pip`` but you can also try with
``easy_install`` and ``virtualenv``. Creating a spot in your environment where
TweetMob can be isolated from other packages is best practice.

To get started with an environment for TweetMob, create a virtual environment for
it without any site-packages that might pollute::

    virtualenv --no-site-packages tweetmob-env
    cd tweetmob-env 
    source bin/activate
    
The above commands created a virtual environment and *activated* it. Those
actions will encapsulate anything that we do with TweetMob, making it
easier to debug problems if needed.::

	pip install tweetmob

After a lot of output, you should have TweetMob successfully installed and ready
to use.

Get the credentials of authenticate
-----------------------------------

After installing you need to get the credentials of authenticate. Tweetmob needs to have the credentiales of authenticate to be running properly.:

	tweetmob --get-credentials

	Please, copy & paste this URL to your web browser:

	http://twitter.com/oauth/authorize?oauth_token=fSMx2OhXkUzP2yj3uoN5K5rwT75Kl3Q0ksEz88lG0

	You'll have to authorize the 'tweetmob' app and then copy and paste the given PIN here.

	What is the PIN? 8148260
	Credentials added.


Add account receive direct message::

	tweetmob --account-add jperez


Displays the current configuration values used::

	tweetmob --config-values

	consumer_key   = emeuDovYLyZVQWnMZlqco
	consumer_secret= KKll6SEigcb7BFhqkoiqkXR7dmJGEdaPncaGto5BR
	token          = 145911197-Ntekr2k139rf8zDWpTLb23d7Cn7wZ1eSmQWBozP
	token_secret   = kqbnvgOpT66UFuQ6UhltaQbsfH7wgloxk1RioNy8u
	dm.8d9d55df-6ff6-4851-a6b6-7325c266820a= jperez







