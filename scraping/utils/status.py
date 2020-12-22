import functools
import time

from . import logs


__all__ = [
    'status',
    'time_this',
    'update_answers',
    'update_inputs',
    'update_scraping',
]

_status_keys = (
    'uid',
    'input',
    'scraping',
    'geocodio',
    'times',
    's3',
    'status',
)
status = {k: {} for k in _status_keys}
status['scraping']['particular'] = {}

def time_this(key):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*a, **k):
            start = time.time()
            _result = f(*a, **k)
            end = time.time()
            status['times'][key] = {
                'start': start,
                'end': end,
                'time': round(end - start, 3),
            }
            return _result
        return wrapper
    return decorator


def update_inputs(uid, record):
    status.update({
        'uid': uid,
        'input': dict(zip(
            ('uid', 'name', 'addr-1',
             'addr-2', 'city', 'state', 'zip', 'country', 'addr-geocoded'),
            record.base_columns.values(),
        )),
    })


def update_scraping(data, sources):
    _hits = len([v for v in data.values() if v.get('processed_name')])
    
    _logs = logs.all_logs()
    _errors = [i for i in _logs if i['level'] == 1]
    
    particular = status['scraping']['particular']
    for source, info in particular.items():
        info['errors'] = len([
            i for i in _errors
            if i.get('context', {}).get('source') == source
        ])
    
    status['scraping'] = {
        'sources': sources,
        'sources-hits': _hits,
        'sources-empty': len(sources) - _hits,
        'particular': particular,
    }


