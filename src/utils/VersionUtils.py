def read_version():
    with open('VERSION.txt', 'r') as f:
        version = f.read()
    return version
