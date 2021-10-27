from typing import Dict

from logic.apps.repo_modules_default import tools


def exec(params: Dict[str, any]):

    server = params['server']['name']
    namespace = params['server']['namespace']

    image_url = params['jenkins']['image']['url']
    image_tag = params['jenkins']['image']['tag']

    is_namespace = params['jenkins']['imageStream']['namespace']
    is_name = params['jenkins']['imageStream']['name']
    is_tag = params['jenkins']['imageStream']['tag']

    conf_template = params['jenkins']['config']['template']
    conf_ram = params['jenkins']['config']['memoryRAM']
    conf_vol = params['jenkins']['config']['memoryVolume']
    conf_storage_class = params['jenkins']['config']['storageClass']

    oc = tools.get_oc(server)
    oc.login()

    oc.exec('get pods')

    # print(f'Creando {namespace}')
    # # oc.exec(f'new-project {namespace}')
    # oc.exec(f'get pods')
    # print(f'\n\n')

#     print(f'Creando PVC en {namespace} con nombre jenkins-persistent')
#     tools.sh(f""" echo "\
# kind: PersistentVolumeClaim
# apiVersion: v1
# metadata:
# name: jenkins
# labels:
#     app: jenkins-persistent
#     template: {conf_template}-template
# spec:
# accessModes:
#     - ReadWriteMany
# resources:
#     requests:
#     storage: {conf_vol}
# storageClassName: {conf_storage_class}
# volumeMode: Filesystem \
# " | {oc.binary_name()} -n {namespace} apply -f -
#     """)
#     print(f'\n\n')

#     print(f'Descargando imagen {image_url}:{image_tag} en {is_namespace}')
#     oc.exec(
#         f'import-image openshift4/{is_name}:{is_tag} --from={image_url}:{image_tag} --confirm -n {is_namespace}')
#     print(f'\n\n')

#     print(f'Instalando Jenkins en {namespace}')
#     oc.exec(f"""
#     oc new-app -n {namespace} \
# 		--template={conf_template} \
# 		--param=NAMESPACE={is_namespace} \
# 		--param=MEMORY_LIMIT={conf_ram} \
# 		--param=VOLUME_CAPACITY={conf_vol} \
# 		--param=JENKINS_IMAGE_STREAM_TAG={is_name}:{is_tag}
#     """)
#     print(f'\n\n')

#     print(f'Creando CRB con nombre jenkins-cluster-admin')
#     tools.sh(f""" echo "\
# kind: ClusterRoleBinding
# apiVersion: rbac.authorization.k8s.io/v1
# metadata:
#   name: jenkins-cluster-admin
# subjects:
#   - kind: ServiceAccount
#     name: jenkins
#     namespace: {namespace}
# roleRef:
#   apiGroup: rbac.authorization.k8s.io
#   kind: ClusterRole
#   name: cluster-admin \
# " | {oc.binary_name()} -n {namespace} apply -f -
#     """)
#     print(f'\n\n')

#     print(f'Configurando Jenkins')
#     oc.exec(f"""set -n {namespace} env dc jenkins \
# JAVA_TOOL_OPTIONS="-Dhttps.protocols=TLSv1.2" \
# JAVA_OPTS="-Dhttps.protocols=TLSv1.2 -Djdk.tls.client.protocols=TLSv1.2" """)
#     print(f'\n\n')
