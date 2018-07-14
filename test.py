class Singleton(object):
    __singleton = None

    def __init__(self):
        pass

    @staticmethod
    def get_instance():
        if Singleton.__singleton is None:
            Singleton.__singleton = Singleton()
        return Singleton.__singleton

if __name__ == "__main__":
    instance1 = Singleton.get_instance()
    instance2 = Singleton.get_instance()

    print
    id(instance1)
    print
    id(instance2)