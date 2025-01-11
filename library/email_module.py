#!/usr/bin/env python3

'''
@author: mahendras.tulipit@gmail.com
@date: 11th Jan. 2025
@description: This module send the email to the distribution list.
'''

import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from ansible.module_utils.basic import AnsibleModule

def send_email(module, smtp_server, smtp_port, sender_email, recipient_emails, subject, body, subtype, attachment_path=None, username=None, password=None):
    try:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = ', '.join(recipient_emails)
        msg.attach(MIMEText(body, subtype))

        if attachment_path:
            part = MIMEBase('application', 'octet-stream')
            with open(attachment_path, 'rb') as attachment:
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
            msg.attach(part)

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        if username and password:
            server.login(username, password)

        server.sendmail(sender_email, recipient_emails, msg.as_string())
        server.quit()

        module.exit_json(changed=True, message="Email sent successfully.")
    except Exception as e:
        module.fail_json(msg=f"Failed to send email: {str(e)}")

def main():
    module = AnsibleModule(
        argument_spec={
            "smtp_server": {"required": True, "type": "str"},
            "smtp_port": {"required": True, "type": "int"},
            "sender_email": {"required": True, "type": "str"},
            "recipient_email": {"required": True, "type": "list"},
            "subject": {"required": True, "type": "str"},
            "body": {"required": True, "type": "str"},
            "subtype": {
                "type": 'str',
                "default": 'plain',
                "choices": ['html', 'plain']
            },
            "attachment_path": {"required": False, "type": "str"},
            "username": {"required": False, "type": "str"},
            "password": {"required": False, "type": "str", "no_log": True},
        }
    )

    smtp_server = module.params['smtp_server']
    smtp_port = module.params['smtp_port']
    sender_email = module.params['sender_email']
    recipient_emails = module.params['recipient_email']
    subject = module.params['subject']
    body = module.params['body']
    subtype = module.params['subtype']
    attachment_path = module.params.get('attachment_path')
    username = module.params.get('username')
    password = module.params.get('password')

    send_email(module, smtp_server, smtp_port, sender_email, recipient_emails, subject, body, subtype, attachment_path, username, password)

if __name__ == '__main__':
    main()
