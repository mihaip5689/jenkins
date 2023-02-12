import yaml
import os

def checkSecurityContext():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for fileName in files:
      if fileName.endswith('.yaml'):
        with open(fileName, 'r') as f:
        	configuration = yaml.safe_load(f)
    
        print(configuration)
        spec = configuration['spec']
        containers = spec['containers']
        print('Checking namespace')
        if 'namespace' not in configuration['metadata']:
            print('No specified namespace. Deploying to readOnly ns')
            configuration['metadata']['namespace'] = 'read-only'
        print('Checking user ID and group ID for pod: ' + configuration['metadata']['name'])
        if 'serviceAccountName' not in spec:
            print('No service account set. Granting read only permissions')
            configuration['spec']['serviceAccountName'] = 'read-only-serviceaccount'
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
                print('Setting default user ID and group ID')
                print('Setting read only root file system')
                ct['securityContext'] = { 'allowPrivilegeEscalation': False,
                                          'runAsUser': 1000,
                                          'runAsGroup': 1000,
                                          'readOnlyRootFilesystem': True}
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
                if sC['readOnlyRootFilesystem'] == 'false':
                    print('Insecure container:: Allowed access to root file system.')
                    print('Setting read only root file system for container: ' + ct['name'])
                    ct['securityContext']['readOnlyRootFilesystem'] = True
    
        with open(fileName, 'w') as f:
            yaml.safe_dump(configuration, f, indent=2)
           

if __name__ == "__main__":
  checkSecurityContext()
