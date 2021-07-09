# 'Here’s a project for devoted matrix enthusiasts: learn to perform a variety
# of operations on matrices including addition, multiplication, finding the determinant,
# and dealing with inverse matrices. If you are working on your tech or math major,
# this project is a good chance for you to learn matrices in action and not just in
# your notebook.

class MatrixDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if type(value) is not list or not len(value) or not all(list(map(lambda x: type(x) is list, value))):
            raise TypeError("It's incorrect type. It have to be a nested <list>")
        if len(value) * len(value[0]) != sum(list(map(len, value))):
            raise ValueError("It has unstructured data")
        if not all([type(x) in (int, float) for row in value for x in row]):
            raise TypeError('The enclosed data must be <int> or <float>')
        instance.__dict__[self.name] = value


class Matrix:
    A = MatrixDescriptor()

    def __init__(self, value=None):
        if value is None:
            self.A = [[]]
        else:
            self.A = value

    def __str__(self):
        return '\n'.join([' '.join(map(str, x)) for x in self.A])

    def __add__(self, other):
        if isinstance(other, Matrix) and self.dim == other.dim:
            matrices_sum = []
            for i, value in enumerate(self.A):
                matrices_sum.append(list(map(sum, zip(value, other.A[i]))))
            return Matrix(matrices_sum)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Matrix) and self.dim[1] == other.dim[0]:
            return Matrix([[sum(map(lambda x, y: x * y, row, column))
                            for column in other.T] for row in self.A])
        elif isinstance(other, (int, float)):
            return Matrix([list(map(lambda x: x * other, row)) for row in self.A])
        else:
            return NotImplemented

    @staticmethod
    def __dimA(mtrx):
        return len(mtrx) if mtrx[0] else 0, len(mtrx[0])

    @staticmethod
    def __zip(value):
        return list(map(list, zip(*value)))

    def __detA(self, mtrx):
        if all(map(lambda x: x == 2, self.__dimA(mtrx))):  # JFF
            mtrx[1].reverse()
            dia_sums = tuple(map(lambda x, y: x * y, *mtrx))
            return dia_sums[0] - dia_sums[1]
            # return mtrx[0][0] * mtrx[1][1] - mtrx[0][1] * mtrx[1][0]  # It's JSS
        else:
            result = 0
            for j, col in enumerate(mtrx[0]):
                result += self.__detA(self.__cof(mtrx, (0, j))) * pow(-1, sum((1, j + 1))) * col
            return result

    def __cof(self, mtrx, idx):  # idx - tuple of Minor coordinate (i, j)
        if any(map(lambda x, y: x > y - 1, idx, self.__dimA(mtrx))):
            raise IndexError
        else:
            return [[x for j, x in enumerate(row) if j != idx[1]] for i, row in enumerate(mtrx) if i != idx[0]]

    @property
    def dim(self):
        return self.__dimA(self.A)

    @property
    def T(self):
        return self.__zip(self.A)

    @property
    def sT(self):
        return self.__zip([row[::-1] for row in self.A[::-1]])

    @property
    def vT(self):
        return [row[::-1] for row in self.A]

    @property
    def hT(self):
        return self.A[::-1]

    @property
    def C(self):  # nested list of cofactors
        return [[self.__detA(self.__cof(self.A, (i, j))) * pow(-1, sum((i + 1, j + 1)))
                 for j in range(len(row))] for i, row in enumerate(self.A)]

    @property
    def det(self):
        if len(self.A) == 1:
            return self.A[0][0]
        elif self.dim[0] != self.dim[1] or sum(self.dim) == 0:
            return None
        else:
            return self.__detA(self.A)


class Processor:
    def __init__(self):
        self.active = True
        self.matrices = {}
        self.main_menu = {'1': {'text': 'Add matrices',
                                'action': self.add},
                          '2': {'text': 'Multiply matrix by a constant',
                                'action': self.multiply_w_const},
                          '3': {'text': 'Multiply matrices',
                                'action': self.multiply},
                          '4': {'text': 'Transpose matrix',
                                'action': self.transpose},
                          '5': {'text': 'Calculate a determinant',
                                'action': self.determinant},
                          '6': {'text': 'Inverse matrix',
                                'action': self.inverse},
                          '0': {'text': 'Exit',
                                'action': self.exit}}

        self.transpose_menu = {'1': {'text': 'Main diagonal',
                                     'value': 'T'},
                               '2': {'text': 'Side diagonal',
                                     'value': 'sT'},
                               '3': {'text': 'Vertical line',
                                     'value': 'vT'},
                               '4': {'text': 'Horizontal line',
                                     'value': 'hT'}}

    @staticmethod
    def show_menu(menu):
        for key, value in menu.items():
            print(f'{key}. {value.get("text")}')

    @staticmethod
    def new_matrix(name=None):
        message = 'Enter size of matrix:'.split()
        if name is not None:
            message.insert(-1, name)
        matrix_rows = int(input(f"{' '.join(message)} ").split()[0])
        print('Enter', 'matrix:', sep=' ' if name is None else f' {name} ')
        return Matrix([list(map(float, input().split())) for _ in range(matrix_rows)])

    def add(self):
        try:
            matrices_sum = self.new_matrix('first') + self.new_matrix('second')
            print(f'The result is:\n{matrices_sum}\n')
        except TypeError:
            print('The operation cannot be performed.\n')

    def multiply(self, constant=False):
        try:
            first_multiplier = self.new_matrix('first' if not constant else None)
            second_multiplier = float(input('Enter constant: ')) if constant else self.new_matrix('second')
            print(f'The result is:\n{first_multiplier * second_multiplier}\n')
        except TypeError:
            print('The operation cannot be performed.\n')

    def multiply_w_const(self):
        self.multiply(True)

    def transpose(self):
        self.show_menu(self.transpose_menu)
        trans_method = self.transpose_menu[input('Your choice: ')]['value']
        print(Matrix(self.new_matrix().__getattribute__(trans_method)))

    def determinant(self):
        print(f'The result is:\n{self.new_matrix().det}\n')

    def inverse(self):
        new_matrix = self.new_matrix()
        if new_matrix.det == 0:
            print("This matrix doesn't have an inverse.\n")
        else:
            print(f'The result is:\n{Matrix(Matrix(new_matrix.C).T) * (1 / new_matrix.det)}\n')

    def exit(self):
        self.active = False

    def start(self):
        while self.active:
            self.show_menu(self.main_menu)
            self.main_menu.get(input('Your choice: '))['action']()


if __name__ == '__main__':
    proc = Processor()
    proc.start()
