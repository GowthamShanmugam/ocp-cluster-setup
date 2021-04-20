import os
import yaml
import json

def readConfigFile(baseDir, dirName, filename):
    with open(os.path.join(baseDir, dirName, filename)) as localConfigDump:
        return json.load(localConfigDump) if 'json' in filename else yaml.load(localConfigDump, Loader=yaml.FullLoader)
