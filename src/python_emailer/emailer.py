
# email functions
import smtplib
from email.mime.text import MIMEText
from cryptography.fernet import Fernet
import base64
import json
import warnings
import os


class Emailer:
    def __init__(self,
                 config : str = '~/.conf/python_emailer/emailer_config.pkl', 
                 encrypt_in_memory = True, # probably stupid an overkill
                 key : str = None) -> None:
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
            self.email = self.fenret.encrypt(params['email'].encode('utf-8'))
            self.password = self.fenret.encrypt(params['password'].encode('utf-8'))
            self.server = params['server']
            self.port = params['port']
        return
    
    def send_email(self, to : str,  message : str, subject : str = '') -> None:
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
    
    def send_sms(self, to: str, message: str, provider: str) -> None:
        to = to + sms_id(provider)
        print(to)
        if len(message) > 153:
            warnings.warn('message is longer than 153 characters, it may be truncated')
        self.send_email(to, message)
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
