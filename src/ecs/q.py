#http://www.kr41.net/2016/03-23-dont_inherit_python_builtin_dict_type.html
from collections.abc import Mapping

class Q(Mapping):
    def __init__(self,*args,**kw):
        self._storage = dict(*args, **kw)
        
    def __getitem__(self, key):
        return self._storage[key]
    
    def __iter__(self):
        return iter(self._storage)    # ``ghost`` is invisible
    
    def __len__(self):
        return len(self._storage)

    def get(self, *sel):
        return self._inner_get(self, *sel)
        
    def _inner_get(self, d={}, *sel):
        if d is None:
            return None
        elif len(sel) == 0:
            return d
        elif sel[0] == '*':
            if isinstance(d, list):
                vals = []
                for v in d:
                    val = self._inner_get(v, *sel[1:])
                    if val:
                        vals.append(val)
                if len(vals) > 1:
                    return vals
                elif len(vals) == 1:
                    return vals[0]
                else:
                    return
            elif isinstance(d, dict):
                vals = []
                for (k, v) in d.items():
                    val = self._inner_get(v, *sel[1:])
                    if val:
                        vals.append(val)
                if len(vals) > 1:
                    return vals
                elif len(vals) == 1:
                    return vals[0]
                else:
                    return
        elif isinstance(sel[0], list):
            for s in sel[0]:
                val = self._inner_get(d, *[s, *sel[1:]])
                if val:
                    return val
        elif isinstance(sel[0], int):
            return self._inner_get \
                (d[sel[0]], *sel[1:])
        elif sel[0] in d:
            return self._inner_get \
                (d[sel[0]], *sel[1:])
        else:
            return


