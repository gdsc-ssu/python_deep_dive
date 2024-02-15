import collections
import sys


class A:
    def __init__(self) -> None:
        self.a = "a"
        self.b = "b"
        self.c = "c"
        self.d = "d"
        self.e = "e"


Test = collections.namedtuple("Test", "a b c d e")
test = Test(*[i for i in "a b c d e".split()])
test_dict = {i: i for i in "a b c d e".split()}
test_class = A()

print(f"tuple_size: {sys.getsizeof(test)}")
print(f"dict_size: {sys.getsizeof(test_dict)}")
print(f"class_size: {sys.getsizeof(test_class.__dict__)}")
