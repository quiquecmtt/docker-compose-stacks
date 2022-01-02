from types import DynamicClassAttribute
import yaml, json
import os, subprocess

WORKINGDIR = os.getcwd()
PYCONFIGDIR = f"{WORKINGDIR}/pyconfig.d"

def init():
    exceptVars=[
        'ALLPASS'
    ]

    with open(f"{PYCONFIGDIR}/envvars.yaml", "r") as stream:
        envDict = yaml.full_load(stream)

    with open(f"{PYCONFIGDIR}/pyconfig.yaml", "r") as stream:
        configDict = yaml.full_load(stream)

    if configDict['enableUIDGID'] == False:
        exceptVars.extend(['HUID','HGID'])

    return envDict, configDict, exceptVars


def define_env_files(envDict):
    for stack in envDict:
        if stack == "all": continue
        envDict[stack]['env_file'] = f'{WORKINGDIR}/{stack}/.env'

def define_compose_env_vars(envDict, configDict):
    for stack in envDict:
        envDict[stack]['compose'] = {}
        if stack == "all": continue
        # Get info from pyconfig
        composeFiles = configDict['stacks'][stack]['files']
        composeNetworkFile = f"docker-compose.{'' if configDict['enableTraefik'] else 'no'}traefik.yaml"
        composeFiles.append(composeNetworkFile)
        composeProfiles = [profile for profile in configDict['stacks'][stack]['profiles'] if configDict['stacks'][stack]['profiles'][profile]]
        pathSeparator = ":"
        # Add compose info to dict
        envDict[stack]['compose']['COMPOSE_PATH_SEPARATOR'] = pathSeparator
        envDict[stack]['compose']['COMPOSE_FILE'] = pathSeparator.join(composeFiles)
        if composeProfiles:
            envDict[stack]['compose']['COMPOSE_PROFILES'] = ','.join(composeProfiles)

        print(stack)
        print(composeFiles)
        print(composeProfiles)
        print(composeNetworkFile)

def dict_to_env_file(dict, envFilePath):
    with open(envFilePath, "a") as envFile:
        if dict['compose'] != None:
            for envVar in dict['compose']:
                if envVar in exceptVars: continue
                envFile.write(f"{envVar}={dict['compose'][envVar]}\n")
        if dict['dynamic'] != None:
            for envVar in dict['dynamic']:
                if envVar in exceptVars: continue
                
                shCommand = dict['dynamic'][envVar].split() if isinstance(dict['dynamic'][envVar], str) else dict['dynamic'][envVar]
                shOutput = subprocess.run(shCommand, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8').strip()
                envFile.write(f"{envVar}={shOutput}\n")
        if dict['static'] != None:
            for envVar in dict['static']:
                if envVar in exceptVars: continue
                envFile.write(f"{envVar}={dict['static'][envVar]}\n")

def gen_env_files(envDict):
    for stack in envDict:
        if stack == "all": continue
        envFilePath = envDict[stack]['env_file'] # + 'test'
        with open(envFilePath, "w"): pass
        dict_to_env_file(envDict[stack], envFilePath)
        dict_to_env_file(envDict['all'], envFilePath)



# print(json.dumps(stackDict, indent = 2))

# for stack in stackDict:
#     if stack == "root": continue
#     print(stack)
#     with open(stackDict[stack]['env_file'], "w") as envFile:
#         if configDict['enableTraefik']:
#             envFile.write('COMPOSE_PATH_SEPARATOR=:\n')
#             envFile.write("COMPOSE_FILE=docker-compose.yaml:docker-compose.traefik.yaml\n")
#         if envDict['all']['dynamic'] != None:
#             for envVar in envDict['all']['dynamic']:
#                 if envVar in exceptVars: continue
#                 envFile.write(f"{envVar}={subprocess.run(envDict['all']['dynamic'][envVar].split(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8').strip()}\n")
#         if envDict[stack]['dynamic'] != None:
#             for envVar in envDict[stack]['dynamic']:
#                 if envVar in exceptVars: continue
#                 envFile.write(f"{envVar}={subprocess.run(envDict[stack]['dynamic'][envVar].split(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8').strip()}\n")
        
#         if envDict['all']['static'] != None:
#             for envVar in envDict['all']['static']:
#                 if envVar in exceptVars: continue
#                 envFile.write(f"{envVar}={envDict['all']['static'][envVar]}\n")
#         if envDict[stack]['static'] != None:
#             for envVar in envDict[stack]['static']:
#                 if envVar in exceptVars: continue
#                 envFile.write(f"{envVar}={envDict[stack]['static'][envVar]}\n")

if __name__ == '__main__':
    envDict, configDict, exceptVars = init()
    # print(json.dumps(envDict, indent = 2))
    define_env_files(envDict)
    # print(json.dumps(envDict, indent = 2))
    define_compose_env_vars(envDict, configDict)
    print(json.dumps(envDict, indent = 2))
    gen_env_files(envDict)

    