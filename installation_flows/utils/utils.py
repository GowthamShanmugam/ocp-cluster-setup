import os
import yaml
import json
import time
import subprocess

from threading import Timer

def readConfigFile(baseDir, dirName, filename):
    with open(os.path.join(baseDir, dirName, filename)) as localConfigDump:
        return json.load(localConfigDump) if 'json' in filename else yaml.load(localConfigDump, Loader=yaml.FullLoader)


def readArrayOfConfigFile(baseDir, dirName, filename):
    with open(os.path.join(baseDir, dirName, filename)) as localConfigDump:
        res = json.loads(localConfigDump) if 'json' in filename else yaml.load_all(localConfigDump, Loader=yaml.FullLoader)
        return list(res)

def writeConfigFile(clusterDir, dirName, filename, configs):
    with open(os.path.join(clusterDir, dirName, filename), 'w') as localConfigDump:
        json.dump(configs, localConfigDump) if filename.split(".")[-1] in ['json', 'txt']  else yaml.dump(configs, localConfigDump, default_flow_style=False, explicit_start=True)


def writeArrayOfConfigFile(clusterDir, dirName, filename, config):
    with open(os.path.join(clusterDir, dirName, filename), 'w') as localConfigDump:
        json.dumps(config, localConfigDump) if 'json' in filename else yaml.dump_all(config, localConfigDump, default_flow_style=False, explicit_start=True)


def execute_command(cmds, timeout=300):
    result = []
    for cmd in cmds:
        print(cmd)
        retry = 1
        while(retry <= 2):
            result = []
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            timer = Timer(timeout, p.kill)
            try:
                timer.start()
                while p.poll() is None:
                    time.sleep(0.5)

                retry += 1
                res, err = p.communicate()
                if err:
                    raise RuntimeError('Command ' + cmd + ' Failed: ' + err)
                res = res.decode('utf-8')
                if res != '':
                    result.append(res)
            finally:
                retry += 1
                if retry <= 2:
                    print("Timed out the command and retying....")
                timer.cancel()
    return result
