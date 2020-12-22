import datetime
import functools
import traceback
from collections import (
    deque,
    namedtuple,
)


__all__ = [
    'init',
    'all_logs',
    'error_info',
    'log_event',
    'log_this',
    'codes',
]


def init():
    global _logs
    _logs = deque()


def log_this(ret_val=None):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*a, **k):
            try:
                result = f(*a, **k)
            except Exception as exc:
                log_event(
                    msg='Unhandled Exception. Source: ' + f.__name__,
                    err=error_info(exc)
                )
                return ret_val
            else:
                return result
        return wrapper
    return decorator


def error_info(exc):
    return {
        'type': type(exc).__name__,
        'args': exc.args,
        'tb': traceback.format_exc(),
    }


def log_event(msg, level=0, err=None, **kwargs):
    if err is not None:
        try:
            _ = err['type'] and err['args'] and err['tb']
        except KeyError as exc:
            raise ValueError(
                '`err` arg, if specified, should have these keys: '
                'type, args, tb. You can use `logs.error_info`.'
            )
        else:
            level = codes.ERROR
    _logs.append({
        'level': level,
        'msg': msg,
        'error': err or {},
        'context': kwargs,
        'ts': _now(),
    })


def all_logs():
    return list(_logs)


def _now():
    return datetime.datetime.now().isoformat()


_logs = None
codes = namedtuple('Codes', 'DEBUG INFO ERROR')(-1, 0, 1)
