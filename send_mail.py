import smtplib
import passwords_manager

SERVICE = 'gmail'
GMAIL_USERNAME = passwords_manager.get_username_by_service(SERVICE)
GMAIL_PASSWORD = passwords_manager.get_password(SERVICE, GMAIL_USERNAME)


def connect(server):
    server.ehlo()
    server.starttls()
    server.login(GMAIL_USERNAME, GMAIL_PASSWORD)


def send_mail(server, msg, toaddr="shahafalo@gmail.com", fromaddr=GMAIL_USERNAME):
    server.sendmail(fromaddr, toaddr, msg)


def main(msg):
    print "starting"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    connect(server)
    send_mail(server, msg)
    server.quit()
    print "just finish agter sending the massage:"
    print msg


def do_this(msg="cool man"):
    main(msg)
