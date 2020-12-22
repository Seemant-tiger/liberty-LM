import re

import nameparser
import usaddress


def cleaned_name(name):
    pattern = re.compile(
        r'''
            [\(\[]  # opening ( or [
            .*?     # part inside () or []
            [\)\]]  # closing ) or ]
        ''',
        re.VERBOSE,
    )
    name = pattern.sub('', name)
    name = cleaned_string(name)
    name = name.lower()
    name = ' '.join(filter(lambda x: x != 'dba', name.split()))
    return name


def cleaned_string(s):
    s = s.strip().lower()
    s = s.replace(' & ', ' and ')
    s = ' '.join(re.findall(r'[a-zA-Z0-9]+', s))
    s = ' '.join(s.split())
    return s.strip()


def as_unicode(obj, encoding='utf-8'):
    if not isinstance(obj, str):
        return obj.decode(encoding, errors='ignore')
    return obj

def ct(tf):
    """Convert 24 hours time-format 
       into 12 hours """
    
    t = time.strptime(tf, "%H%M")
    return time.strftime("%I:%M %p", t)


def to_unicode(obj, encoding='utf-8'):
    '''
    Function to decode any string type to unicode
    Input:
        obj:obj
    Output:
        return:str
    '''
    if not isinstance(obj, str):
        return obj.decode(encoding, errors='ignore')
    return obj

def extract_city_and_state(acc_address):
    '''
    Function to extract city and state name from address Will be used only if
    geocode results are empty

    Input:
        acc_address:str
    Output:
        return:str
    '''
    _a = None
    try:
        _a = usaddress.tag(acc_address)[0]
    except Exception as e:
        logs.log_event(
            msg='shared.cu.extract_city_and_state',
            err=logs.error_info(e),
        )
        # error_log.error(e)
    if not _a:
        return ""
    comp = _a.get('PlaceName', '') + " " + _a.get('StateName', '')
    comp = " ".join(comp.split()).strip()
    return comp
