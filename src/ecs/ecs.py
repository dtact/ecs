# noqa: D101,D100,D102
import json

import dateutil.parser
from datetime import datetime


class Int(int):  # noqa D101
    def __new__(cls, val):  # noqa D102

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
            val = dateutil.parser.isoparse(val).isoformat("T").replace("+00:00", "Z")
        elif isinstance(val, float) or isinstance(val, int):
            # normalize
            val = datetime.fromtimestamp(val).isoformat("T").replace("+00:00", "Z")
        else:
            val = val.isoformat("T").replace("+00:00", "Z")

        return super().__new__(cls, val)


class Duration(Int):
    pass


class Path(String):
    pass


class Query(String):
    def __new__(cls, val):
        if val is None:
            return
        elif type(val) is dict:
            if not val:
                return

            from urllib.parse import urlencode

            val = urlencode(val)
            return super().__new__(cls, val)
        elif type(val) is str:
            return super().__new__(cls, val)
        else:
            raise Exception("Unsupported type for query")


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
    """ """

    pass


class Address(String):
    """ """

    pass


class Base(dict):
    def __init__(self, *args):
        d = {}

        for arg in args:
            if arg is None:
                continue
            elif arg == {}:
                continue

            allowed = False
            for (k, t) in self._allowed.items():
                if type(arg) is t:
                    allowed = True

                    d[k] = arg

            if not allowed:
                raise Exception(
                    f"Type {type(arg)} not supported for {type(self)}, allowed are: {self._allowed}"
                )

        super().__init__(d)


class Original(String):
    pass


class User(Base):
    _allowed = {"name": Name, "id": Id}


class Target(User):
    pass


User._allowed.update({"target": Target})


class Error(Base):
    _allowed = {"code": Code, "id": Id, "message": Message}


class Event(Base):
    "Meta-information specific to ECS."

    _allowed = {
        "original": Original,
        "provider": Provider,
        "action": Action,
        "id": Id,
        "category": Category,
        "type": Type,
        "dataset": Dataset,
        "kind": Kind,
        "outcome": Outcome,
        "group": Group,
        "duration": Duration,
    }

    def __init__(self, name, *args, type=None):
        super().__init__(name, *args)

        if self.get("original"):
            self["original"] = json.dumps(self.get("original"))


class Source(Base):
    """
    Fields about the source side of network connection, used with destination.

    Source fields capture details about the sender of a network
    exchange/packet. These fields are populated from a network event,
    packet, or other event containing details of a network transaction.

    Source fields are usually populated in conjunction with destination
    fields. The source and destination fields are considered the baseline
    and should always be filled if an event contains source and destination
    details from a network transaction. If the event also contains
    identification of the client and server roles, then the client
    and server fields should also be populated.
    """

    _allowed = {
        "address": Address,
        "bytes": Bytes,
        "packets": Packets,
        "port": Port,
        "user": User,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        address = self.get("address")
        if address:
            try:
                import ipaddress

                self["ip"] = str(ipaddress.ip_address(address))
            except ValueError:
                self["domain"] = address


class Destination(Source):
    pass


class Client(Source):
    pass


class Server(Source):
    pass


class Account(Base):
    _allowed = {"id": Id, "name": Name}


class Region(String):
    pass


class Useragent(Base):
    _allowed = {"original": Original}


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
    _allowed = {"ip": IP, "hash": Hash, "hosts": Hosts, "user": Users}


class Cloud(Base):
    _allowed = {"account": Account, "region": Region}


class Method(String):
    pass


class StatusCode(Int):
    """ """

    pass


class Version(String):
    """ """

    pass


class Request(Base):
    """ """

    _allowed = {"method": Method}


class Response(Base):
    """ """

    _allowed = {"status_code": StatusCode}


class HTTP(Base):
    """
    Fields related to HTTP activity. Use the url field set to store the url of
    the request.
    """

    _allowed = {"request": Request, "response": Response, "version": Version}


class URL(Base):
    """
    Fields that let you store URLs in various forms.

    URL fields provide support for complete or partial URLs, and supports the
    breaking down into scheme, domain, path, and so on.
    """

    _allowed = {"original": Original, "path": Path, "query": Query}


class Custom(dict):
    def __init__(self, name, *args, type=None):
        d = {}

        for arg in args:
            if arg is None:
                continue

            if type is str:
                d = str(arg)
            elif type is bool:
                d = bool(arg)
            elif type is float:
                d = float(arg)
            elif type is int:
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

        super().__init__({name: d})


class Trace(Base):
    _allowed = {"id": Id}


class Cipher(String):
    pass


class TLS(Base):
    _allowed = {"version": Version, "cipher": Cipher}


class ECS(Base):
    """
    The Elastic Common Schema (ECS) is an open source specification, developed
    with support from the Elastic user community. ECS defines a common set of
    fields to be used when storing event data in Elasticsearch, such as logs
    and metrics.
    """

    _allowed = {
        "source": Source,
        "destination": Destination,
        "client": Client,
        "server": Server,
        "event": Event,
        "@timestamp": Timestamp,
        "cloud": Cloud,
        "user_agent": Useragent,
        "error": Error,
        "custom": Custom,
        "related": Related,
        "http": HTTP,
        "url": URL,
        "tls": TLS,
        "trace": Trace,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        self["ecs"] = {"version": "1.9.0"}
