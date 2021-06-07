import os.path
import smtplib
import logging as log

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from installation_flows.utils import utils


def sendEmail(baseDir, api, password, clusterName, clusterDirPath, ocpReleaseFilePath, enableNotification):
    emailConfig = utils.readConfigFile(baseDir, 'config', 'emailConfig.json')
    try:
        if enableNotification:
            body = " Username: kubeadmin \t\t Password: %s \n Server API: %s \n Cluster URL: https://console-openshift-console.apps.%s.devcluster.openshift.com \n Cluster Directory: %s" % (
                password, api, clusterName, clusterDirPath
            )
            msg = MIMEMultipart()
            msg['Subject'] = "[OCP cluster bot]: cluster: %s" % clusterName
            msg['From'] = emailConfig['email_id']
            msg['To'] = ', '.join(emailConfig['receiver_emails'])
            msg.attach(MIMEText(body, 'plain'))

            for file in [os.path.join(clusterDirPath, 'auth', 'kubeconfig'), os.path.join(clusterDirPath, 'auth', 'kubeadmin-password'), os.path.join(clusterDirPath, 'metadata.json'), ocpReleaseFilePath]:
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(file, "rb").read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
                msg.attach(part)

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

