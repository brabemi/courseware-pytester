from flask import Flask, request, jsonify
import tempfile
import json
import subprocess
import sys

prefix = 'cw-tests-'

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def test_code():
    print(request.data)
    content = request.json
    code = content['code']
    code_file_name = content['code_file_name']
    test = content['test']

    with tempfile.TemporaryDirectory(
        prefix=prefix,
        dir='/home/brabemi/Documents/pyladies/courseware-pytester/tmp'
    ) as tmp_folder:

        with open(tmp_folder + '/' + code_file_name, 'w') as code_file:
            print(code, file=code_file)

        with open(tmp_folder + '/test.py', 'w') as test_file:
            print(test, file=test_file)

        try:
            subprocess.run([
                sys.executable,
                '-m',
                'pytest',
                '--json-report',
                '--json-report-file',
                tmp_folder + '/.report.json',
                tmp_folder + '/test.py'
            ], timeout=5)
        except subprocess.TimeoutExpired:
            return jsonify({'collectors': [{'nodeid': 'Timeout', 'outcome': 'failed', 'longrepr': 'Test execution time is too long'}]})

        with open(tmp_folder + '/.report.json') as json_file:
            test_result = json.load(json_file)

    return jsonify(test_result)


app.run(port=5001)
