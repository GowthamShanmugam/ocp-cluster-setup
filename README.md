# OCP Cluster Setup

## This script provides 2 types of deployment:
    1. Immediate Deployment
    2. Scheduled Deployment (Cron Job)

### For immediate deployment
    PycharmProjects/ocpClusterSetup/venv/bin/python3.9 main.py

### For scheduled deployment
    PycharmProjects/ocpClusterSetup/venv/bin/python3.9 main.py true

### Deployment configuration
    Before deployment make sure these changes are done
    
    1. Modify config/ClusterConfig.json file as per your need: 
   
        {
          "ocp" : {
              "setup_info": {
                 "cluster_name": "clusterName",   // No need to change for each deployment, script will appened uuid
                 "base_domain": "devcluster.openshift.com",
                 "platform": "", // aws, gcp .....
                 "type": "", // machine type for (e.g) aws machine type m4.2xlarge
                 "region": "",  // region for (e.g) aws region us-east-1
                 "pull_secret": ""       // Mandatory
              },
              "build_info": {
                  "base_repo": "https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp-dev-preview",
                  "build_version": "latest-4.8",  // find names in above URL
                  "build_name": "openshift-install-linux.tar.gz"  // Mostly no need to change this
              }
          },
          "ocs": {
              "ocs_build": "quay.io/rhceph-dev/ocs-registry:4.8.0-303.ci"  // refer (https://storage-jenkins-csb-ceph.cloud.paas.psi.redhat.com/job/ocs-ci/)
          }
        }


    2. Modify config/LocalConfig.json file as per your need:
  
        {
            "cron_setup": {
                "cron_schedule": "0 09 * * TUE" // For more help: https://crontab.guru/  (only for scheduled deployment)
            },
            "dir_path": "/tmp"  // Directory will created like /tmp/{clusterName-uuid} (you can find exact name in PycharmProjects/ocpClusterSetup/log/ocpClusterInstallation.log)
        }
     
     
    3. Modify config/emailConfig.json file as per your need:
        
         {
             "email_id" : "tendrlalerting@gmail.com", // Email id should have (Allow less secure apps permission enabled), for now i prefer to use this
             "email_pass": "",
              "receiver_emails": [""],    // list of email
              "auth": "ssl",
              "email_smtp_port": 465,
              "email_smtp_server": "smtp.gmail.com"
         }
        

