import yaml
import pathlib

with open('podToDeploy.yaml', 'r') as f:
    configuration = yaml.safe_load(f)

print(configuration)
spec = configuration['spec']
containers = spec['containers']

if 'securityContext' not in spec:
    print('Insecure pod:: Security Context not configured. Applying default configuration.')
    configuration['spec']['securityContext'] = {'runAsUser': 1000, 'runAsGroup': 1000}
else:
    sC = spec['securityContext']
    if 'runAsUser' in sC and sC['runAsUser'] == 0:
        print('Insecure pod:: Trying to run as root. Applying default configuration.')
        configuration['spec']['securityContext']['runAsUser'] = 1000

    if 'runAsGroup' in sC and sC['runAsGroup'] == 0:
        print('Insecure pod:: Trying to run as root. Applying default configuration.')
        configuration['spec']['securityContext']['runAsGroup'] = 1000

for ct in configuration['spec']['containers']:
    if 'securityContext' not in ct:
        print('Insecure container:: Security Context not configured. Applying default configuration.')
        ct['securityContext'] = {'allowPrivilegeEscalation': False}
    else:
        sC = ct['securityContext']
        if sC['allowPrivilegeEscalation'] == 'true':
            print('Insecure container:: Allowed privilege escalation. Applying default configuration.')
            ct['securityContext'] = {'allowPrivilegeEscalation': False}
configuration['metadata']['name'] = 'secure-pod'

with open('securePodToDeploy.yaml', 'w') as f:
    yaml.safe_dump(configuration, f, indent=2)

fileToRemove = pathlib.Path('./podToDeploy.yaml')
fileToRemove.unlink()
