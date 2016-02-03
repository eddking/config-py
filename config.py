
def _ensure_array(key):
    if isinstance(key, list):
        return key
    if isinstance(key, basestring):
        key = [str(key)]
    if isinstance(key, tuple):
        key = list(key)
    return key

class Config(object):

    def __init__(self, data):
        self.data = data
        self.fallback = None

    def get(self, *key, **opts):
        return self._get(_ensure_array(key), opts)

    def _get(self, key, opts):
        d = self.data
        default = opts.get('default', None)
        ignore_missing = opts.get('ignore_missing', False)
        expect = opts.get('expect', None)

        for part in key:
            if not d.has_key(part):
                if self.fallback is not None:
                    return self.fallback._get(key, opts)
                if default is not None:
                    return default
                elif ignore_missing:
                    return None
                else:
                    raise Exception('config entry missing: ' + '.'.join(key))
            d = d[part]

        if expect is not None:
            if not isinstance(d, expect):
                raise Exception('config entry {} is the wrong type, expected: {}'.format('.'.join(key), expect.__name__))
        return d

    def refine(self, *key):
        return ConfigView(self, _ensure_array(key))

    def set_fallback(self, *fallbacks):
        if self.fallback is not None:
            raise Exception('config already has a fallback')
        self.fallback = fallbacks[0]
        #This lets you set multiple fallbacks in one method call, by chaining them together
        for c, n in zip(fallbacks[:-1], fallbacks[1:]):
            c.set_fallback(n)

class ConfigView(object):

    def __init__(self, config, prefix):
        self.config = config
        self.prefix = prefix

    def get(self, *key, **opts):
        key = _ensure_array(key)
        return self.config._get(self.prefix + key, opts)

    def refine(self, *key):
        key = _ensure_array(key)
        return ConfigView(self.config, self.prefix + key)

