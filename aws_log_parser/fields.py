import datetime
import ipaddress
import functools
import logging
import socket
import urllib.parse

from geolite import geolite2
from dataclasses import dataclass
from http import cookies

from .exceptions import UnknownHttpType


logger = logging.getLogger(__name__)


@functools.lru_cache(max_size=8192)
def resolve_ipaddress(ip_address):
    return socket.gethostbyaddr(ip_address)[0]


@dataclass
class LogField:
    name: str
    raw_value: str

    @property
    def value(self):
        return self.raw_value.rstrip('"').lstrip('"')

    @property
    def parsed(self):
        raise NotImplemented

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.parsed


@dataclass
class StringField(LogField):

    @property
    def parsed(self):
        return self.value


@dataclass
class IntegerField(LogField):

    @property
    def parsed(self):
        return int(self.value)


@dataclass
class IpAddressField(LogField):

    @property
    def parsed(self):
        ipaddress.ip_address(self.value)

    def hostname(self):
        return resolve_ipaddress(self.value)

    def country(self):
        match = geolite2.lookup(self.value)
        return match.country if match else None


@dataclass
class FloatField(LogField):

    @property
    def parsed(self):
        return float(self.value)


@dataclass
class DictField(LogField):

    @property
    def parsed(self):
        return dict(self.value)


@dataclass
class HttpTypeField(LogField):

    @property
    def parsed(self):
        from .models import HttpType
        for ht in HttpType:
            if self.value == ht.value:
                return ht
        raise UnknownHttpType(self.value)


@dataclass
class DateTimeField(LogField):

    @property
    def parsed(self):
        return datetime.datetime.fromisoformat(
            self.value.rstrip('Z')
        ).replace(tzinfo=datetime.timezone.utc)


@dataclass
class HttpRequestField(LogField):

    @property
    def parsed(self):
        from .models import HttpRequest
        # The url can contain spaces
        split = self.value.split()
        url = ' '.join(split[1:-1])
        parsed = urllib.parse.urlparse(url)
        return HttpRequest(
            split[0],
            url,
            urllib.parse.parse_qs(parsed.query),
            split[-1],
        )


@dataclass
class CookieField(LogField):

    @property
    def parsed(self):
        cookie = cookies.SimpleCookie()
        cookie.load(rawdata=self.value)
        return cookie


@dataclass
class DateField(LogField):

    @property
    def parsed(self):
        return datetime.date.fromisoformat(self.value)


@dataclass
class TimeField(LogField):

    @property
    def parsed(self):
        return datetime.time.fromisoformat(self.value)


@dataclass
class ListField(LogField):

    @property
    def parsed(self):
        return self.value.split(',')


@dataclass
class LoadBalancerErrorReasonField(LogField):

    @property
    def parsed(self):
        from .models import LoadBalancerErrorReason
        return getattr(LoadBalancerErrorReason, self.value)


@dataclass
class HostField(LogField):

    @property
    def parsed(self):
        from .models import Host
        ip, port = self.value.split(':')
        return Host(ip, int(port))


@dataclass
class UrlQuotedField(LogField):

    @property
    def parsed(self):
        return urllib.parse.unquote(self.value).replace('%20', ' ')


@dataclass
class UrlQueryField(LogField):

    @property
    def parsed(self):
        return urllib.parse.parse_qs(self.value)