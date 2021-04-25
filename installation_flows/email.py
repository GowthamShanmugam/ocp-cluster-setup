import smtplib
import pyjokes
import logging as log

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from installation_flows.utils import utils


def sendEmail(baseDir, api, password, clusterName, clusterDirPath, enableNotification):
    emailConfig = utils.readConfigFile(baseDir, 'config', 'emailConfig.json')
    try:
        if enableNotification:
            body = " clusterDirectory: %s \n server: %s \n password: %s \n username: kubeadmin \n clusterURL: https://console-openshift-console.apps.%s.devcluster.openshift.com \n\n\n Start the day with laugh(:D :D :D): %s" % (
                clusterDirPath, api, password, clusterName, pyjokes.get_joke(language='en')
            )
            msg = MIMEMultipart()
            msg['Subject'] = "[OCP cluster bot]: cluster: %s" % clusterName
            msg['From'] = emailConfig['email_id']
            msg['To'] = ', '.join(emailConfig['receiver_emails'])
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP_SSL(
                emailConfig['email_smtp_server'],
                int(emailConfig['email_smtp_port'])
            )
            server.ehlo()
            server.login(
                emailConfig['email_id'],
                emailConfig['email_pass']
            )
            log.info("...Sending email notification")
            server.send_message(msg)
        else:
            log.warning("Mail notification is disabled")
    except (
            smtplib.socket.gaierror,
            smtplib.SMTPException
    ) as ex:
        log.error("Unable to send email: %s", ex)
        raise ex
