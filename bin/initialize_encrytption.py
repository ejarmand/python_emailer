#!/usr/bin/env python3

# set up Fernet encrytion for user
from cyptography.fernet import Fernet
from ArgParser import ArgParser
import os

# todo: consider os.open insead of os.chmod

def parse_args(arg_parser):
    parser = ArgParser(description='configure fenret encryption for emailer.py')
    arg_parser.add_argument('-o', '--key_out',
      type=str,
      default='~/.conf/python_emailer/fenret.key', 
      help='path to write encryption key to'
      )
    arg_parser.add_argument('-p' '--permissions',
     type=str, default='600', help='permissions to set on key file')
    return arg_parser.parse_args()

def initialize_encryption(key_out, permissions):
    key = Fernet.generate_key()
    dir_path = os.path.dirname(key_out)
    os.makedirs(dir_path, exist_ok=True)

    with open(key_out, 'wb') as key_file:
        key_file.write(key)
    os.chmod(key_out, int(permissions, 8))

    with open(key_out, 'rb') as key_file:
        key = key_file.read()
    
def main():
    if args.key_out != '~/.conf/python_emailer/fenret.key':
        print('WARNING: using a non-default key path\n'
              'please remember to pass the proper key path when initializing the emailer')
        )
    args = parse_args(ArgParser())
    # sanitize path
    key_out = os.path.abspath(os.path.expanduser(args.key_out))

    if os.path.exists(key_out):
        response = input(f'key file {key_out} already exists, do you wish to overwrite it? [N/y]')
        if not response.lower().startswith('y'):
            print('aborting') 
        return
    print(f'initializing encryption key at {key_out}')
    initialize_encryption(args.key_out, args.permissions)
    print('encryption key initialized')

if __name__ == '__main__':
    main()
