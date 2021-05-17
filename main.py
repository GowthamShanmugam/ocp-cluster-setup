import os
import sys
import logging as log
from installation_flows import setupOcpCluster, cronJobSetup


baseDir = os.path.dirname(os.path.abspath(__file__))
log.basicConfig(filename=os.path.join(baseDir, 'log', 'ocpClusterInstallation.log'), filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',  level=log.INFO)

def main(cronExecution):
    try:
        cronJobSetup.cronJobSetup(baseDir) if cronExecution else setupOcpCluster.setupOcpCluster(baseDir)
        log.info('!------OCP cluster setup is finished successfully------!')
    except Exception as ex:
        log.error("Unable to create OCP cluster: %s", ex)


if __name__ == '__main__':
    main(len(sys.argv) > 1)
