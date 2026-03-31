from flask import Flask, request
import subprocess
import shlex
from typing import List

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str:
    args: List[str] = request.args.getlist('arg')

    command = ['ps']
    for arg in args:
        safe_arg = shlex.quote(arg)
        command.append(safe_arg)

    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout if result.stdout else result.stderr

    return f"<pre>{output}</pre>"


if __name__ == "__main__":
    app.run(debug=True)

