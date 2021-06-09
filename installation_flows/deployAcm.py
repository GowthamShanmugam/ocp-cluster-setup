import os
import logging as log
import time

from installation_flows.utils import utils


def deployAcm(baseDir, clusterDir, clusterConfig):
    try:
        acmConfig = clusterConfig['acm']
        if acmConfig['deploy_acm']:
            configs = utils.readArrayOfConfigFile(baseDir, 'templates', 'acmConfig.yaml')
            configs[2]['spec']['channel'] = acmConfig['channel']
            configs[2]['spec']['startingCSV'] = acmConfig['acm_subscription']
            utils.writeArrayOfConfigFile(clusterDir, '', 'acmConfig.yaml', configs)
            log.info('...Subscribing ACM %s', acmConfig['acm_subscription'])
            utils.execute_command(['oc --kubeconfig ' + os.path.join(clusterDir, 'auth/kubeconfig') + ' apply -f ' + os.path.join(clusterDir, 'acmConfig.yaml')])

            log.info("Waiting ACM operator to be up and run...")
            checkAcmOperatorStatus(clusterDir, acmConfig['acm_subscription'])
            utils.execute_command(['oc --kubeconfig ' + os.path.join(clusterDir, 'auth/kubeconfig') + ' apply -f ' + os.path.join(baseDir, 'templates', 'acmHubConfig.yaml')])
        else:
            log.warning("ACM subscription is skipped")
    except Exception as ex:
        log.error("Unable to subscribe ACM: %s", ex, exc_info=True)

def checkAcmOperatorStatus(clusterDir, name, retry=1):
    status = utils.execute_command(['oc --kubeconfig ' + os.path.join(clusterDir, 'auth/kubeconfig') + ' get  ClusterServiceVersion ' + name + ' -n open-cluster-management -o=jsonpath={.status.phase}'])
    print(retry)
    try:
        if status[0] == 'Succeeded' or retry >= 5:
            return
    except Exception:
        pass

    time.sleep(60)
    checkAcmOperatorStatus(clusterDir, name, retry+1)
