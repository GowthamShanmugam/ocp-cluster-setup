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
            cmd = ['oc --kubeconfig ' + os.path.join(clusterDir, 'auth/kubeconfig') + ' get  ClusterServiceVersion ' + acmConfig['acm_subscription'] + ' -n open-cluster-management -o=jsonpath={.status.phase}']
            checkStatus(clusterDir, cmd, 'Succeeded')
            utils.execute_command(['oc --kubeconfig ' + os.path.join(clusterDir, 'auth/kubeconfig') + ' apply -f ' + os.path.join(baseDir, 'templates', 'acmHubConfig.yaml')])

            log.info("Waiting for multi cluster hub to be up")
            cmd = ['oc --kubeconfig ' + os.path.join(clusterDir, 'auth/kubeconfig') + ' get  MultiClusterHub multiclusterhub -n open-cluster-management -o=jsonpath={.status.phase}']
            checkStatus(clusterDir, cmd, 'Running', 10)

            time.sleep(60)
            log.info("Creating managed cluster")
            acmconfigPath = os.path.join(clusterDir, 'acmConfig.yaml')
            utils.execute_command(['oc --kubeconfig ' + os.path.join(clusterDir, 'auth/kubeconfig') + ' apply -f ' + os.path.join(baseDir, 'templates', 'acmManagedCluster.yaml')])
            utils.execute_command(['oc --kubeconfig ' + os.path.join(clusterDir, 'auth/kubeconfig') + ' apply -f ' + os.path.join(baseDir, 'templates', 'acmAddonConfig.yaml')])
            time.sleep(30)
            utils.execute_command([
                'oc get --kubeconfig ' + os.path.join(clusterDir, 'auth/kubeconfig') + ' Secret ocscluster-import -n ocscluster -o=jsonpath={.data.\'crds\.yaml\'} | base64 -d > ' + acmconfigPath,
                'oc --kubeconfig ' + acmConfig['target_cluster_kubeconfig_path'] + ' apply -f ' + acmconfigPath
            ])
            time.sleep(30)
            utils.execute_command([
                'oc get --kubeconfig ' + os.path.join(clusterDir, 'auth/kubeconfig') + ' Secret ocscluster-import -n ocscluster -o=jsonpath={.data.\'import\.yaml\'} | base64 -d > ' + acmconfigPath,
                'oc --kubeconfig ' + acmConfig['target_cluster_kubeconfig_path'] + ' apply -f ' + acmconfigPath
            ])
        else:
            log.warning("ACM subscription is skipped")
    except Exception as ex:
        log.error("Unable to subscribe ACM: %s", ex, exc_info=True)

def checkStatus(clusterDir, cmd, expected, retry=1):
    status = utils.execute_command(cmd)
    print("retry: " + str(retry))
    try:
        if status[0] == expected or retry >= 6:
            return
    except Exception:
        if retry >= 5:
            return


    time.sleep(60)
    checkStatus(clusterDir, cmd, expected, retry+1)

