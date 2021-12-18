import requests
import tools

params = tools.get_params()

server_from = params['servers']['from']['name']
namespaces = params['servers']['from']['namespaces']

server_to = params['servers']['to']['name']

jaime_url = params['jaime']['url']


oc = tools.get_client(server_from)
login_success = oc.login()
if not login_success:
    print(f'Error en login {server_from}')
    exit(0)



def post_work(yaml_params: str):
    requests.post(
        url=f'{jaime_url}/api/v1/works',
        data=yaml_params,
        headers={'Content-Type': 'text/plain; charset=utf-8'}
    )


for np in namespaces:

    for ob in ['secrets', 'configmaps', 'buildconfigs']:

        yaml_params = f"""
name: migrate-{np}-{ob}
module: migrate_object
agent:
    type: OPENSHIFT
servers:
    from:
        name: {server_from}
        namespace: {np}
        object: {ob}
    to:
        name: {server_to}
        namespace: {np}
"""

        print(f"{server_to} -> Generando work para {np} {ob}")
        post_work(yaml_params)


print(f"{server_to} -> Proceso terminado")
