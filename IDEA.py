class IDEA:
    def __init__(self, key: int):
        self.keys: tuple | None = None
        self.change_key(key)

    def change_key(self, key: int):
        modulus = 1 << 128
        assert 0 <= key < modulus

        sub_keys = []

        for i in range(9 * 6):
            sub_keys.append()



