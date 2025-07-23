class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class globalKeyStore(metaclass=Singleton):
    def __init__(self):
        self.store = {}

    def set_value(self, key, value):
        self.store[key] = value

    def get_value(self, key):
        return self.store.get(key, None)

banana = globalKeyStore()
apple = globalKeyStore()
banana.set_value("fruit", "banana")
apple.set_value("fruit", "apple")
print(banana.get_value("fruit"))  # Output: banana
print(apple.get_value("fruit"))   # Output: banana, since both are the same instance
print(banana is apple)  # Output: True, both variables point to the same instance