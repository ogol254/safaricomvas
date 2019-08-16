import smtplib
import email.utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


import logging
import logging.handlers

# smtp_handler = logging.handlers.SMTPHandler(mailhost=("172.29.229.69", 25),
#                                             fromaddr="VASSolutions@safaricom.co.ke", 
#                                             toaddrs="Aogol@safaricom.co.ke",
#                                             subject=u"AppName error!")

# logger = logging.getLogger()
# logger.addHandler(smtp_handler)


class Email():

    def __init__(self, to_email=[]):
        self.to_email = to_email


    def send(self, msg):
        server = smtplib.SMTP()
        server.connect ('172.29.229.69', 25) 
        try:
            for i in self.to_email: 
                server.sendmail('VASSolutions@safaricom.co.ke', [i], msg.as_string())
        except Exception as e:
            return e
            # logger.exception('Unhandled Exception')

    def welcome_text(self, to_name, to_password, to_username):
        text = """ \
            <div style="overflow-x: auto;"><html><body>
            <table style="height: 26px; background-color: #228b22; overflow-x:auto; margin-left: auto; margin-right: auto;"  width="1405"><tbody>
                        <tr><td style="width: 648.75px; text-align: center;">&nbsp;</td></tr></tbody></table>
                    <h2 style="text-align: center;">Hi, %s</h2>
                    <p style="text-align: center;">Welcome to Asset tracker. Please click the link below to log in</p>
                    <p style="text-align: center;">URL:<a href="http://www.safaricom.co.ke">www.safaricom.co.ke</a></p>
                    <p style="text-align: center;">Username: %s</p>
                    <p style="text-align: center;">Password: %s</p>
                    <p style="text-align: center;">Thank you!</p>
            <table style="height: 5px; background-color: #228b22; overflow-x:auto; margin-left: auto; margin-right: auto;"  width="1405">
                    <tbody><tr><td style="width: 637.841px;">&nbsp;</td></tr></tbody></table>
            </body></html></div>
        """ % (str(to_name), str(to_username), str(to_password))
        msg = MIMEText(text, "html")
        msg['To'] = email.utils.formataddr((to_name, ','.join(self.to_email)))
        msg['From'] = email.utils.formataddr(('VAS Solutions', 'VASSolutions@safaricom.co.ke'))
        msg['Subject'] = "Welcome to Safaricom VAS {}".format(to_username)
        self.send(msg)


    def project_a_admin(self, to_name, creator, projectname, link):
        text = """ \
            <div style="overflow-x: auto;"><table style="height: 26px; background-color: #228b22; overflow-x: auto;"  width="1405"><tbody><tr><td style="width: 648.75px; text-align: center;">&nbsp;</td></tr></table>
                <h2 style="text-align: center;"><br /><img src="https://images.app.goo.gl/SCmL16ewskfmJrfz6" alt="https://images.app.goo.gl/SCmL16ewskfmJrfz6" width="250" height="170" /></h2>
                <h2 style="text-align: center;">NEW PROJECT ALERT</h2>
                <p style="text-align: center;">&nbsp;</p>
                <p style="text-align: left;">Dear %s ,&nbsp;</p>
                <p style="text-align: left;">%s has added a new project %s. We need your approval to publish this in the site. Kindly check out and approve.</p>
                <table style="height: 46px; background-color: #228b22; margin-left: auto; margin-right: auto;" width="206"><tbody><tr>
                <td style="width: 196.023px; text-align: center;"><span style="color: #ffffff;"><a style="color: #ffffff;" href="%s">CLICK HERE TO APPROVE</a></span></td></tr></tbody></table>
                <p style="text-align: left;">Warm Regards&nbsp;</p>
                <p style="text-align: left;">Vas Solutions</p>
            <table style="height: 5px; background-color: #228b22; overflow-x: auto;"  width="1405"><tbody><tr><td style="width: 637.841px;">&nbsp;</td></tr></tbody></table></div>
        """ % (str(to_name), str(creator), str(projectname), str(link))
        msg = MIMEText(text, "html")
        msg['To'] = email.utils.formataddr((to_name, ','.join(self.to_email)))
        msg['From'] = email.utils.formataddr(('VAS Solutions', 'VASSolutions@safaricom.co.ke'))
        msg['Subject'] = "New Project Alert: {}".format(projectname)
        self.send(msg)

    def p_self_notifier(self, name, projectname):
        text = """ \
            <div style="overflow-x: auto;"><table style="height: 26px; background-color: #228b22; overflow-x: auto;"  width="1405"><tbody><tr><td style="width: 648.75px; text-align: center;">&nbsp;</td></tr></table>
                <h2 style="text-align: center;"><br /><img src="https://images.app.goo.gl/SCmL16ewskfmJrfz6" alt="https://images.app.goo.gl/SCmL16ewskfmJrfz6" width="250" height="170" /></h2>
                <h2 style="text-align: center;">NEW PROJECT ALERT</h2>
                <p style="text-align: center;">&nbsp;</p>
                <p style="text-align: left;">Dear %s ,&nbsp;</p>
                <p style="text-align: left;">Your new project %s has been submitted for approval</p>
                <p style="text-align: left;">Warm Regards&nbsp;</p>
                <p style="text-align: left;">Vas Solutions</p>
            <table style="height: 5px; background-color: #228b22; overflow-x: auto;"  width="1405"><tbody><tr><td style="width: 637.841px;">&nbsp;</td></tr></tbody></table></div>
        """ % (str(name), str(projectname))
        msg = MIMEText(text, "html")
        msg['To'] = email.utils.formataddr((name, ','.join(self.to_email)))
        msg['From'] = email.utils.formataddr(('VAS Solutions', 'VASSolutions@safaricom.co.ke'))
        msg['Subject'] = "New Project Alert: {}".format(projectname)
        self.send(msg)




