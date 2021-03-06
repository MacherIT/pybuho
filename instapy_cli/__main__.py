import sys
from platform import python_version
from instapy_cli.cli import InstapyCli as client
from optparse import OptionParser
import pkg_resources  # part of setuptools
version = pkg_resources.require('instapy_cli')[0].version


'''
TODO:
- use instapy_cli.media to download image link and use it for upload and configure_photo
- rewrite main to support file and links for media
'''
def main(args=None):

    welcome_msg = 'instapy-cli'
    print('instapy ' + version + '  |  python ' + python_version())

    # cli = client()
    # cli.loop(args)

    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option('-u', dest='username', help='username')
    parser.add_option('-p', dest='password', help='password')
    parser.add_option('-f', dest='file', help='file path or url')
    parser.add_option('-t', dest='caption', help='caption text')
    # parser.add_option('-h', dest='help', help='help')
    (options, args) = parser.parse_args(args)
    if args is None or (
        not options.username and
        not options.password and
        not options.file and
        not options.caption
    ):
        print('[USE] instapy -u USR -p PSW -f FILE/LINK -t \'TEXT CAPTION\'')
        print('\nFor other reference go to >> https://github.com/b3nab/instapy-cli')
        return
    if not options.username:
        parser.error('Username is required')
    password = options.password
    if not options.password:
      import getpass
      password = getpass.getpass()
    if not options.file:
        parser.error('File path or url link is required to create a media to upload')

    with client(options.username, password) as cli:
        text = options.caption or ''
        return cli.upload(options.file, text)

if __name__ == '__main__':
    main()
