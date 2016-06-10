import os
here = os.path.abspath(os.path.dirname(__file__))
base = here
def join(*paths):
    print(paths)
    l = os.path.join(base, *paths)
    print(l)
    return l