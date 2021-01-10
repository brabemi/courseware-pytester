import tempfile
import json
import subprocess
import sys


prefix = 'cw-tests-'
test_file_name = prefix + 'test.py'


def lambda_handler(event, context):
    print(json.loads(event['body']))
    content = json.loads(event['body'])
    code = content['code']
    code_file_name = content['code_file_name']
    test = content['test']

    with tempfile.TemporaryDirectory(
        prefix=prefix,
        dir='/tmp'
    ) as tmp_folder:

        with open(tmp_folder + '/' + code_file_name, 'w') as code_file:
            print(code, file=code_file)

        with open(tmp_folder + '/' + test_file_name, 'w') as test_file:
            print(test, file=test_file)

        try:
            subprocess.run([
                sys.executable,
                '-m',
                'pytest',
                '--json-report',
                '--json-report-file',
                tmp_folder + '/.report.json',
                tmp_folder + '/' + test_file_name
            ], timeout=10)
        except subprocess.TimeoutExpired:
            return {
                'statusCode': 200,
                'body': json.dumps(
                    {'collectors': [
                        {
                            'nodeid': 'Timeout',
                            'outcome': 'failed',
                            'longrepr': 'Test execution time is too long'
                        }
                    ]
                    }
                )
            }

        with open(tmp_folder + '/.report.json') as json_file:
            test_result = json.load(json_file)

    return {
        'statusCode': 200,
        'body': json.dumps(test_result)
    }
