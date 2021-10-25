import logging
import os
import re
from typing import Dict

import yaml

import tools


def exec(params: Dict[str, any]):

    server_from = params['servers']['from']['name']
    namespace_from = params['servers']['from']['namespace']
    object_from = params['servers']['from']['object']
    only_from = params['servers']['from'].get('only', [])
    ignore_from = params['servers']['from'].get('ignore', [])

    server_to = params['servers']['to']['name']
    namespace_to = params['servers']['to']['namespace']
    method_to = params['servers']['to'].get('method', 'apply')

    oc_from = tools.get_oc(server_from)
    oc_from.login()

    objects_to_migrate = [
        ob
        for ob
        in oc_from.exec(f'get {object_from} -n {namespace_from} -o custom-columns=NAME:.metadata.name').split('\n')[1:-1]
    ]

    tools.sh('mkdir yamls')

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

    oc_to = tools.get_oc(server_to)
    oc_to.login()

    yamls_to_migrate = [
        nombre_archivo
        for _, _, nombre_archivo in os.walk('yamls/')
    ]
    print(f'{server_to} -> Por migrar {len(yamls_to_migrate)} {object_from}')

    yamls_errors = []
    for yaml_to_migrate in yamls_to_migrate:
        try:
            with open(f'yamls/{yaml_to_migrate}') as file:
                dic_yaml = yaml.load(file, Loader=yaml.FullLoader)

            dic_yaml['metadata'].pop('creationTimestamp', None)
            dic_yaml['metadata'].pop('namespace', None)
            dic_yaml['metadata'].pop('resourceVersion', None)
            dic_yaml['metadata'].pop('selfLink', None)
            dic_yaml['metadata'].pop('uid', None)
            dic_yaml.pop('status', None)

            yaml_to_apply = yaml.dump(dic_yaml, default_flow_style=False)

            tools.sh(
                f'echo "{yaml_to_apply}" | {oc_to.server.binary_name()} {method_to} -n {namespace_to} -f -')
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
