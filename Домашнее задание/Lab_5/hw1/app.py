from time import sleep
from typing import List
from flask import Flask
import subprocess
import os
import signal

app = Flask(__name__)


def get_pids(port: int) -> List[int]:
    if not isinstance(port, int):
        raise ValueError("Port must be an integer")

    pids: List[int] = []

    try:
        result = subprocess.run(
            ['lsof', '-i', f':{port}', '-t'],
            capture_output=True,
            text=True
        )

        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        pid = int(line)
                        pids.append(pid)
                    except ValueError:
                        continue
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    return pids


def free_port(port: int) -> None:
    pids: List[int] = get_pids(port)

    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
        except (ProcessLookupError, PermissionError, OSError):
            try:
                os.kill(pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError, OSError):
                pass


def run(port: int) -> None:
    free_port(port)
    sleep(3)
    app.run(port=port, host='0.0.0.0')


if __name__ == '__main__':
    run(5000)