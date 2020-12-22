import collections
import concurrent.futures
import jsonpath_ng


class JSONData(collections.UserDict):
    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            return None
    
    def get(self, key, default=None):
        try:
            return self.data[key]
        except KeyError:
            return default
    
    def first(self, expr):
        try:
            return jsonpath_ng.parse(expr).find(self.data)[0].value
        except IndexError:
            return None
    
    def all(self, expr):
        return [i.value for i in jsonpath_ng.parse(expr).find(self.data)]


def normalized_dict(d, root_key=None):
    output = []
    try:
        it = d.items()
    except AttributeError:
        it = enumerate(d)
    
    for k, v in it:
        key = '|'.join(filter(None, (root_key, str(k))))
        if isinstance(v, (dict, list)):
            output.extend(normalized_dict(v, key))
        else:
            output.append((key, v))
    
    return output


def parallel_results_mapped(f, keys, *parallel_args, **same_args):
    results = {}
    parallel_args = parallel_args or [keys]
    
    with concurrent.futures.ThreadPoolExecutor(len(parallel_args[0])) as executor:
        futures = {
            executor.submit(f, *args, **same_args): key
            for key, *args in zip(keys, *parallel_args)
        }
    for future in concurrent.futures.as_completed(futures):
        results[futures[future]] = future.result()
    
    return results
