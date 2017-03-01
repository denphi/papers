
# papers

File sharing service built using Flask, Celery, and RethinkDB

## References

- <https://www.pluralsight.com/guides/python/build-a-simple-file-storage-service-using-vuejs-flask-and-rethinkdb>
- <https://github.com/afropolymath/papers>
- <https://github.com/hueyl77/flask-storage>

## Setup

### Use a virtual environment

e.g. <http://virtualenvwrapper.readthedocs.io/en/latest/install.html>

> Mac OS X

> Create and activate

~~~
virtualenv -p python3.6 venv
~~~

~~~
source venv/bin/activate
~~~

> deactivate

~~~
deactivate
~~~

### Install requirements

~~~
pip3.6 install -r requirements.txt
~~~

### Install RethinkDB

<https://www.rethinkdb.com/docs/install/>

> Mac OS X

~~~
brew update && brew install rethinkdb
~~~

## Configuration

Rename ```config.py.example``` to ```config.py``` and edit as needed.

## Run

### Set RethinkDB

~~~
rethinkdb
~~~

<http://localhost:8080/>

### Create Database

~~~
python3.6 run.py migrate
~~~

### Run Application

~~~
python3.6 run.py runserver
~~~

### Run Application, on specific port and host 0.0.0.0, to allow network access

~~~
python3.6 run.py runserver --host=0.0.0.0 --port=8081
~~~

### Run Argument

|Argument|Description|
|---|---|
|```migrate```|Creates Database|
|```shell```|Runs a Python shell inside Flask application context.|
|```drop_db```|Drops Database|
|```runserver```|Runs the Flask development server i.e. app.run()|

## API

### API Methods

|Method|URI|Description|Note|
|---|---|---|---|
|```GET```|```/api/v1/users```|This endpoint list users||
|```POST```|```/api/v1/auth/login```|This endpoint login users||
|```POST```|```/api/v1/auth/register```|This endpoint register users||
|```GET```|```/api/v1/files```|This endpoint lists user files|```user_id``` is in JWT.|
|```GET```|```/api/v1/files/<file_id>```|This endpoint gets a single file via ```file_id```|```user_id``` is in JWT.|
|```PUT```|```/api/v1/files/<file_id>```|This endpoint will be used to edit a single file with id ```file_id```|```user_id``` is in JWT.|
|```DELETE```|```/api/v1/files/<file_id>```|This endpoint will be used to delete a single file with id ```file_id```|```user_id``` is in JWT.|
|```POST```|```/api/v1/upload```|This endpoint uploads Base64 encoded images|```user_id``` is in JWT.|
|```GET```|```/api/v1/download```|This endpoint downloads an image|```user_id``` is in JWT.|

### List Users

~~~
curl -X GET http://127.0.0.1:5000/api/v1/users
~~~

> Results, no users

~~~
[]
~~~

> Results

~~~
[
    {
        "date_created": "Wed, 22 Feb 2017 23:59:14 -0000",
        "date_modified": "Wed, 22 Feb 2017 23:59:14 -0000",
        "email": "temp@test.com",
        "fullname": "temp"
    }
]
~~~

### Create User

~~~
curl -X POST http://127.0.0.1:5000/api/v1/auth/register -d "fullname=temp" -d "email=temp@test.com" -d "password=temp123" -d "password_conf=temp123"
~~~

> Results

~~~
{
    "message": "Successfully created your account."
}
~~~

### Create User, with address

~~~
curl -X POST http://127.0.0.1:5000/api/v1/auth/register -d "fullname=temp" -d "email=jon.smith@test.com" -d "password=temp123" -d "password_conf=temp123" -d "street_number=128" -d "route=" -d "locality=GLH" -d "postal_town=London" -d "administrative_area_level_2=Camden" -d "administrative_area_level_1=England" -d "country=United Kingdom" -d "postal_code=NW3 3JJ"
~~~

> Results

~~~
{
    "message": "Successfully created your account."
}
~~~

### Login

> Form

~~~
curl -X POST http://127.0.0.1:5000/api/v1/auth/login -d "email=temp@test.com" -d "password=temp123"
~~~

> Json

~~~
curl -X POST -H "Content-Type: application/json" -d '{"email": "temp@test.com", "password": "temp123"}' http://127.0.0.1:5000/api/v1/auth/login
~~~

> Results

~~~
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNTA5NzFiLWUxMGQtNGY1ZS05OTIyLWZlODA1OWZiNjJiZCJ9.svXGbFs7N6lfxs8AgYtqMJCiKU85naUvxTn-pekX_SM"
}
~~~

### Create Folder

~~~
curl -X POST -H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNTA5NzFiLWUxMGQtNGY1ZS05OTIyLWZlODA1OWZiNjJiZCJ9.svXGbFs7N6lfxs8AgYtqMJCiKU85naUvxTn-pekX_SM" -H "Content-Type: application/json" http://127.0.0.1:5000/api/v1/files -d '{"name": "temp_folder", "is_folder": "true"}'
~~~

> Results

~~~
{
    "creator": "3b50971b-e10d-4f5e-9922-fe8059fb62bd",
    "date_created": "Wed, 22 Feb 2017 23:59:45 -0000",
    "date_modified": "Wed, 22 Feb 2017 23:59:45 -0000",
    "id": "a1c53f56-3b67-4af8-8554-041f58410cb0",
    "is_folder": true,
    "name": "temp_folder",
    "objects": [],
    "parent_id": "0",
    "size": 0,
    "uri": null
}
~~~

### Create sub folder

~~~
curl -X POST -H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNTA5NzFiLWUxMGQtNGY1ZS05OTIyLWZlODA1OWZiNjJiZCJ9.svXGbFs7N6lfxs8AgYtqMJCiKU85naUvxTn-pekX_SM" -H "Content-Type: application/json" http://127.0.0.1:5000/api/v1/files -d '{"name": "temp_sub_folder", "parent_id": "a1c53f56-3b67-4af8-8554-041f58410cb0", "is_folder": "true"}'
~~~

> Results

~~~
{
    "creator": "3b50971b-e10d-4f5e-9922-fe8059fb62bd",
    "date_created": "Thu, 23 Feb 2017 00:00:15 -0000",
    "date_modified": "Thu, 23 Feb 2017 00:00:15 -0000",
    "id": "ddca5489-c77c-4b70-85a9-c58692d317a7",
    "is_folder": true,
    "name": "temp_sub_folder",
    "objects": [],
    "parent_id": "a1c53f56-3b67-4af8-8554-041f58410cb0",
    "size": 0,
    "uri": null
}
~~~

### Upload file

~~~
curl -X POST -H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNTA5NzFiLWUxMGQtNGY1ZS05OTIyLWZlODA1OWZiNjJiZCJ9.svXGbFs7N6lfxs8AgYtqMJCiKU85naUvxTn-pekX_SM" http://127.0.0.1:5000/api/v1/files -F "file=@_TESTDATA/garden-2040714_640.jpg"
~~~

> Results

~~~
{
    "creator": "3b50971b-e10d-4f5e-9922-fe8059fb62bd",
    "date_created": "Thu, 23 Feb 2017 00:02:19 -0000",
    "date_modified": "Thu, 23 Feb 2017 00:02:19 -0000",
    "id": "06fd734a-e5bb-414f-9e11-22306a2a2897",
    "is_folder": false,
    "name": "garden-2040714_640.jpg",
    "objects": [],
    "parent_id": "0",
    "size": 102591,
    "uri": "upload/3b50971b-e10d-4f5e-9922-fe8059fb62bd/garden-2040714_640.jpg"
}
~~~

### Upload file, Base64

~~~
curl -X POST -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ijk4YWM1ZDJlLTNlZmQtNGE5MS04Yjg2LWFkN2I0ZjJjYzBjZiJ9.zJuFG_pHWi3IrqlqowkoZbIsUfyWENzSHD1zk-b3kvQ" -H "Content-Type: application/json" http://127.0.0.1:5000/api/v1/upload -d '{"site_name": "Test Image", "url": "www.test.com", "image_data": "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAICAYAAADA+m62AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAB1WlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS40LjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyI+CiAgICAgICAgIDx0aWZmOkNvbXByZXNzaW9uPjE8L3RpZmY6Q29tcHJlc3Npb24+CiAgICAgICAgIDx0aWZmOk9yaWVudGF0aW9uPjE8L3RpZmY6T3JpZW50YXRpb24+CiAgICAgICAgIDx0aWZmOlBob3RvbWV0cmljSW50ZXJwcmV0YXRpb24+MjwvdGlmZjpQaG90b21ldHJpY0ludGVycHJldGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KAtiABQAAAS1JREFUGBkdjj9LAnEAhp/OUy/PyPJPmJynpN6hpoLmIG051xC0NvQFWvs6rW1BGDQ0VhBICCkJhZmZQeWSmaW/LteX533el2J5UwTMvNjbPxC3zQdxeV0VG1s7wuaPiPL2rjg8OhZPzz0hr+VzvPX71O+anJyd8zUY0On2CC0FKBUKFDI5FuY9yAULrNUbtFptKpVTBDAY/WCYJvnsKuFQEEWRkZJmAl3XGQ4+qV5d0KjdoLrdpLIZYnEdVbUgCSS/z4umaTjtdj5e27y/dKaz6VQSn9dj+QVCCCTVqaBb4HIwaIXgdNgxIhrJWJQ5VZ1m/7DssNlYCYfIZtJ0H+9Z9Hgw4jG0gB9ZsiEmEybWcVl1KRhRjfVSkeHom1nFRcIwpwW7LDEe/1rWGf4AWFZd7C8FwSoAAAAASUVORK5CYII="}'
~~~

> data:image/png;base64, prefix will be removed

~~~
curl -X POST -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ijk4YWM1ZDJlLTNlZmQtNGE5MS04Yjg2LWFkN2I0ZjJjYzBjZiJ9.zJuFG_pHWi3IrqlqowkoZbIsUfyWENzSHD1zk-b3kvQ" -H "Content-Type: application/json" http://127.0.0.1:5000/api/v1/upload -d '{"name": "Test Image", "url": "www.test.com", "image_data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAICAYAAADA+m62AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAB1WlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS40LjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyI+CiAgICAgICAgIDx0aWZmOkNvbXByZXNzaW9uPjE8L3RpZmY6Q29tcHJlc3Npb24+CiAgICAgICAgIDx0aWZmOk9yaWVudGF0aW9uPjE8L3RpZmY6T3JpZW50YXRpb24+CiAgICAgICAgIDx0aWZmOlBob3RvbWV0cmljSW50ZXJwcmV0YXRpb24+MjwvdGlmZjpQaG90b21ldHJpY0ludGVycHJldGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KAtiABQAAAS1JREFUGBkdjj9LAnEAhp/OUy/PyPJPmJynpN6hpoLmIG051xC0NvQFWvs6rW1BGDQ0VhBICCkJhZmZQeWSmaW/LteX533el2J5UwTMvNjbPxC3zQdxeV0VG1s7wuaPiPL2rjg8OhZPzz0hr+VzvPX71O+anJyd8zUY0On2CC0FKBUKFDI5FuY9yAULrNUbtFptKpVTBDAY/WCYJvnsKuFQEEWRkZJmAl3XGQ4+qV5d0KjdoLrdpLIZYnEdVbUgCSS/z4umaTjtdj5e27y/dKaz6VQSn9dj+QVCCCTVqaBb4HIwaIXgdNgxIhrJWJQ5VZ1m/7DssNlYCYfIZtJ0H+9Z9Hgw4jG0gB9ZsiEmEybWcVl1KRhRjfVSkeHom1nFRcIwpwW7LDEe/1rWGf4AWFZd7C8FwSoAAAAASUVORK5CYII="}'
~~~

### List files

~~~
curl -X GET -H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNTA5NzFiLWUxMGQtNGY1ZS05OTIyLWZlODA1OWZiNjJiZCJ9.svXGbFs7N6lfxs8AgYtqMJCiKU85naUvxTn-pekX_SM" -H "Cache-Control: no-cache" http://127.0.0.1:5000/api/v1/files
~~~

> JWT prefix will be removed

~~~
curl -X GET -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNTA5NzFiLWUxMGQtNGY1ZS05OTIyLWZlODA1OWZiNjJiZCJ9.svXGbFs7N6lfxs8AgYtqMJCiKU85naUvxTn-pekX_SM" -H "Cache-Control: no-cache" http://127.0.0.1:5000/api/v1/files
~~~

> Results

~~~
[
    {
        "creator": "3b50971b-e10d-4f5e-9922-fe8059fb62bd",
        "date_created": "Thu, 23 Feb 2017 00:00:15 -0000",
        "date_modified": "Thu, 23 Feb 2017 00:00:15 -0000",
        "id": "ddca5489-c77c-4b70-85a9-c58692d317a7",
        "is_folder": true,
        "name": "temp_sub_folder",
        "parent_id": "a1c53f56-3b67-4af8-8554-041f58410cb0",
        "size": 0,
        "uri": null
    },
    {
        "creator": "3b50971b-e10d-4f5e-9922-fe8059fb62bd",
        "date_created": "Thu, 23 Feb 2017 00:02:19 -0000",
        "date_modified": "Thu, 23 Feb 2017 00:02:19 -0000",
        "id": "06fd734a-e5bb-414f-9e11-22306a2a2897",
        "is_folder": false,
        "name": "garden-2040714_640.jpg",
        "parent_id": "0",
        "size": 102591,
        "uri": "upload/3b50971b-e10d-4f5e-9922-fe8059fb62bd/garden-2040714_640.jpg"
    },
    {
        "creator": "3b50971b-e10d-4f5e-9922-fe8059fb62bd",
        "date_created": "Wed, 22 Feb 2017 23:59:45 -0000",
        "date_modified": "Wed, 22 Feb 2017 23:59:45 -0000",
        "id": "a1c53f56-3b67-4af8-8554-041f58410cb0",
        "is_folder": true,
        "name": "temp_folder",
        "parent_id": "0",
        "size": 0,
        "uri": null
    }
]
~~~

### Get File

~~~
curl -X GET -H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNTA5NzFiLWUxMGQtNGY1ZS05OTIyLWZlODA1OWZiNjJiZCJ9.svXGbFs7N6lfxs8AgYtqMJCiKU85naUvxTn-pekX_SM" -H "Cache-Control: no-cache" http://127.0.0.1:5000/api/v1/files/06fd734a-e5bb-414f-9e11-22306a2a2897
~~~

> Results

~~~
{
    "creator": "3b50971b-e10d-4f5e-9922-fe8059fb62bd",
    "date_created": "Thu, 23 Feb 2017 00:02:19 -0000",
    "date_modified": "Thu, 23 Feb 2017 00:02:19 -0000",
    "id": "06fd734a-e5bb-414f-9e11-22306a2a2897",
    "is_folder": false,
    "name": "garden-2040714_640.jpg",
    "objects": [],
    "parent_id": "0",
    "size": 102591,
    "uri": "upload/3b50971b-e10d-4f5e-9922-fe8059fb62bd/garden-2040714_640.jpg"
}
~~~

### Get File, download

~~~
curl -X GET -H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNTA5NzFiLWUxMGQtNGY1ZS05OTIyLWZlODA1OWZiNjJiZCJ9.svXGbFs7N6lfxs8AgYtqMJCiKU85naUvxTn-pekX_SM" -H "Cache-Control: no-cache" "http://127.0.0.1:5000/api/v1/files/4cacd8dd-0cf8-44e5-ab0e-9610bedb3d9d?download=true"
~~~

### Put File

~~~
curl -X PUT -H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNTA5NzFiLWUxMGQtNGY1ZS05OTIyLWZlODA1OWZiNjJiZCJ9.svXGbFs7N6lfxs8AgYtqMJCiKU85naUvxTn-pekX_SM" http://127.0.0.1:5000/api/v1/files/06fd734a-e5bb-414f-9e11-22306a2a2897 -F "file=@_TESTDATA/tulips-2048324_640.jpg"
~~~

> TODO: The file should be replaced on disk

> Results

~~~
{
    "creator": "3b50971b-e10d-4f5e-9922-fe8059fb62bd",
    "date_created": "Thu, 23 Feb 2017 00:02:19 -0000",
    "date_modified": "Thu, 23 Feb 2017 00:02:19 -0000",
    "id": "06fd734a-e5bb-414f-9e11-22306a2a2897",
    "is_folder": false,
    "name": "garden-2040714_640.jpg",
    "objects": [],
    "parent_id": "0",
    "size": 102591,
    "uri": "upload/3b50971b-e10d-4f5e-9922-fe8059fb62bd/garden-2040714_640.jpg"
}
~~~

### Delete File

~~~
curl -I -X DELETE -H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNTA5NzFiLWUxMGQtNGY1ZS05OTIyLWZlODA1OWZiNjJiZCJ9.svXGbFs7N6lfxs8AgYtqMJCiKU85naUvxTn-pekX_SM" http://127.0.0.1:5000/api/v1/files/06fd734a-e5bb-414f-9e11-22306a2a2897
~~~

> Results

~~~
HTTP/1.0 204 NO CONTENT
Content-Type: application/json
Content-Length: 0
Server: Werkzeug/0.11.15 Python/2.7.13
Date: Thu, 23 Feb 2017 00:20:37 GMT
~~~

### Delete File, ```hard_delete```

Deletes file from disk

~~~
curl -I -X DELETE -H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjNiNTA5NzFiLWUxMGQtNGY1ZS05OTIyLWZlODA1OWZiNjJiZCJ9.svXGbFs7N6lfxs8AgYtqMJCiKU85naUvxTn-pekX_SM" "http://127.0.0.1:5000/api/v1/files/06fd734a-e5bb-414f-9e11-22306a2a2897?hard_delete=true"
~~~

> Results

~~~
HTTP/1.0 204 NO CONTENT
Content-Type: application/json
Content-Length: 0
Server: Werkzeug/0.11.15 Python/2.7.13
Date: Thu, 23 Feb 2017 00:25:03 GMT
~~~

## Scripts

~~~
cd scripts

./upload_base64_file.py temp@test.com temp123 ../_TESTDATA/bgbill12/bgbill12.png

./upload_base64_file.py temp@test.com temp123 ../_TESTDATA/ocr_test_images/64c98c75c795823a1f.png
~~~

## NOTES: -

- Test pictures (```./_TESTDATA/*.jpg```) are from <https://pixabay.com/>
- Test OCR image (```./_TESTDATA/ocr_test_images/64c98c75c795823a1f.png```) is from <http://eng.wealthfront.com/2015/07/02/testing-with-optical-character-recognition-ocr/>
