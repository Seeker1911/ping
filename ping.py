import os
import smtplib
import time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

"""
Python 3 script to check on website availability
use no hangup to run in background i.e. nohup /path/to/ping.py &
see def server_error for instructions on setting up application specific password with 2FA
"""

def main():
    while True:
        http = 'http://'
        com = '.com/'
        url_list = ['seeker-studios', 'musiccitytalent', 'pythonsecretunderground']
        
        for url in url_list:
            try :
                response = urlopen( http + url + com )
            except HTTPError as e:
                server_error(str(e.code))
            except URLError as e:
                 server_error(str(e.reason))
            else:
                html = response.read()
        time.sleep(3600)
        

def server_error(error):
    """1. Log-in into Gmail with your account
       2. Navigate to https://security.google.com/settings/security/apppasswords
       3. In 'select app' choose 'custom', give it an arbitrary name and press generate
       4. It will give you 16 chars token.
       5. This works even if you have 2FA."""

    _gmail_secret = os.environ['GMAIL_PASSWORD']
    _gmail_address = os.environ['GMAIL_ADDRESS']
    _icloud_address = os.environ['ICLOUD_ADDRESS']

    sendemail(from_addr    = _gmail_address,
              to_addr_list = [_cloud_address],
              subject      = 'Server Error',
              message      = 'Server down: ' + str(error),
              login        = 'michaelmead007@gmail.com',
              password     = _gmail_secret)

def sendemail(from_addr, to_addr_list, 
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems
        
if __name__ == "__main__":
    main()
