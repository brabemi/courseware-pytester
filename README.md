# courseware-pytester

## Build

Start `lambci/lambda:build-python3.8` container

```
cd build/
python -m venv venv
. venv/bin/activate
python -m pip install -r ../requirements-lambda.txt
cd venv/lib/python3.8/site-packages/
zip -r ../../../../my-deployment-package.zip .
cd ../../../../
cp ../lambda_function.py ./
zip -g my-deployment-package.zip lambda_function.py
```

## Test

```
curl -X POST -k -H 'x-api-key: API_KEY' -H 'Content-Type: application/json' -i 'https://1uldyze5u0.execute-api.eu-west-1.amazonaws.com/default/test' --data '{
"code": "def inc(x):\n    return x + 1",
"test": "from test import inc\nimport time\ndef test_answer():\n    time.sleep(4)\n    assert inc(3) == 5",
"code_file_name": "test.py"
}'
```
