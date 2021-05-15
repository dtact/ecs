import json

import dateutil.parser
from datetime import datetime

class Int(int):
    def __new__(cls, val):
        if val is None:
            return
        
        return super().__new__(cls, val) 

class String(str):
    def __new__(cls, val):
        if val is None:
            return
        
        return super().__new__(cls, val) 

class Bytes(Int):
    pass

class Timestamp(str):
    def __new__(cls, val):   
        if val is None:
            return
        
        if isinstance(val, str):
            # normalize
            val = dateutil.parser.isoparse(val).isoformat('T').replace('+00:00', 'Z')
        elif isinstance(val, float) or isinstance(val, number):
            # normalize
            val = datetime.fromtimestamp(val).isoformat('T').replace('+00:00', 'Z')
        else:
            val = val.isoformat('T').replace('+00:00', 'Z')

        return super().__new__(cls, val)

class Provider(String):
    pass        

class Action(String):
    pass

class Message(String):
    pass

class Code(String):
    pass

class Id(String):
    pass

class Name(String):
    pass

class Dataset(String):
    pass

class Outcome(String):
    pass
        
class Kind(String):
    pass

class Type(list):
    def __init__(self, val):
        if isinstance(val, list):
            super().__init__(val)
        elif isinstance(val, str):
            super().__init__([val])
        else:
            raise Exception("Expected list for type, got: ", val)

class Group(list):
    def __init__(self, val):
        if isinstance(val, list):
            super().__init__(val)
        elif isinstance(val, str):
            super().__init__([val])
        else:
            raise Exception("Expected list for group, got: ", val)
            
class Category(list):
    def __init__(self, val):
        if isinstance(val, list):
            super().__init__(val)
        elif isinstance(val, str):
            super().__init__([val])
        else:
            raise Exception("Expected list for category, got: ", val)
        
class Port(Int):
    pass
    
class Packets(Int):
    pass

class MAC(String):
    pass

class Address(String):
    pass
        
class Base(dict):
    def __init__(self, *args):
        d = {}

        if isinstance(self._allowed, dict):
            for arg in args:
                if arg is None:
                    continue
                elif arg == {}:
                    continue
                  
                allowed = False
                for (k,t) in self._allowed.items():
                    if isinstance(arg, t):
                        allowed = True
                        
                        d[k] = arg
                        
                if not allowed:
                    raise Exception(f"Type {type(arg)} not supported for {type(self)}, allowed are: {self._allowed}")
                    
            super().__init__(d)
        else:
            for arg in args:
                if arg is None:
                    continue

                allowed = False
                for t in self._allowed:
                    if isinstance(arg, t):
                        d = {
                            **d,
                            **arg,
                        }

                        allowed = True

                if not allowed:
                    raise Exception(f"Type {type(arg)} not supported for {self._field}, allowed are: {self._allowed}")

            # no empty objects
            if (d == {}):
                return

            super().__init__({
                self._field: d,
            })

class Original(String):
    pass

class User(Base):
    _allowed = { 'name' : Name, 'id': Id }

class Target(User):
    pass

User._allowed.update({'target': Target})
 
class Error(Base):
    _allowed = {'code': Code, 'id': Id, 'message': Message}
    
class Event(Base):
    _allowed = { 'original': Original, 'provider': Provider, 'action': Action, 'id': Id, 'category': Category, 'type': Type, 
                'dataset': Dataset, 'kind': Kind, 'outcome': Outcome, 'group': Group}
    
    def __init__(self, name, *args, type=None):
        super().__init__(name, *args)

        if self.get('original'):
            self['original'] = json.dumps(self.get('original'))

class Source(Base):
    _allowed = {'address': Address, 'bytes': Bytes, 'packets': Packets, 'port': Port, 'user': User}
    
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        
        address = self.get('address')
        if address:
            try:
                import ipaddress
                self['ip'] = str(ipaddress.ip_address(address))
            except ValueError as exc:
                self['domain'] = address

class Destination(Base):
    _allowed = {'address': Address, 'bytes': Bytes, 'packets': Packets, 'port': Port, 'user': User}

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        
        address = self.get('address')
        if address:
            try:
                import ipaddress
                self['ip'] = str(ipaddress.ip_address(address))
            except ValueError as exc:
                self['domain'] = address

class Client(Base):
    _allowed = {'address': Address, 'bytes': Bytes, 'packets': Packets, 'port': Port, 'user': User}

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        
        address = self.get('address')
        if address:
            try:
                import ipaddress
                self['ip'] = str(ipaddress.ip_address(address))
            except ValueError as exc:
                self['domain'] = address

class Server(Base):
    _allowed = {'address': Address, 'bytes': Bytes, 'packets': Packets, 'port': Port, 'user': User}

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        
        address = self.get('address')
        if address:
            try:
                import ipaddress
                self['ip'] = str(ipaddress.ip_address(address))
            except ValueError as exc:
                self['domain'] = address

class Account(Base):
    _allowed = {'id': Id, 'name': Name}

class Region(String):
    pass

class Useragent(Base):
    _allowed = {'original': Original}

class IP(list):
    def __init__(self, *vals):
        if not len(vals):
            return
        super().__init__([val for val in vals if val])

class Hash(list):
    def __init__(self, *vals):
        if not len(vals):
            return
        super().__init__([val for val in vals if val])
        
class Hosts(list):
    def __init__(self, *vals):
        if not len(vals):
            return
        super().__init__([val for val in vals if val])

class Users(list):
    def __init__(self, *vals):
        if not len(vals):
            return
        super().__init__([val for val in vals if val])
        
class Related(Base):
    _allowed = { 'ip': IP, 'hash': Hash, 'hosts': Hosts, 'users': Users }
    
class Cloud(Base):
    _allowed = {'account': Account, 'region': Region}

class Custom(dict):
    def __init__(self, name, *args, type=None):
        d = {}
        
        for arg in args:
            if arg is None:
                continue
                
            if type == str:
                d = str(arg)
            elif type == bool:
                d = bool(arg)
            elif type == float:
                d = float(arg)
            elif type == int:
                d = int(arg)
            elif isinstance(arg, Custom):
                d = {
                    **d,
                    **arg,
                }
            else:
                print(f"Unsupported type {name} {arg} {type(arg)}")
                
        if d == {}:
            return

        super().__init__({
            name: d
        })
    
        
class ECS(Base):
    _allowed = {'source': Source, 'destination': Destination, 'client': Client, 'server': Server, 'event': Event, '@timestamp': Timestamp, 'cloud': Cloud, 
                'user_agent': Useragent, 'error': Error, 'custom': Custom, 'related': Related
               }

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        
        self['ecs'] = {'version': '1.9.0'}
  
