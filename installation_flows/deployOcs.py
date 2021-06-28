import os
import time
import logging as log
from installation_flows.utils import utils


def deployOcs(baseDir, clusterDir, clusterConfig):
    try:
        ocsConfig = clusterConfig['ocs']
        if ocsConfig['deploy_ocs']:
            configs = utils.readArrayOfConfigFile(baseDir, 'templates', 'ocsConfig.yaml')
            configs[2]['spec']['image'] = ocsConfig['ocs_build']
            configs[3]['spec']['channel'] = ocsConfig['channel']
            configs[3]['spec']['startingCSV'] = ocsConfig['ocs_subscription']
            utils.writeArrayOfConfigFile(clusterDir, '', 'ocsConfig.yaml', configs)
            log.info('...Deploying OCS %s', ocsConfig['ocs_build'])
            utils.execute_command(['oc --kubeconfig ' + os.path.join(clusterDir, 'auth/kubeconfig') + ' apply -f ' + os.path.join(clusterDir, 'ocsConfig.yaml')])
            time.sleep(300)
            utils.execute_command(['oc --kubeconfig ' + os.path.join(clusterDir, 'auth/kubeconfig') + ' apply -f ' + os.path.join(baseDir, 'templates', 'storageCluster.yaml')])
        else:
            log.warning("OCS deployment is skipped")
    except Exception as ex:
        log.error("Unable to deploy OCS: %s", ex, exc_info=True)

