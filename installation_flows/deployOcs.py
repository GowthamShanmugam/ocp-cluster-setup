import os
import yaml
import logging as log
from installation_flows.utils import utils


def deployOcs(baseDir, server, password, deployOcs):
    try:
        if deployOcs:
            clusterConfig = utils.readConfigFile(baseDir, 'config', 'clusterConfig.json')
            with open(os.path.join(baseDir, 'config', 'ocsConfig.yaml'), 'r+') as f:
                configs = list(yaml.load_all(f, Loader=yaml.FullLoader))
                configs[2]['spec']['image'] = clusterConfig['ocs']['ocs_build']
                yaml.dump_all(configs, f, default_flow_style=False, explicit_start=True)
            log.info('Log in ocp cluster using oc client')
            os.system('oc login  '+server+' -u kubeadmin -p '+password+'  --insecure-skip-tls-verify')
            log.info('...Deploying OCS %s', clusterConfig['ocs']['ocs_build'])
            os.system('oc apply -f ' + os.path.join(baseDir, 'config', 'ocsConfig.yaml'))
        else:
            log.warning("OCS deployment is skipped")
    except Exception as ex:
        log.error("Unable to deploy OCS: %s", ex)
        raise ex
