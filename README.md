# Python Emailer
A python class meant to send simple email messages.


## Installation
to install clone the repo, and then install with pip, e.g.

```bash
git clone https://github.com/ejarmand/python_emailer.git
python3 -m pip install ./python_emailer
```

## Setup
To get started you can initialize an encryption key if you want to save the key in a particular location, or you can just create a new encrypted emailer config by calling:

```bash
create_encrypted_emailer -e your_email@provider.com -s your_passord
```

If you haven't initialized an encryption key, using `init_emailer_encryption` then you'll be prompted to initialize a key using the same key value listed for your emailer.

### Twilio
I've set up the emailer to send useing [twilio](https://www.twilio.com/docs/usage/api) as a backend as this should be superior for sms (although requires a new account and costs some money per text). This is similarly initilaized with `create_encrypted_twilio`, e.g.


```bash
create_encrypted_twilio -i twilioSID -t authenticaiton_token -p phone_number_you_send_messages_from
```

You can't send messages from your own number to itself using twilio. You can purchase and set up a phone number via twilio but it's complicated. (though much cheaper than adding a new line). I may look into setting up a way to forward from smtp, to a server which passes on the sms via twilio to increase accesibility to my friends who don't want to configure an account. Clearly not a universal solution.

## Usage

### emailer class
After configuring usage is simple, the difference in between smtp and twilio is taken care of by the config:
```python
from python_emailer import Emailer
my_emailer = Emailer(config="path/to/emailer/confg") # config default points to default config path
my_emailer.send_email(
                      to="destination@provider.com",
                      message="Your python script failed without any errors!",
                      subject="Your script finished :)"
                      )
```

## Security warning

This repo attempts to encrypt email users and email passowords on the local machine.
This is better than storing plain text but is still a risk. *If a user has sudo and access to both config and key files, they will have access to your email address and password.*
- Never publicly upload an encryption key.
- Avoid uploading any object containing your email address and password.
- Avoid using an email address which you use for important things, (e.g. linked to bank or credit card)
    - It is generally quite easy to make a new email address and I'd reccomend creating one explicitly for sending messages if possible

*This software is provided without any warranty and I am not responsible for security issues arising from saving a password*

### keeping password from bash history
Given the command line initialization of an encrypted emailer, you won't want to store the command with your password in your bash history. To avoid this you can run history -c to wipe the current session, or use the HISTCONTROL variable to selectively remove commands from history. You can see options in the [GNU manual section on Bash variables](https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html) 

### How to connect to google?

Google disabled unsafe apps from password access as of sept 30, 2024. To connect with a gmail account you'll need to enable 2-step authentication, and then generate an app password [(How to create app passwords)](https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237)


### config scripts

```bash
usage: create_encrypted_emailer [-h] [-e EMAIL] [-p PASSWORD] [-s SERVER] [-k KEY] [--no-store-key] [-o CONFIG_OUT] [--permissions PERMISSIONS]

intialize an encrypted emailer

options:
  -h, --help            show this help message and exit
  -e EMAIL, --email EMAIL
                        email address to send from
  -p PASSWORD, --password PASSWORD
                        password for the email address
  -s SERVER, --server SERVER
                        smtp server to send email through. default is smtp.gmail.com
  -k KEY, --key KEY     path to the Fernet key file
  --no-store-key        do not store the path to key in the configuration file
  -o CONFIG_OUT, --config_out CONFIG_OUT
                        path to write encrypted emailer configuration to
  --permissions PERMISSIONS
                        permissions for the configuration file default is 600 in octal
                        format, user can read and write; group and others have no permissions
```

```bash
usage: init_emailer_encryption [-h] [-o KEY_OUT] [-p PERMISSIONS]

configure fernet encryption for emailer.py

options:
  -h, --help            show this help message and exit
  -o KEY_OUT, --key_out KEY_OUT
                        path to write encryption key to
  -p PERMISSIONS, --permissions PERMISSIONS
                        permissions to set on key file default is 600 in octal
                        format, user can read and write; group and others have no permissions
```


there is also a `send_sms` method. I'm currently having issues with emails not delivered when sent through python_emailer.

You can wrap the emailer in a finally block to send a message on success or failure:

```python
from python_emailer import Emailer
from time import time

def main():
    ...

if __name__ == __main__:
    tstart = time()
    try:
        main()
    except Exception as error:
        print(f'{error} erorr occured')
    finally:
        mailer = Emailer()
        # check for which message to send
        if error:
            mailer.send_email(to=your@email.com,
             f"this is a sad day, your script failed after {time()-tsart} seconds",
             "script failed"
             )
        else:
            mailer.send_email(to=your@email.com,
            f"Hooray! Your script ran succesfully in {time()-tsart} seconds!"
            "script completed without error"
            )
```




## Known issues
### sending messages to verizon

It seems Verizon agressively filters and slows messages sent to @vtext.com. This seems to coincide with them introducing an enterprise service to allow sms sent from email via SMTP.

