def singleton(cls):
    instances = dict()

    def __new__(klass, *args, **kwargs):
        klass_path = klass.__module__ + '.' + klass.__name__
        instance = instances.get(klass_path, None)
        if instance is not None:
            return instance

        attributes = dict(klass.__dict__)
        attributes.pop('__new__')

        klass = type(klass.__name__, klass.__bases__, attributes)
        instances[klass_path] = klass(*args, **kwargs)
        return instances[klass_path]

    cls.__new__ = __new__
    return cls