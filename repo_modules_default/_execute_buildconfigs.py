import re
import time

import tools

params = tools.get_params()

size = params['lot']['size']
wait_time_seconds = params['lot']['wait_time_seconds']

server = params['servers']['name']
namespace = params['servers']['namespace']
only = params['servers'].get('only', [])
ignore = params['servers'].get('ignore', [])


oc = tools.get_client(server)

login_success = oc.login()
if not login_success:
    print(f'Error en login {server}')
    exit(0)


print(f"{server} -> Obtieniendo todos los buildconfigs")

bc_list = [
    bc
    for bc
    in oc.exec(f'get bc -n {namespace} -o custom-columns=NAME:.metadata.name').split('\n')[1:]
]


print(f"{server} -> bc entontrados: {len(bc_list)}")


bc_list_to_execute = []

for bc in bc_list:

    if only:
        match_all_regex = len(
            [regex for regex in only if re.match(regex, bc)]) == len(only)
        if not match_all_regex:
            continue

    if ignore:
        match_any_regex = any(
            True for regex in ignore if re.match(regex, bc))
        if match_any_regex:
            continue

    bc_list_to_execute.append(bc)


print(f"{server} -> bc para ejecutar: {len(bc_list_to_execute)}")


print(f"{server} -> Comenzando ejecucion")

lot_exec_count = 0
for bc in bc_list_to_execute:

    lot_exec_count += 1

    print(f"{server} -> Ejecutando bc: {bc}")
    oc.exec(f'start-build {bc} -n {namespace}')

    if lot_exec_count == size:
        lot_exec_count = 0
        time.sleep(float(wait_time_seconds))


print(f"{server} -> Proceso terminado")
