import re
from typing import Dict

import tools


def exec(params: Dict[str, any]):

    server_from = params['servers']['from']['name']
    namespace_from = params['servers']['from']['namespace']
    object_from = params['servers']['from']['object']
    only_from = params['servers']['from'].get('only', [])
    ignore_from = params['servers']['from'].get('ignore', [])

    oc_from = tools.get_oc(server_from)
    oc_from.login()

    print("Obtieniendo todos los objetos")
    objects_to_migrate = [
        ob
        for ob
        in oc_from.exec(f'get {object_from} -n {namespace_from} -o custom-columns=NAME:.metadata.name').split('\n')[1:-1]
    ]
    print(f"{server_from} -> Objetos entontrados: {len(objects_to_migrate)}")

    tools.sh('mkdir yamls')

    objects_to_migrate_filtered = []
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
        objects_to_migrate_filtered.append(ob)

    print(f"{server_from} -> traidos {len(objects_to_migrate_filtered)} yamls")

    for ob in objects_to_migrate_filtered:
        print(ob)

    print("Proceso terminado OK")
