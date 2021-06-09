import os
import logging as log
from crontab import CronTab

from installation_flows.utils import utils


def cronJobSetup(baseDir, executionPath):
    localConfig = utils.readConfigFile(baseDir, 'config', 'localConfig.json')

    # Remove all old cron jobs
    utils.execute_command(['crontab -r'])

    # Creating new cron job
    cron = CronTab(user=True)
    job = cron.new(command=executionPath + ' ' + os.path.join(baseDir, 'main.py'))
    job.setall(localConfig['cron_schedule'])
    log.info("Setting up cron job under current user at: %s", localConfig['cron_schedule'])
    cron.write()
