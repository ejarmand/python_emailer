#!/usr/bin/env python3
from cryptography.fernet import Fernet
from argparse import ArgumentParser
import base64
import json
import os

def parse_args():
    parser = ArgumentParser(description='intialize an encrypted emailer')
    parser.add_argument('-e', '--email',
        type=str,
        help='email address to send from'
    )
    parser.add_argument('-p', '--password',
        type=str,
        help='password for the email address'
    )
    parser.add_argument('-s', '--server',
        type=str,
        default='smtp.gmail.com',
        help='smtp server to send email through. default is %(default)s'
    )
    parser.add_argument('-k', '--key', 
        type=str,
         default='~/.conf/python_emailer/fernet.key', 
         help='path to the Fernet key file'
    )
    parser.add_argument('--no-store-key',
        action='store_true',
        help='do not store the path to key in the configuration file'
    )
    parser.add_argument('-o', '--config_out',
        type=str,
        default='~/.conf/python_emailer/emailer_config.pkl',
        help='path to write encrypted emailer configuration to'
    )
    parser.add_argument('--permissions', 
        type=str,
        default='600',
        help=('permissions for the configuration file default is %(default)s'
              ' in octal format, user can read and write; group and others have no permissions'
        )
    )
    return parser.parse_args()

def main():
    args =parse_args()
    try:
        args.email.encode('utf-8')
        args.password.encode('utf-8')
    except UnicodeError:
        print('ERROR: email and password must be utf-8')
        return

    san_key = os.path.abspath(os.path.expanduser(args.key))
    if not os.path.exists(san_key):
        reinit = input('ERROR: key file not found, would you like to '
              'run init_emailer_encryption with the key you povided? [N/y]')
        if reinit.lower().startswith('y'):
            os.system('init_emailer_encryption -o ' + args.key)
        else:
            print('aborting')
            return
    san_key = os.path.abspath(os.path.expanduser(args.key))
    with open(san_key, 'rb') as key_file:
        fernet = Fernet(key_file.read())

    PORT = 587 # For tls messages
    params = { 'email': args.email,
                'password': args.password,
                'server': args.server,
                'port': PORT}
    params_encrypt = {'key' : args.key if not args.no_store_key else '',
                    'params': base64.b64encode(
                                fernet.encrypt(
                                    json.dumps(params).encode()
                                )
                              ).decode('utf-8')
                    }
    config_out = os.path.abspath(os.path.expanduser(args.config_out))

    with open(config_out, 'w') as config_file:
        json.dump(params_encrypt, config_file)
    print('args.permissions', args.permissions)
    os.chmod(config_out, int(args.permissions, 8))


    print(f'encrypted emailer configuration written to {config_out}')
    return

if __name__ == '__main__':
    main()







