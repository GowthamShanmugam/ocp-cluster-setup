import os
import yaml
import uuid
import tarfile
import logging as log
import urllib.request

from installation_flows.utils import utils
from installation_flows.deployOcs import deployOcs
from installation_flows.email import sendEmail

def _updateInstallConfig(installConfig, clusterConfig, clusterName):
    installConfig['baseDomain'] = clusterConfig['ocp']['setup_info']['base_domain']
    installConfig['metadata']['name'] = clusterName
    installConfig['platform'] = {clusterConfig['ocp']['setup_info']['platform']: {"region" : clusterConfig['ocp']['setup_info']['region']}}
    installConfig['controlPlane']['platform'] = {
      clusterConfig['ocp']['setup_info']['platform']: {"type": clusterConfig['ocp']['setup_info']['type']}}
    installConfig['pullSecret'] = clusterConfig['ocp']['setup_info']['pull_secret']


def setupOcpCluster(baseDir):
    localConfig = utils.readConfigFile(baseDir, 'config', 'localConfig.json')
    clusterConfig = utils.readConfigFile(baseDir, 'config', 'clusterConfig.json')
    clusterName = clusterConfig['ocp']['setup_info']['cluster_name'] + '-' + str(uuid.uuid4())
    dirPath = os.path.join(localConfig['dir_path'], clusterName)
    openshiftInstallerExe = os.path.join(baseDir, 'openshift-installer', 'openshift-install')
    openshiftInstallerPath = os.path.join(baseDir, 'openshift-installer')
    openshiftInstallerGzPath = os.path.join(baseDir, 'openshift-installer.tar.gz')
    openshiftInstallerRepoLink = os.path.join(
        clusterConfig['ocp']['build_info']['base_repo'],
        clusterConfig['ocp']['build_info']['build_version'],
        clusterConfig['ocp']['build_info']['build_name']
    )

    try:
        log.info('Creating a directory for cluster setup: %s', dirPath)
        os.mkdir(dirPath)

        installConfig = utils.readConfigFile(baseDir, 'config', 'installConfig.yaml')
        _updateInstallConfig(installConfig, clusterConfig, clusterName)
        with open(os.path.join(dirPath, 'install-config.yaml'), 'w') as yaml_file:
            yaml.dump(installConfig, yaml_file, default_flow_style=False)
            log.info('Install config: %s', installConfig)
        if(not os.path.exists(openshiftInstallerExe)):
            log.info('...Downloading openshift-installer')
            urllib.request.urlretrieve(openshiftInstallerRepoLink, openshiftInstallerGzPath)
            log.info('...Unzip openshift-installer')
            tar = tarfile.open(openshiftInstallerGzPath, 'r')
            tar.extractall(openshiftInstallerPath)
            tar.close()
        log.info('!---------------Creating a new cluster ------------!')
        os.system(os.path.join(baseDir, openshiftInstallerExe) + ' create cluster --dir ' + dirPath)
        log.info('!---------------Cluster is created successfully ------------!')
        kubeConfig = utils.readConfigFile(dirPath, 'auth', 'kubeconfig')['clusters'][0]
        server = kubeConfig['cluster']['server']
        password = utils.readConfigFile(dirPath, 'auth', 'kubeadmin-password')
        deployOcs(baseDir, server, password, localConfig['deploy_ocs'])
        sendEmail(baseDir, server, password, clusterName, dirPath, localConfig['enable_notification'])
    except Exception as ex:
        log.warning('Error in ocp cluster setup %s', ex)
        log.warning('...Destroying the cluster')
        os.system(os.path.join(baseDir, openshiftInstallerExe) + ' create destroy --dir ' + dirPath)
