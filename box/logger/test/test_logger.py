from module import logger
from module import compose
import json

def test_log():
    print()
    res = logger.log('node-www', {'m': 'msg-aaa'})

    expected = {
        "pointer_id": "node::node-www:01a1eec7-1842-7017-aac5-bcad1f3f431f",
        "log_time": "2026-11-18T13:09:47.714766+00:00",
        "message": {
            "m": "msg-aaa"
        }
    }

    # assert res == expected

def test_descriptor():
    print()

    descriptor = logger.descriptor('descriptor::file://../../../test/a.jsonl')
    res = logger.log('node-www', {'m': 'msg-aaa'}, descriptor = descriptor)

    expected = {
        "pointer_id": "node::node-www:01a1eec7-1842-7017-aac5-bcad1f3f431f",
        "log_time": "2026-11-18T13:09:47.714766+00:00",
        "message": {
            "m": "msg-aaa"
        }
    }

    # assert res == expected

def test_compose_match():
    source = {
        'k0': 0,
        'k1': {
            'k1-1': 11,
            'k1-2': 12,
        },
    }
    pattern = {
        'k0': 0,
        'k1': {
            'k1-1': 11,
            'k1-2': lambda x: True,
        },
    }

    res = compose.compose_match(
        source,
        pattern
    )
    print(f'res is {res}')


    assert res == {
        'k0': True,
        'k1': {
            'k1-1': True,
            'k1-2': True
        }
    }

def test_geometry_match():
    source = {
        'k0': 0,
        'k1': {
            'k1-1': 11,
            'k1-2': 12,
        },
    }
    pattern = {
        'k0': 0,
        'k1': {
            'k1-1': 11,
            'k1-2': lambda x: True,
        },
    }

    res = compose.geometry_match(
        source,
        pattern
    )
    print(f'res is {res}')

    assert res

def test_leaf_collect():
    source = {
        'k0': 0,
        'k1': {
            'k1-1': 11,
            'k1-2': 12,
        },
        'k2': 2,
    }
    

    res = compose.leaf_collect(
        source,
    )
    print(f'res is \n{json.dumps(res, indent=4)}')

    assert res == {
        "k0": 0,
        "k1/k1-1": 11,
        "k1/k1-2": 12,
        "k2": 2
    }

    res = compose.leaf_collect(
        source,
        delimiter = '::'
    )
    print(f'res is \n{json.dumps(res, indent=4)}')

    assert res ==  {
        "k0": 0,
        "k1::k1-1": 11,
        "k1::k1-2": 12,
        "k2": 2
    }


def test_leaf_apply():
    source = {
        'k0': 0,
        'k1': {
            'k1-1': 11,
            'k1-2': 12,
        },
        'k2': 2,
    }

    res = compose.leaf_apply(
        source,
        lambda x: x >= 10
    )
    print(f'res is \n{json.dumps(res, indent=4)}')

    assert res == {
        "k0": False,
        "k1": {
            "k1-1": True,
            "k1-2": True
        },
        "k2": False
    }

    
