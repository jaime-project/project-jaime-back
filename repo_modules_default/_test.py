import tools

params = tools.get_params()

cluster_from = params['servers']['from']['name']
namespace_from = params['servers']['from']['namespace']
object_from = params['servers']['from']['object']

oc_from = tools.get_client(cluster_from)
login_success = oc_from.login()
if not login_success:
    print(f'Error en login {cluster_from}')
    exit(0)

print(f"{cluster_from} -> Obtieniendo todos los objetos")
objects_to_migrate = [
    ob
    for ob
    in oc_from.exec(f'get {object_from} -n {namespace_from} -o custom-columns=NAME:.metadata.name', echo=False).split('\n')[1:]
]

print(f"{cluster_from} -> Objetos entontrados: {len(objects_to_migrate)}")

for ob in objects_to_migrate:
    print(ob)

print(f"{cluster_from} -> Proceso terminado OK")
