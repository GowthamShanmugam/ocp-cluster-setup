# OCP Cluster Setup

## Dependencies
   1. [Openshift Client](https://mirror.openshift.com/pub/openshift-v4/clients/oc/4.4/)
   2. Linux Cron (CentOS/RHEL/Fedora: yum install cronie , Linux/Unix: apt-get install cron)
   3. Configure your cloud platform credentials in local
   4. Any python3 version (https://computingforgeeks.com/install-latest-python-on-centos-linux/)
   
## Configure virtual environment
    1. yum install python3-virtualenv
    2. virtualenv --python=python3.x ~/ocp-cluster-setup/venv
    3. cd ~/ocp-cluster-setup/venv/bin
    4. source activate
    5. pip3 install -r ~/ocp-cluster-setup/requirements.txt 

## This script provides 2 types of deployment
    1. Immediate Deployment
    2. Scheduled Deployment (Cron Job)

### For immediate deployment
    python3 ~/ocpClusterSetup/main.py

### For scheduled deployment
    python3 ~/ocpClusterSetup/main.py true

### Deployment configuration
    Before deployment make sure these mandatory changes are done
    
    For fast cluster deployment:
    ------------------------------------------------------------------------------------------------
    1. Modify config/ClusterConfig.json: 
   
        "ocp" : {
            "setup_info": {
                "pull_secret": ""   // Add your pull secret which should have ci build access
            },    
        }


    2. Modify config/LocalConfig.json:
  
        {
            "cron_schedule": "0 9 * * 1-5",  // week days 9AM, For more info: https://crontab.guru
            "dir_path": "/tmp",  // cluster setup workspace
            "refresh_openshift_installer": false, // To control installer download
        }
     
     
    3. Modify config/emailConfig.json file as per your need:
        
        {
            "email_id" : "ocpclusterbot@gmail.com", // I prefer to use this for our team
            "email_pass": "",    // Mandatory
            "receiver_emails": ["abc@gmail.com", "xyz@gmail.com"],    // list of email
         }
         


    For cluster deployment with more custom configurations:
    --------------------------------------------------------------------------------------------------
    1. Paste you own intallConfig content on custom_templates/installConfig.yaml
    
    2. Go to config/clusterConfig.json and enable "custom_install_config_template": true 
    
    (Script wont take any config from setup_info of clusterConfig.json)
     
 ### Logs
     ocpClusterSetup/log/ocpClusterInstallation.log (script related logs)
     /tmp/{clustername-uuid}/.openshift_install.log (openshift-installer logs)
     
 ### Destroy Cluster
     ocpClusterSetup/openshift-installer/openshift-install destroy cluster --dir {cluster dir path}  // for path check email/script-logs
 
 ### Note
     * For any changes in OCP build version (config file) , Please remove ocpClusterSetup/openshift-installer and ocpClusterSetup/openshift-installer.tar.gz. Otherwise, Tt will not consider the new version change.
     * If you dont prefer the above option, Please enable "refresh_openshift_installer" flag( in localConfig). It will download the new build for every new cluster creation request.
        


