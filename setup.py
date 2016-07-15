"""Setup file"""
from setuptools import setup

setup(name='slack-notify',
      version='0.1.3',
      description='Websocket client to connect with slack RTM API',
      url='https://github.com/darkSasori/slack-notify',
      author='Lineu Felipe',
      author_email='lineufelipe@gmail.com',
      license='MIT',
      packages=['slacknotify'],
      zip_safe=False,
      install_requires=[
          "pycurl",
          "ws4py",
          "ujson"
      ],
      scripts=['bin/slack-notify'])
