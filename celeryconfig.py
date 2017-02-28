
from kombu import Queue

task_default_queue = 'default'
task_queues = (
    Queue('find_regions',    routing_key='find_regions'),
    Queue('debug_regions', routing_key='debug_regions'),
    Queue('mcs_ocr',    routing_key='mcs_ocr'),
    Queue('validate_address', routing_key='validate_address')
)
task_default_exchange = 'tasks'
task_default_exchange_type = 'topic'
task_default_routing_key = 'task.default'
