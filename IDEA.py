from IDEA_operations import _keys_addition_layer, _multiply_addition_layer

"""
Данный файл является классовым представлением алгоритма шифрования IDEA
"""


class IDEA:
    def __init__(self, key: int) -> None:
        """

        :param key: int
        """
        self._keys: tuple | None = None
        self.change_key(key)

    def change_key(self, key: int) -> None:
        """

        :param key: int
        """
        modulus = 1 << 128  # 2 ** 128
        assert 0 <= key < modulus

        sub_keys = []
        for i in range(8 * 6 + 4):  # количество подключей (6 ключей в 8 раундах и 4 ключа в финальном)
            sub_keys.append((key >> (112 - 16 * (i % 8))) % 0x10000)  # нарезаем подключи по 16 бит
            if i % 8 == 7:  # последняя итерация каждого разбиения
                key = ((key << 25) | (key >> 103)) % modulus  # двигаем блок на 25 позиций влево
        keys = []
        for i in range(9):
            round_keys = sub_keys[6 * i: 6 * (i + 1)]  # последний срез вернёт 4 ключа
            keys.append(tuple(round_keys))
        self._keys = tuple(keys)

    def encrypt(self, plaintext: int) -> int:
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

        """
        Слова x2, x3 в 9ом раунде не переставляются. (раунд без MA) 
        Соответсвенно нужно поменять их местами
        """
        y1, y2, y3, y4 = _keys_addition_layer(x1, x3, x2, x4, self._keys[8])

        cipher_text = (y1 << 48) | (y2 << 32) | (y3 << 16) | y4
        return cipher_text

    @staticmethod
    def generate_private_key() -> int:
        from secrets import token_hex

        return int(token_hex(32), 16) >> 128
