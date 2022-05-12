
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from traceback import format_exc

email='Your-email'
PASSWORD='Your-pass'

try:
    # set up the SMTP server
    s = smtplib.SMTP(host='###SMTP-Host', port=465)
    s.starttls()
    s.login(email, PASSWORD)

    msg = MIMEMultipart()       # create a message

    message = 'its a test'

    msg['From']=email
    msg['To']='###Dst-mail'
    msg['Subject']="###Your SubjectT"
    
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    
    # send the message via the server set up earlier.

    s.send_message(msg)
    
    del msg
    s.quit()
    #update database
    print('OK')
except Exception as e:
    print('!!!  Exception error   !!!')
    print(format_exc())
