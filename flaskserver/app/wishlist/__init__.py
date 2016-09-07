try:
    FileNotFoundError = FileNotFoundError
except:
    from exceptions import IOError
    class FileNotFoundError(IOError):
        pass
