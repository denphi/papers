
from functools import wraps


# NOTE: -
# DON'T pass args to Celery worker decorated with this, only kwargs.
# As this decorator unpacks tuples return from chained workers.
# Only return a single argument / dict (i.e. the kwargs) from workers.
# This returned argument is passed to chained workers in the args.
# Any worker decorated with this will have its args assigned to kwargs and the args set to [].
def unpack_chained_kwargs(f):
    @wraps(f)
    def _wrapper(*args, **kwargs):
        if len(args) > 0 and type(args[0]) == dict:
            kwargs = args[0]
            args = []
        return f(*args, **kwargs)
    return _wrapper
