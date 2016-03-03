from __future__ import print_function
import email.message
import smtplib
from smtplib import *
from jinja2 import *

from oauth2client import tools
from oauth2client.client import *

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


def render_mail(data="stats.json"):
    mail_file = open("base.html", "w")
    template = open("base.html" + ".j2", 'r')
    t_str = template.read()
    base_data = open(data)
    meta_data = json.loads(base_data.read())
    mail_template = Template(t_str)
    params = "Infrastructure QA status - %s" % datetime.datetime.now().__format__('%Y %b %d')
    mail_file.write(mail_template.render(data=meta_data, title=params))
    mail_file.close()
    return params


def send_rendered_mail(sub, to):
    mail_file = open("base.html", "r")
    temp = mail_file.read()
    msg = email.message.Message()
    msg['Subject'] = sub
    msg['From'] = 'rtandon@loggly.com'
    msg['To'] = to
    msg['Cc'] = "psurothiya@loggly.com"
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(temp)

    s = smtplib.SMTP(
        host="smtp.gmail.com",
        port=587
    )
    s.ehlo()
    s.starttls()
    s.ehlo()
    creds=json.loads(open("credentials.json").read())
    
    s.login(creds["username"],
            creds["password"])
    s.sendmail(msg['From'], [msg['To'], msg['Cc']], msg.as_string())


sender_to = "rsingh@loggly.com"
subject = render_mail()
send_rendered_mail(sub=subject, to=sender_to)
