def logger(func):
    def inner(*args, **kwargs):
        print("\033[35m{}\033[m( {}, {} )".format(func.__name__, args, kwargs))
        return func(*args, **kwargs)
    return inner


def print_args(*args, **kwargs):
    for arg in args:
        print("{}={}".format(eval("'arg'"), arg))
    for arg in kwargs.keys():
        print("{}={}".format(arg, kwargs[args]))