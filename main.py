from IDEA import IDEA


def main():
    # key = 0x00000000000000000000000000000000
    # plain  = 0x8000000000000000
    # cipher = 0x8001000180008000

    key = 0x2BD6459F82C5B300952C49104881FF48
    plain = 0xF129A6601EF62A47
    cipher = 0xEA024714AD5C4D84

    print('key:\t\t', hex(key))
    print('plaintext:\t', hex(plain))

    crypto_idea = IDEA(key)

    encrypted = crypto_idea.encrypt(plain)

    assert encrypted == cipher

    print('ciphertext\t', hex(cipher))


if __name__ == '__main__':
    main()
