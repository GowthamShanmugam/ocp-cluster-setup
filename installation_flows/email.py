import smtplib
import pyjokes
import logging as log

from installation_flows.utils import utils


def sendEmail(baseDir, api, password, clusterName, clusterDirPath, enableNotification):
    emailConfig = utils.readConfigFile(baseDir, 'config', 'emailConfig.json')
    try:
        if enableNotification:
            server = smtplib.SMTP_SSL(
                emailConfig['email_smtp_server'],
                int(emailConfig['email_smtp_port'])
            )
            server.login(
                emailConfig['email_id'],
                emailConfig['email_pass']
            )
            log.info("...Sending email notification")
            server.sendmail(
                emailConfig['email_id'],
                emailConfig['receiver_emails'],
                "Subject: [OCP cluster bot]: clusterName: %s\n\n Cluster Directory: %s \n server: %s \n password: %s \n username: kubeadmin \n clusterURL: https://console-openshift-console.apps.%s.devcluster.openshift.com \n\n\n Today's Joke(:D :D :D): %s" % (clusterName, clusterDirPath, api, password, clusterName, pyjokes.get_joke(language='en'))
            )
        else:
            log.warning("Mail notification is disabled")
    except (
            smtplib.socket.gaierror,
            smtplib.SMTPException
    ) as ex:
        log.error("Unable to send email: %s", ex)
        raise ex
