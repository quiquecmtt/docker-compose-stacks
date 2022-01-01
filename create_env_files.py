import yaml, json
import os, subprocess

WORKINGDIR = os.getcwd()
exceptVars=[
    'ALLPASS'
]

with open("envvars.yaml", "r") as stream:
    envDict = yaml.full_load(stream)

with open("pyconfig.yaml", "r") as stream:
    configDict = yaml.full_load(stream)

if configDict['enableUIDGID'] == False:
    exceptVars.extend(['HUID','HGID'])

stackDict = {
    'root': {'env_file': f'{WORKINGDIR}/.env'}
}
for stack in envDict:
    if stack == "all":
        continue
    stackDict[stack] = {}
    stackDict[stack]['env_file'] = f'{WORKINGDIR}/{stack}/.env'

# print(json.dumps(stackDict, indent = 2))

for stack in stackDict:
    if stack == "root": continue
    print(stack)
    with open(stackDict[stack]['env_file'], "w") as envFile:
        if configDict['enableTraefik']:
            envFile.write('COMPOSE_PATH_SEPARATOR=:\n')
            envFile.write("COMPOSE_FILE=docker-compose.yaml:docker-compose.traefik.yaml\n")
        if envDict['all']['dynamic'] != None:
            for envVar in envDict['all']['dynamic']:
                if envVar in exceptVars: continue
                envFile.write(f"{envVar}={subprocess.run(envDict['all']['dynamic'][envVar].split(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8').strip()}\n")
        if envDict[stack]['dynamic'] != None:
            for envVar in envDict[stack]['dynamic']:
                if envVar in exceptVars: continue
                envFile.write(f"{envVar}={subprocess.run(envDict[stack]['dynamic'][envVar].split(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8').strip()}\n")
        
        if envDict['all']['static'] != None:
            for envVar in envDict['all']['static']:
                if envVar in exceptVars: continue
                envFile.write(f"{envVar}={envDict['all']['static'][envVar]}\n")
        if envDict[stack]['static'] != None:
            for envVar in envDict[stack]['static']:
                if envVar in exceptVars: continue
                envFile.write(f"{envVar}={envDict[stack]['static'][envVar]}\n")