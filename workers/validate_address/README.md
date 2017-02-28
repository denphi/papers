
# Validate Address

## Run

~~~
celery -A validate_address worker --loglevel=info -Q validate_address -n validate_address_01@%h
~~~
