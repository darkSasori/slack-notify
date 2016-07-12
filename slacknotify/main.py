"""Main file to run slack-notify"""
import argparse
import os
import logging
from slacknotify.web import start_rtm, connect_ws


def run():
    """Run the slack-notify"""
    parser = argparse.ArgumentParser(description='Slack notification listen')
    parser.add_argument('--token', help='Set token to connect with slack')
    parser.add_argument(
        '--loglevel',
        choices=['DEBUG', 'INFO', 'WARNING'],
        default='INFO',
        help='Set log level'
    )
    try:
        file = '%s/.config/slack-notify' % os.getenv('HOME')
        args = parser.parse_args()
        if args.token:
            file = open(file, 'w')
            file.write(args.token)
            file.close()
            token = args.token
        else:
            file = open(file, 'r')
            token = file.read()
            file.close()

        logging.basicConfig(
            format='[%(asctime)s] %(levelname)s - %(message)s',
            datefmt='%d/%m/%Y %I:%M:%S %p',
            level=args.loglevel
        )

        response = start_rtm(token)
        if response['ok'] is False:
            raise Exception(response['error'])

        connect_ws(response)

    except FileNotFoundError:
        logging.error("Set token with --token")

if __name__ == '__main__':
    run()
