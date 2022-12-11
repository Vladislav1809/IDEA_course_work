from IDEA_operations import _keys_addition_layer, _multiply_addition_layer


class IDEA:
    def __init__(self, key: int):
        self._keys: tuple | None = None
        self.change_key(key)

    def change_key(self, key: int):
        modulus = 1 << 128  # 2 ** 128
        assert 0 <= key < modulus

        sub_keys = []

        for i in range(9 * 6):
            sub_keys.append((key >> (112 - 16 * (i % 8))) % 0x10000)
            if i % 8 == 7:
                key = ((key << 25) | (key >> 103)) % modulus

        keys = []
        for i in range(9):
            round_keys = sub_keys[6 * i: 6 * (i + 1)]
            keys.append(tuple(round_keys))
        self._keys = tuple(keys)

    def encrypt(self, plaintext):
        assert 0 <= plaintext < (1 << 64), 'длина вводимого текста ' \
                                           'больше допустимого значения'

        x1 = (plaintext >> 48) & 0xFFFF
        x2 = (plaintext >> 32) & 0xFFFF
        x3 = (plaintext >> 16) & 0xFFFF
        x4 = plaintext & 0xFFFF

        for i in range(8):
            round_keys = self._keys[i]

            y1, y2, y3, y4 = _keys_addition_layer(x1, x2, x3, x4, round_keys)
            x1, x2, x3, x4 = _multiply_addition_layer(y1, y2, y3, y4, round_keys)

            x2, x3 = x3, x2

            y1, y2, y3, y4 = _keys_addition_layer(x1, x2, x3, x4, self._keys[8])

            cipher_text = hex((y1 << 48) | (y2 << 32) | (y3 << 16) | y4)
            return cipher_text


