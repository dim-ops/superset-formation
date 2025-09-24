import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_username = 'AKIA5FTZEYBYCFCEQJVW'
smtp_password = 'BKvgGPtbPxEzqYMHBm1Maeajf3GQfrTE/9pqdQ0xZvK3'
from_email = 'report.superset@dimops.com'
to_email = 'dimitri.grisard03@gmail.com'

msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = 'Superset SMTP config test'
msg.attach(MIMEText('It worked'))

try:
    mailserver = smtplib.SMTP('email-smtp.us-east-1.amazonaws.com', 2587)
    mailserver.starttls()
    mailserver.login(smtp_username, smtp_password)
    mailserver.sendmail(from_email, to_email, msg.as_string())
    mailserver.quit()
    print('Email envoyé avec succès !')
except Exception as e:
    print(f'Erreur: {e}')
