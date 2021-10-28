from typing import Dict

from logic.apps.repo_modules_default import tools


def exec(params: Dict[str, any]):

    server_from = params['servers']['from']['name']
    namespace_from = params['servers']['from']['namespace']
    object_from = params['servers']['from']['object']

    oc_from = tools.get_oc(server_from)
    oc_from.login()

    print(f"{server_from} -> Obtieniendo todos los objetos")
    objects_to_migrate = [
        ob
        for ob
        in oc_from.exec(f'get {object_from} -n {namespace_from} -o custom-columns=NAME:.metadata.name').split('\n')[1:-1]
    ]
    print(f"{server_from} -> Objetos entontrados: {len(objects_to_migrate)}")

    for ob in objects_to_migrate:
        print(ob)


    print(f"{server_from} -> Proceso terminado OK")

    for ob in objects_to_migrate:
        yaml_dict = oc_from.exec(
            f'get {object_from} {ob} -n {namespace_from} -o yaml')
        print(yaml_dict)
