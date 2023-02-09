import yaml
import pathlib

with open('podToDeploy.yaml', 'r') as f:
    configuration = yaml.safe_load(f)

print(configuration)
spec = configuration['spec']
containers = spec['containers']

print('Checking user ID and group ID for pod: ' + configuration['metadata']['name'])
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
        print('Insecure container:: Security Context not configured.')
        print('Applying default configuration for container: ' + ct['name'])
        print('Disabling privilege escalation')
        ct['securityContext']['allowPrivilegeEscalation'] = False
        print('Setting default user ID and group ID')
        ct['securityContext']['runAsUser'] = 1000
        ct['securityContext']['runAsGroup'] = 1000
        print('Setting read only root file system')
        ct['securityContext']['readOnlyRootFileSystem'] = True
    else:
        sC = ct['securityContext']
        if 'runAsUser' in sC and sC['runAsUser'] == 0:
            print('Insecure container. Trying to run as root.')
            print('Setting default user ID for container: ' + ct['name'])
            ct['securityContext']['runAsUser'] = 1000
        if 'runAsGroup' in sC and sC['runAsGroup'] == 0:
            print('Insecure container. Trying to run as root.')
            print('Setting default group ID for container: ' + ct['name'])
            ct['securityContext']['runAsGroup'] = 1000
        if sC['allowPrivilegeEscalation'] == 'true':
            print('Insecure container:: Allowed privilege escalation.')
            print('Disabling privilege escalation for container: ' + ct['name'])
            ct['securityContext']['allowPrivilegeEscalation'] = False
        if sC['readOnlyRootFileSystem'] == 'false':
            print('Insecure container:: Allowed access to root file system.')
            print('Setting read only root file system for container: ' + ct['name'])
            ct['securityContext']['readOnlyRootFileSystem'] = True


# for ct in configuration['spec']['containers']:
#     print('Checking user ID and group ID for container: ' + ct['name'])
#     if 'securityContext' not in ct:
#         print('Insecure container:: Security Context not configured. Applying default configuration.')
#         print('Disabling privilege escalation')
#         ct['securityContext'] = {'allowPrivilegeEscalation': False}
#     else:
#         sC = ct['securityContext']
#         if sC['allowPrivilegeEscalation'] == 'true':
#             print('Insecure container:: Allowed privilege escalation. Applying default configuration.')
#             ct['securityContext'] = {'allowPrivilegeEscalation': False}
#
#
# for ct in configuration['spec']['containers']:
#     print('Checking privilege escalation for container: ' + ct['name'])
#     if 'securityContext' not in ct:
#         print('Insecure container:: Security Context not configured. Applying default configuration.')
#         ct['securityContext'] = {'allowPrivilegeEscalation': False}
#     else:
#         sC = ct['securityContext']
#         if sC['allowPrivilegeEscalation'] == 'true':
#             print('Insecure container:: Allowed privilege escalation. Applying default configuration.')
#             ct['securityContext'] = {'allowPrivilegeEscalation': False}

configuration['metadata']['name'] = 'secure-pod'

with open('securePodToDeploy.yaml', 'w') as f:
    yaml.safe_dump(configuration, f, indent=2)

fileToRemove = pathlib.Path('./podToDeploy.yaml')
fileToRemove.unlink()
