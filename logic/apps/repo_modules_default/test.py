from typing import Dict

import yaml

import tools

with open('params.yaml', 'r') as f:
    params = yaml.load(f.read(), Loader=yaml.FullLoader)

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
