import os
import logging as log
from crontab import CronTab

from installation_flows.utils import utils


def cronJobSetup(baseDir):
    localConfig = utils.readConfigFile(baseDir, 'config', 'localConfig.json')
    cron = CronTab(user=True)
    job = cron.new(command='/usr/bin/python '+os.path.join(baseDir, 'main.py'))
    job.setall(localConfig['cron_setup']['cron_schedule'])
    log.info("Setting up cron job under current user at: %s", localConfig['cron_setup']['cron_schedule'])
    cron.write()
