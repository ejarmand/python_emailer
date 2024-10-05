# Python Emailer

A python class meant to send simple email messages.

## Security warning

This repo attempts to encrypt email users and email passowords on the local machine.
This is better than storing plain text but is still a risk. *If a user has sudo and access to both config and key files, they will have access to your email address and password.*
- Never publicly upload an encryption key.
- Avoid uploading any object containing your email address and password.
- Avoid using an email address which you use for important things, (e.g. linked to bank or credit card)
    - It is generally quite easy to make a new email address and I'd reccomend creating one explicitly for sending messages if possible

*This software is provided without any warranty and I am not responsible for security issues arising from saving a password*
