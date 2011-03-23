"""Decorator to create lazy attributes."""


class lazy(object):
    """lazy descriptor

    Used as a decorator to create lazy attributes. Lazy attributes
    are evaluated on first use.
    """

    def __init__(self, func):
        self.__func = func
        self.__name__ = func.__name__
        self.__module__ = func.__module__
        self.__doc__ = func.__doc__
        self.__dict__.update(func.__dict__)

    def __get__(self, inst, inst_cls):
        if inst is None:
            return self

        if not hasattr(inst, '__dict__'):
            raise AttributeError("'%s' object has no attribute '__dict__'" % (inst_cls.__name__,))

        name = self.__name__
        if name.startswith('__') and not name.endswith('__'):
            name = '_%s%s' % (inst_cls.__name__, name)

        value = self.__func(inst)
        inst.__dict__[name] = value
        return value

    @classmethod
    def invalidate(cls, inst, name):
        """Invalidate a lazy attribute.

        This obviously violates the lazy contract. A subclass of lazy
        may however have a contract where invalidation is appropriate.
        """
        inst_cls = inst.__class__

        if not hasattr(inst, '__dict__'):
            raise AttributeError("'%s' object has no attribute '__dict__'" % (inst_cls.__name__,))

        if name.startswith('__') and not name.endswith('__'):
            name = '_%s%s' % (inst_cls.__name__, name)

        if not isinstance(getattr(inst_cls, name), cls):
            raise AttributeError("'%s.%s' is not a %s attribute" % (inst_cls.__name__, name, cls.__name__))

        if name in inst.__dict__:
            del inst.__dict__[name]

