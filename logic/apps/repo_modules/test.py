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

    for ob in objects_to_migrate:
        print(ob)

    print("Proceso terminado OK")
