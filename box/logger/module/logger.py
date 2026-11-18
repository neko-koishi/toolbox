import uuid
from datetime import datetime, timezone
import json

def descriptor(description: str):
    # dst is descriptor string
    # basically, descriptor is file descriptor.
    # but extensional.

    # file descriptor
    # descriptor::file://<filepath>

    splited_prefix = description.split('::')
    splited_protocol = ''.join(splited_prefix[1:]).split('://')

    protocol = splited_protocol[0]
    destination = ''.join(splited_protocol[1])

    emitter = None

    match protocol:
        case 'file':
            def emit(data: dict):
                with open(destination, 'a', encoding = 'utf-8') as f:
                    f.write(json.dumps(data) + '\n')
            emitter = emit

        case _:
            pass

    return emitter

def log(
    node_id: str,
    message: dict,
    descriptor: callable = lambda x: print(f'log: {json.dumps(x, indent=4, default=str)}'),
) -> dict:
    if type(message) != dict:
        raise Exception(f'message must be dict. not {type(message)}')

    # at this point but not time
    # -> time as id
    # not the time
    time_id = str(uuid.uuid7())

    # in same node,
    # pointer_id is unique and serial.
    # pointer is a mark of the point.
    pointer_id = f'node::{node_id}:{time_id}'

    # when interaction with another,
    # one send request, 
    # one receive request. 
    # 
    # for above, attach the one communicator
    # at tail.
    # but one to one is rule.
    # not to n is impossible.
    # for everything, absolutely,
    # only one to only one.
    # 
    # for this communicate rule,
    # nodes can save order in whole nodes.
    #  
    # example
    # entity_id = f'node::{node_id}:{action_id}<{node_id}:{pointer_id}'

    log_time = datetime.now(timezone.utc)
   
    data = {
        'pointer_id': pointer_id,
        'log_time': log_time.isoformat(),
        'message': message,
    }

    descriptor(data)

    return log    

