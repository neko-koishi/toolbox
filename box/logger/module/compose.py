def compose_match(
    source: dict,
    pattern: dict
):
    print()
    print(f'source : {source}')
    print(f'pattern: {pattern}')

    r = _recurse_cmatch(source, pattern)

    return r

def geometry_match(
    source: dict,
    pattern: dict
):
    source_applied = leaf_apply(
        source,
        lambda x: True
    )
    pattern_applied = leaf_apply(
        pattern,
        lambda x: True
    )
    res = source_applied == pattern_applied
    print(f'source_applied: {source_applied}')
    return res


def leaf_apply(
    source: dict,
    apply_fn,
):
    cur_nodes = {}
    for k, v in source.items():
        if type(v) not in [list, dict]:
            cur_nodes[k] = apply_fn(v)
            continue
            
        next_source = source.get(k)

        down_nodes = leaf_apply(
            next_source,
            apply_fn
        )

        cur_nodes[k] = down_nodes

    return cur_nodes

def leaf_collect(
    source: dict,
    delimiter = '/'
):
    collection = {
        'cur_pathkeys': [],
        'kvs': {}
    }
    _leaf_collect_recurse(
        source,
        collection = collection,
        delimiter = delimiter
    )
    leaves = collection['kvs']
    return leaves



def _recurse_cmatch(
    source: dict,
    pattern: dict,
    default_fn = None
):
    cur_nodes = {}
    for k, v in source.items():
        p_value = pattern[k]
        print(f'k      : {k}')
        print(f'v      : {v}')
        print(f'p_value: {p_value}')

        if type(v) not in [list, dict]:
            assert_res = None
            if default_fn is None:
                assert_res = _match_assert(v, p_value)
            else:
                assert_res = default_fn(v)

            cur_nodes[k] = assert_res

            continue
            
        next_source = source.get(k)
        next_pattern = pattern.get(k)

        down_nodes = _recurse_cmatch(
            next_source,
            next_pattern
        )

        cur_nodes[k] = down_nodes

    return cur_nodes

def _leaf_collect_recurse(
    source: dict,
    collection = {
        'cur_pathkeys': [],
        'kvs': {}
    },
    delimiter = '/'
):
    cur_nodes = {}
    for k, v in source.items():
        collection['cur_pathkeys'].append(k)
        if type(v) not in [list, dict]:
            collection['kvs'].update({
                delimiter.join(collection['cur_pathkeys']): v
            })
            collection['cur_pathkeys'].pop()
            continue
            
        next_source = source.get(k)

        _leaf_collect_recurse(
            next_source,
            collection = collection,
            delimiter = delimiter

        )
        collection['cur_pathkeys'].pop()

    return collection

def _match_assert(v, p_value):
    res = None
    if callable(p_value):
        res = p_value(v)
    else:
        res = v == p_value

    print(res)

    return res


