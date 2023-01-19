import os

PATH = "logic/apps/"

directorios = [f.path for f in os.scandir(PATH) if f.is_dir()]

for directorio in directorios:

    carpetas = [f.path for f in os.scandir(directorio) if f.is_dir()]
    for carpeta in carpetas:
        os.system(f'rm -fr {carpeta}')

    archivos = [f.path for f in os.scandir(directorio) if f.is_file()]
    
    for archivo in archivos:
        
        if len(archivo.replace(directorio, '').split('_')) > 1:

            nombre_archivo = archivo.replace(directorio, '').split('_')[1]
            os.system(f'mv {archivo} {directorio}/{nombre_archivo}')
    
