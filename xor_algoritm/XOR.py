class XOR:
    def __init__(self, first_number: int, second_number: int):
        self.int_xor_result = 0
        self.binary_xor_result = None
        (self.int_first_number, self.int_second_number) = (first_number, second_number)
        # print(self.int_first_number, self.int_second_number)
        (self.binary_first_number, self.binary_second_number) = (f'{first_number:b}', f'{second_number:b}')
        # print(self.binary_first_number, self.binary_second_number)

    def __call__(self):
        print(self.int_first_number, self.int_second_number)
        print(self.int_first_number ^ self.int_second_number)
        self.int_xor_result: int = self.int_first_number ^ self.int_second_number
        self.binary_xor_result = f'{self.int_xor_result:b}'
        return self.int_xor_result
