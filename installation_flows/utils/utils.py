import os
import yaml
import json

def readConfigFile(baseDir, dirName, filename):
    with open(os.path.join(baseDir, dirName, filename)) as localConfigDump:
        return json.load(localConfigDump) if 'json' in filename else yaml.load(localConfigDump, Loader=yaml.FullLoader)


def readArrayOfConfigFile(baseDir, dirName, filename):
    with open(os.path.join(baseDir, dirName, filename)) as localConfigDump:
        res = json.loads(localConfigDump) if 'json' in filename else yaml.load_all(localConfigDump, Loader=yaml.FullLoader)
        return list(res)

def writeConfigFile(clusterDir, dirName, filename, configs):
    with open(os.path.join(clusterDir, dirName, filename), 'w') as localConfigDump:
        json.dump(configs, localConfigDump) if 'json' in filename else yaml.dump(configs, localConfigDump, default_flow_style=False, explicit_start=True)


def writeArrayOfConfigFile(clusterDir, dirName, filename, config):
    with open(os.path.join(clusterDir, dirName, filename), 'w') as localConfigDump:
        json.dumps(config, localConfigDump) if 'json' in filename else yaml.dump_all(config, localConfigDump, default_flow_style=False, explicit_start=True)
