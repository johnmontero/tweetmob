import tweetmob
from distutils.core import setup

setup(
    name             = "tweetmob",
    version          = tweetmob.__version__,
    packages         = ['tweetmob','tweetmob/commands'],
    scripts          = ['bin/tweetmob'],
    author           = "John Montero",
    author_email     = "jmonteroc [at] gmail.com",
    description      = "Tweet message hoder",
    license          = "MIT",
    keywords         = "tweet, message, group",
    classifiers      =[
                        'Development Status :: 1 - Beta',
                        'Intended Audience :: Developers',
                        'License :: OSI Approved :: MIT License',
                        'Topic :: Software Development :: Build Tools',
                        'Programming Language :: Python :: 2.5',
                        'Programming Language :: Python :: 2.6',
                        'Programming Language :: Python :: 2.7',
                      ],
    long_description = """

"""

)
