
# Validate Address

## Setup

Add Google API Key to variable ```GOOGLE_API_KEY``` in file ```AddressCompare.py```.

## Run

~~~
celery -A validate_address worker --loglevel=info -Q validate_address -n validate_address_01@%h
~~~
