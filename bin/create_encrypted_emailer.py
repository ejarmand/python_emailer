#!/usr/bin/env python3
from cyptography.fernet import Fernet
from ArgParser import ArgParser
import base64
import json
import os

def parse_args():
    parser = ArgParser(description='intialize an encrypted emailer')
    parser.add_arugment('-e', '--email',
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
        help='smtp server to send email through'
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
    parser.add_argument('-o', '--out_config',
        type=str,
        default='~/.conf/python_emailer/emailer_config.pkl',
        help='path to write encrypted emailer configuration to'
    )
    paser.add_argument('--permissions', 
        type=str,
        default='600',
        help='permissions for the configuration file'
    )
    return parser.parse_args()

def main():
    args =parse_args()
    if not os.path.exists(args.key):
        print('ERROR: key file not found, please initialze encrytion with "initialize_encryption.py"')
        return
    with open(args.key, 'rb') as key_file:
        fernet = Fernet(key_file.read())

    PORT = 587 # For tls messages
    params = { 'email': args.email,
                'password': args.password,
                'server': args.server 
                'port': PORT}
    params_encrypt = {'key' : paser.key if not args.no_store_key else '',
                    'params': base64.b64encode(
                                fernet.encrypt(
                                    json.dumps(params).encode()
                                )
                              ).decode('utf-8')
                    }
    config_out = os.path.abspath(os.path.expanduser(args.key_out))

    with open(config_out, 'wb') as config_file:
        pickle.dump(params_encrypt, config_file)
    print('args.permissions', args.permissions)
    os.chmod(config_out, int(args.permissions, 8))


    print(f'encrypted emailer configuration written to {config_out}')
    return

if __name__ == '__main__':
    main()







