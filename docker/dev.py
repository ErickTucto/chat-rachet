import os
import sys
from subprocess import Popen, PIPE, run
from dotenv import load_dotenv

VERSION="dev v2021.07.01"

HELP=f"""{VERSION} - por Erick Tucto
Helper que facilita el uso de los contenedores.

Uso:
  $ python dev.py [ORDEN|SERVICIO] [PARAMETROS]

ORDEN:
    start        Iniciar los contenedores para el entorno de desarrollo.
    stop         Detener los contenedores para el entorno de desarrollo.
    build        Construir los contenedores para el entorno de desarrollo.

SERVICIO:
    composer     Atajo para usar el composer del proyecto.
    npm          Atajo para usar el npm del proyecto.

PARAMETROS:
    --help       Ayudas.
    --version    Obtener la version del script
"""


def console(command):
    p = Popen(command, shell=True, stdout=PIPE, encoding="utf-8")
    out, err = p.communicate()
    return (p.returncode, out, err)


def verify(args):
    full_path = os.getcwd()
    path_env = os.path.join(full_path, ".env")
    path_key_private = os.path.join(full_path, "php", "aramark")
    path_key_public = os.path.join(full_path, "php", "aramark.pub")
    if os.path.exists(path_env) == False:
        print("No agregaste tus variables de entorno. Tiene .env.example como ejemplo.")
        return 0
    if os.path.exists(path_key_private) == False or os.path.exists(path_key_public) == False:
        print("Necesitamos tus llaves ssh para Aramark")
        print("Privada: php/aramark")
        print("Publica: php/aramark.pub")
        return 0
    print("Todo esta correcto.")
    return 1


def start(args):
    detach = len(args) == 2 and args[1] in ["-d", "--detach", "-detach"]
    if detach:
        Popen("docker-compose up &", shell=True, stdout=PIPE)
    else:
        run(["docker-compose", "up"])
    return 1


def stop(args):
    run(["docker-compose", "down"])
    return 1


def status(args):
    run(["docker-compose", "ps"])
    return 1


def composer(args):
    user = os.getuid()
    group = "www-data"
    run(["docker-compose", "exec", "-u", f"{user}:{group}", "php"] + args)
    return 1


def artisan(args):
    run(["docker-compose", "exec", "php", "php"] + args)
    return 1


def docker(args):
    run(["docker-compose"] + args)
    return 1


def main(args):
    if len(args) == 0 or args[0] in ["-h", "--help", "-help"]:
        print(HELP)
        return 1
    if args[0] in ["-v", "--version", "-version"]:
        print(VERSION)
        return 1
    ORDEN=args[0]
    switcher={
        "start": start,
        "stop": stop,
        "status": status,
        "composer": composer,
        "artisan": artisan,
        "verify": verify,
    }
    RUN_STOP = ORDEN == "start"
    try:
        funcion = switcher.get(ORDEN, docker)
        return funcion(args)
    except KeyboardInterrupt:
        if RUN_STOP:
            stop([])
        return 1


if __name__ == '__main__':
    load_dotenv()
    args = sys.argv[1:]
    main(args)
