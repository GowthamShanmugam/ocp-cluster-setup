import os
import yaml
import logging as log
from installation_flows.utils import utils


def deployOcs(baseDir, clusterDir, server, password, deployOcs):
    try:
        if deployOcs:
            clusterConfig = utils.readConfigFile(baseDir, 'config', 'clusterConfig.json')
            read = open(os.path.join(baseDir, 'templates', 'ocsConfig.yaml'), 'r')
            configs = list(yaml.load_all(read, Loader=yaml.FullLoader))
            configs[2]['spec']['image'] = clusterConfig['ocs']['ocs_build']
            read.close()
            write = open(os.path.join(clusterDir, 'ocsConfig.yaml'), 'w')
            yaml.dump_all(configs, write, default_flow_style=False, explicit_start=True)
            write.close()
            log.info('Log in ocp cluster using oc client')
            os.system('oc login  '+server+' -u kubeadmin -p '+password+'  --insecure-skip-tls-verify')
            log.info('...Deploying OCS %s', clusterConfig['ocs']['ocs_build'])
            os.system('oc apply -f ' + os.path.join(clusterDir, 'ocsConfig.yaml'))
        else:
            log.warning("OCS deployment is skipped")
    except Exception as ex:
        log.error("Unable to deploy OCS: %s", ex)
        raise ex
