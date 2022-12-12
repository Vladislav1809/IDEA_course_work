"""
фундаментальные операции в IDEA
1) сложение по модулю 2**16 (16**4)
2) умножение по модулю 2**16 + 1 (16 ** 4 + 1)
3) XOR | побитовое исключающее или

никакие 2 из этих операций:
 - не удовлетворяют дистрибутивному закону
 - не удовлетворяют ассоциативному закону
"""


def _multiply(x: int, y: int) -> int:
    assert 0 <= x <= 0xFFFF, 'x не попал в интервал от 0 до 16**4 - 1'  # 16**4 - 1
    assert 0 <= y <= 0xFFFF, 'y не попал в интервал от 0 до 16**4 - 1'

    if x == 0:
        x = 0x10000  # 16**4
    if y == 0:
        y = 0x10000

    r = (x * y) % 0x10001  # 16**4 + 1

    if r == 0x10000:
        r = 0

    assert 0 <= r <= 0xFFFF, 'результат умножения по модулю 16 ** 4 + 1 ' \
                             'не попал в интервал от 0 до 16 ** 4 - 1'
    return r


def _keys_addition_layer(p1: int, p2: int, p3: int, p4: int, round_keys: list) -> tuple:
    assert 0 <= p1 <= 0xFFFF
    assert 0 <= p2 <= 0xFFFF
    assert 0 <= p3 <= 0xFFFF
    assert 0 <= p4 <= 0xFFFF
    k1, k2, k3, k4 = round_keys[0:4]
    assert 0 <= k1 <= 0xFFFF
    assert 0 <= k2 <= 0xFFFF
    assert 0 <= k3 <= 0xFFFF
    assert 0 <= k4 <= 0xFFFF

    y1: int = _multiply(p1, k1)
    y2: int = (p2 + k2) % 0x10000
    y3: int = (p3 + k3) % 0x10000
    y4: int = _multiply(p4, k4)

    return y1, y2, y3, y4


def _multiply_addition_layer(y1: int, y2: int, y3: int, y4: int, round_keys: list) -> tuple:
    assert 0 <= y1 <= 0xFFFF
    assert 0 <= y2 <= 0xFFFF
    assert 0 <= y3 <= 0xFFFF
    assert 0 <= y4 <= 0xFFFF
    k5, k6 = round_keys[4:6]
    assert 0 <= k5 <= 0xFFFF
    assert 0 <= k6 <= 0xFFFF

    p = y1 ^ y3
    q = y2 ^ y4

    s = _multiply(p, k5)
    _ = (q + s) % 0x10000
    t = _multiply(_, k6)
    u = (s + t) % 0x10000

    return y1 ^ t, y2 ^ u, y3 ^ t, y4 ^ u
