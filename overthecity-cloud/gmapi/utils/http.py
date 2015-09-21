from django.utils.encoding import smart_str
from urllib import quote_plus


def urlencode(query, doseq=0, safe=''):
    """Custom urlencode that leaves static map delimiters ("|", ",", ":") alone.

    Can operate on unicode strings. The parameters are first cast to UTF-8
    encoded strings and then encoded as per normal.

    """
    safe = safe + '|,:'
    if hasattr(query, 'items'):
        query = query.items()
    return '&'.join(['='.join([quote_plus(smart_str(k), safe=safe),
                               quote_plus(smart_str(v), safe=safe)])
                     for k, s in query
                     for v in ((isinstance(s, basestring) and [s])
                               or (doseq and hasattr(s, '__len__') and s)
                               or [s])])
