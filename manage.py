#!/usr/bin/env python3
import os
import subprocess

import click

cwd = os.path.abspath(os.path.dirname(__file__))


def start():
    subprocess.run("docker-compose down", shell=True, cwd=cwd)
    subprocess.run("DOCKER_BUILDKIT=1 docker-compose up -d", shell=True, cwd=cwd)
    subprocess.run(
        "DOCKER_BUILDKIT=1 docker-compose logs -f -t api", shell=True, cwd=cwd
    )


def stop():
    subprocess.run("docker-compose -p TrucoOnline down", shell=True, cwd=cwd)


def reset():
    # stop()
    cmd = "DOCKER_BUILDKIT=1 docker-compose run api bash -c 'export PYTHONPATH=/app; python3 /app/utils/initialize.py'"
    subprocess.run(cmd, shell=True, cwd=cwd)


def start_db():
    stop()
    subprocess.run(
        "DOCKER_BUILDKIT=1 docker-compose -p TrucoOnline up -d postgres",
        shell=True,
        cwd=cwd,
    )


operations = {"start": start, "stop": stop, "reset": reset, "start_db": start_db}


@click.command()
@click.argument("option", type=click.Choice(list(operations.keys())))
def manage(option):
    operations[option]()


if __name__ == "__main__":
    manage()
