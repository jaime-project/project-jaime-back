import logging
import os
import re
from typing import Dict

import yaml
import tools


params = tools.get_params()

server_from = params['servers']['from']['name']
namespace_from = params['servers']['from']['namespace']
object_from = params['servers']['from']['object']
only_from = params['servers']['from'].get('only', [])
ignore_from = params['servers']['from'].get('ignore', [])

server_to = params['servers']['to']['name']
namespace_to = params['servers']['to']['namespace']
method_to = params['servers']['to'].get('method', 'apply')

oc_from = tools.get_client(server_from)
login_success = oc_from.login()
if not login_success:
    print(f'Error en login {server_from}')
    exit(0)


print(f"{server_from} -> Obtieniendo todos los objetos")
objects_to_migrate = [
    ob
    for ob
    in oc_from.exec(f'get {object_from} -n {namespace_from} -o custom-columns=NAME:.metadata.name').split('\n')[1:]
]
print(f"{server_from} -> Objetos entontrados: {len(objects_to_migrate)}")

tools.sh('mkdir yamls/')

for ob in objects_to_migrate:

    if only_from:
        match_all_regex = len(
            [regex for regex in only_from if re.match(regex, ob)]) == len(only_from)
        if not match_all_regex:
            continue

    if ignore_from:
        match_any_regex = any(
            True for regex in ignore_from if re.match(regex, ob))
        if match_any_regex:
            continue

    print(f'{server_from} -> Obteniendo {ob}')
    oc_from.exec(
        f'get {object_from} {ob} -n {namespace_from} -o yaml > yamls/{ob}.yaml')


oc_to = tools.get_client(server_to)
login_success = oc_to.login()
if not login_success:
    print(f'Error en login {server_to}')
    exit(0)


oc_to.exec(f'new-project {namespace_to}')

yamls_to_migrate = []
for _, _, file_name in os.walk('yamls/'):
    yamls_to_migrate.extend(file_name)
print(f'{server_to} -> Por migrar {len(yamls_to_migrate)} {object_from}')

yamls_errors = []
for yaml_to_migrate in yamls_to_migrate:
    try:
        with open(f'yamls/{yaml_to_migrate}', 'r') as file:
            dic_yaml = yaml.load(file, Loader=yaml.FullLoader)

        dic_yaml['metadata'].pop('creationTimestamp', None)
        dic_yaml['metadata'].pop('namespace', None)
        dic_yaml['metadata'].pop('resourceVersion', None)
        dic_yaml['metadata'].pop('selfLink', None)
        dic_yaml['metadata'].pop('uid', None)
        dic_yaml.pop('status', None)

        yaml_to_apply = yaml.dump(dic_yaml, default_flow_style=False)
        with open(f'yamls/{yaml_to_migrate}', 'w') as f:
            f.write(yaml_to_apply)

        oc_to.exec(f'{method_to} -n {namespace_to} -f yamls/{yaml_to_migrate}')
        print(f'{server_to} -> Migrado {yaml_to_migrate}')

    except Exception as e:
        logging.exception(e)
        logging.error(f'{server_to} -> ERROR al migrar {yaml_to_migrate}')

        yamls_errors.append(yaml_to_migrate)
        print(e.args)

if yamls_errors:
    logging.error(f'{server_to} -> Yamls con errores al migrar:')
    for y_error in yamls_errors:
        logging.error(
            f'{server_to} -> {y_error}')
