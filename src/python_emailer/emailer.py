
# email functions
import smtplib
from email.mime.text import MIMEText
from cryptography.fernet import Fernet
import base64
import json
import warnings
from twilio.rest import Client
import os


class Emailer:
    def __init__(self,
                 version : str = 'email',
                 config : str = '~/.conf/python_emailer/emailer_config.pkl', 
                 key : str = None) -> None:
        if version.lower() == 'twilio':
            # adjusts the default config
            if config == '~/.conf/python_emailer/emailer_config.pkl':
                config = '~/.conf/python_emailer/twilio_config.pkl'
        config = os.path.abspath(os.path.expanduser(config))
        self.load_config(config, key)

    def load_config(self, config : str, key : str = None)-> None:
        with open(config, 'rb') as config_file:
            config = json.load(config_file)
            if not key:
                key = config['key']
                key = os.path.abspath(os.path.expanduser(key))
            with open(key, 'rb') as key_file:
                self.fenret = Fernet(key_file.read())
            params = json.loads(
                self.fenret.decrypt(
                    base64.b64decode(
                    config['params'],
                    )
                ).decode('utf-8')
            )
            if 'twilio' in config.keys():
                self._load_twilio_config(
                    params['sid'],
                    params['token'],
                    params['phone_number']
                )
            else:
                self._load_smpt_config(
                    params['email'],
                    params['password'],
                    params['server'],
                    params['port']
                )
        return
    
    def _load_smpt_config(self, email : str, password : str, server : str, port : int) -> None:
        self.email = self.fenret.encrypt(email.encode('utf-8'))
        self.password = self.fenret.encrypt(password.encode('utf-8'))
        self.server = server
        self.port = port
        return
    
    def _load_twilio_config(self, sid : str, token : str, phone_number : str) -> None:
        self.twilio_sid = self.fenret.encrypt(sid.encode('utf-8'))
        self.twilio_token = self.fenret.encrypt(token.encode('utf-8'))
        self.phone_number = phone_number
        return

    
    def send_email(self, to : str,  message : str, subject : str = '') -> None:
        if hasattr(self, 'twilio_sid'):
            warnings.warn('twilio configuration found, not sure if email works')
            self.send_sms(to=to, message=message)
            return
        
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.fenret.decrypt(self.email).decode('utf-8')
        msg['To'] = to
        with  smtplib.SMTP(self.server, self.port) as server:
            server.starttls()
            server.login(
                        self.fenret.decrypt(self.email).decode('utf-8'),
                        self.fenret.decrypt(self.password).decode('utf-8')
                        )
            server.sendmail(self.fenret.decrypt(self.email).decode('utf-8'), to, msg.as_string())
            server.quit()
        return
    
    def send_sms(self, to: str, message: str, provider: str = None) -> None:
        if hasattr(self, 'twilio_sid'):
            self._send_twilio(to=to, message=message)
            return
        
        if not provider:
            warnings.warn('no provider specified, sms may not be sent')
            return
        to = to + sms_id(provider)
        print(to)
        if len(message) > 153:
            warnings.warn('message is longer than 153 characters, it may be truncated')
        self.send_email(to, message)
        return
    
    def _send_twilio(self, to: str, message: str) -> None:
        if not to.startswith('+1'):
            to = '+1' + to
        client = Client(
            self.fenret.decrypt(self.twilio_sid).decode('utf-8'),
            self.fenret.decrypt(self.twilio_token).decode('utf-8')
        )
        message = client.messages.create(
            to=to,
            from_=self.phone_number,
            body=message
        )
        return

def sms_id(provider : str) -> str:
    sms_conversion = {
        'att': '@txt.att.net',
        'tmobile': '@tmomail.net',
        'verizon': '@vtext.com',
        'sprint': '@messaging.sprintpcs.com'
    }
    if provider.lower() not in sms_conversion.keys():
        warnings.warn(f'{provider} not found in sms conversion')
        return provider
    return sms_conversion[provider.lower()]
