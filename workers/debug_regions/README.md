
# Debug Regions

## Run

~~~
celery -A debug_regions worker --loglevel=info -Q debug_regions -n debug_regions_01@%h
~~~
