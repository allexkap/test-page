import os
import subprocess

from flask import Flask, render_template_string, request

SECRET_KEY = os.environ['KEY']

HTML = """
<!DOCTYPE html>
<html>
  <head>
    <title>Command Runner</title>
  </head>
  <body>
    <h1>Run a shell command</h1>
    <form method="post">
      <label>Key: <input type="text" name="key" value="{{ key }}" /></label><br><br>
      <label>Command: <input type="text" name="command" style="width: 400px;" value="{{ command }}" /></label><br><br>
      <button type="submit">Run</button>
    </form>
    {% if error %}
      <p style="color:red;"><strong>{{ error }}</strong></p>
    {% endif %}
    {% if output %}
      <h2>Output:</h2>
      <pre>{{ output }}</pre>
    {% endif %}
  </body>
</html>
"""

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    error = ''
    key = ''
    command = ''
    if request.method == 'POST':
        key = request.form.get('key', '')
        command = request.form.get('command', '')

        if key != SECRET_KEY:
            error = 'Invalid access key.'
        else:
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                )
                output = result.stdout
            except subprocess.CalledProcessError as e:
                output = f'Error:\n{e.output}'

    return render_template_string(
        HTML, output=output, error=error, key=key, command=command
    )


if __name__ == '__main__':
    app.run()
