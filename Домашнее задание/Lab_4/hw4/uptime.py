from flask import Flask
import subprocess
app = Flask(__name__)

@app.route("/uptime", methods=['GET'])
def uptime() -> str:
    result = subprocess.run(['uptime', '-p'], capture_output=True, text=True)
    uptime_str = result.stdout.strip()
    uptime_str = uptime_str.replace('up ', '', 1)
    return f"Current uptime is {uptime_str}"

if __name__ == '__main__':
    app.run(debug=True)
