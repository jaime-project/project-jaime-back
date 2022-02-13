import logging
import os
import re

import yaml
import tools

###########################################
# VARS
###########################################

params = tools.get_params()

cluster_from = params['servers']['from']['name']
namespace_from = params['servers']['from']['namespace']
object_from = params['servers']['from']['object']
only_from = params['servers']['from'].get('only', [])
ignore_from = params['servers']['from'].get('ignore', [])

cluster_to = params['servers']['to']['name']
namespace_to = params['servers']['to']['namespace']
method_to = params['servers']['to'].get('method', 'apply')
force = params['servers']['to'].get('force', 'false')


###########################################
# SCRIPT
###########################################

# file BK
bk_file_path = f'/data/migrate_{object_from}_{cluster_from}_{namespace_from}_to_{cluster_to}_{namespace_to}.txt'

if str(force).lower() == 'true' or not os.path.exists(bk_file_path):
    tools.sh(f'> {bk_file_path}')

with open(bk_file_path, 'r') as f:
    migrated_bk = f.read().split('\n')


# login server from
oc_from = tools.get_client(cluster_from)
login_success = oc_from.login()
if not login_success:
    print(f'Error en login {cluster_from}')
    exit(0)


# obteniendo yamls
print(f"{cluster_from} -> Obtieniendo todos los objetos")
objects = [
    ob
    for ob
    in oc_from.exec(f'get {object_from} -n {namespace_from} -o custom-columns=NAME:.metadata.name', echo=False).split('\n')[1:]
]

tools.sh('mkdir yamls/')

objects_to_migrate = []
for ob in objects:

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

    if ob in migrated_bk:
        continue

    print(f'{cluster_from} -> Obteniendo {ob}')
    oc_from.exec(f'get {object_from} {ob} -n {namespace_from} -o yaml > yamls/{ob}.yaml')
    objects_to_migrate.append(ob)

print(f'{cluster_from} -> por migrar {len(objects_to_migrate)} {object_from}')


# login server to
oc_to = tools.get_client(cluster_to)
login_success = oc_to.login()
if not login_success:
    print(f'Error en login {cluster_to}')
    exit(0)


# migrar yamls
oc_to.exec(f'new-project {namespace_to}')

yamls_errors = []
for ob in objects_to_migrate:
    try:
        with open(f'yamls/{ob}.yaml', 'r') as file:
            dic_yaml = yaml.load(file, Loader=yaml.FullLoader)
        
        dic_yaml['metadata'].pop('managedFields', None)
        dic_yaml['metadata'].pop('creationTimestamp', None)
        dic_yaml['metadata'].pop('namespace', None)
        dic_yaml['metadata'].pop('resourceVersion', None)
        dic_yaml['metadata'].pop('selfLink', None)
        dic_yaml['metadata'].pop('uid', None)
        dic_yaml.pop('status', None)

        yaml_to_apply = yaml.dump(dic_yaml, default_flow_style=False)
        with open(f'yamls/{ob}.yaml', 'w') as f:
            f.write(yaml_to_apply)

        oc_to.exec(f'{method_to} -n {namespace_to} -f yamls/{ob}.yaml')
        print(f'{cluster_to} -> Migrado {ob}')
        tools.sh(f"""echo "{ob}" >> {bk_file_path}""")

    except Exception as e:
        yamls_errors.append(ob)
        print(f'{cluster_to} -> ERROR al migrar {ob}')
        print(e.with_traceback())

if yamls_errors:
    logging.error(f'{cluster_to} -> Yamls con errores al migrar:')
    for y_error in yamls_errors:
        logging.error(
            f'{cluster_to} -> {y_error}')


print(f'{cluster_to} -> proceso terminado')
tools.sh(f'rm -fr {bk_file_path}')