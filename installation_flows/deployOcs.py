import os
import logging as log
from installation_flows.utils import utils


def deployOcs(baseDir, clusterDir, deployOcs):
    try:
        if deployOcs:
            clusterConfig = utils.readConfigFile(baseDir, 'config', 'clusterConfig.json')
            configs = utils.readArrayOfConfigFile(baseDir, 'templates', 'ocsConfig.yaml')
            configs[2]['spec']['image'] = clusterConfig['ocs']['ocs_build']
            utils.writeArrayOfConfigFile(clusterDir, '', 'ocsConfig.yaml', configs)
            log.info('...Deploying OCS %s', clusterConfig['ocs']['ocs_build'])
            os.system('oc --kubeconfig ' + os.path.join(clusterDir, 'auth/kubeconfig') + ' apply -f ' + os.path.join(clusterDir, 'ocsConfig.yaml'))

            ocsSubscription = clusterConfig['ocs']['ocs_subscription']
            if(ocsSubscription['subscribe']):
                config = utils.readConfigFile(baseDir, 'templates', 'ocsSubscription.yaml')
                config['spec']['startingCSV'] = ocsSubscription['subscription']
                utils.writeConfigFile(clusterDir, '', 'ocsSubscription.yaml', config)
                log.info('Subscribing OCS version: %s', ocsSubscription['subscription'])
                os.system('oc --kubeconfig ' + os.path.join(clusterDir, 'auth/kubeconfig') + ' apply -f ' + os.path.join(clusterDir, 'ocsSubscription.yaml'))
            else:
                log.info('OCS subscription is disabled')
        else:
            log.warning("OCS deployment is skipped")
    except Exception as ex:
        log.error("Unable to deploy OCS: %s", ex, exc_info=True)
        raise ex
