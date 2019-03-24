class BrokenDexstoreInstance():
    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, name):
        raise ValueError("Attempting to use BrokenDexstoreInstance")


class DexstoreIsolator(object):
    enabled = False

    @classmethod
    def enable(self):
        if not self.enabled:
            from dexstore.instance import set_shared_dexstore_instance
            broken = BrokenDexstoreInstance()
            set_shared_dexstore_instance(broken)
            self.enabled = True
