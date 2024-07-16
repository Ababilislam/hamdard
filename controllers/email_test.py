def email_test():
    return dict()

from gluon.tools import Mail
def email_test_1():
    mail = Mail()
    # mail.send('nadira.nazmun2001@gmail.com','Message subject','Plain text body of the message')
    # mail.settings.server = 'smtp.example.com:25'
    
    mail.settings.sender = 'eappair2022@gmail.com'
    mail.settings.login = 'eappair2022@gmail.com:eAppair1234'
    mail.settings.server = 'gae'
    mail.send(to=['nadira.nazmun2001@gmail.com'],
          subject='hello',
          # If reply_to is omitted, then mail.settings.sender is used
          reply_to='nadira.nazmun2001@gmail.com',
          message='hi there')
    return mail







# def mail_test():
#     mail.send('nadira.nazmun2001@gmail.com',
#       'Message subject',
#       ('Plain text body', '<html>html body</html>'))
#     return 'Nadira'

# import smtplib
# # from email.message import EmailMessage
# def send_mail(to_email, subject, message, server='smtp.example.cn',
#               from_email='xx@example.com'):
#     # import smtplib
#     msg = EmailMessage()
#     msg['Subject'] = subject
#     msg['From'] = from_email
#     msg['To'] = ', '.join(to_email)
#     msg.set_content(message)
#     # print(msg)
#     server = smtplib.SMTP(server)
#     server.set_debuglevel(1)
#     server.login(from_email, 'password')  # user & password
#     server.send_message(msg)
#     server.quit()
#     return 'successfully sent the mail.'

# def mail_test():
#     return 'ghgfjghj'
#     send_mail(to_email=['nadira.nazmun2001@gmail.com', 'nadira.nuri@gmail.com'],
#           subject='hello', message='Your analysis has done!')