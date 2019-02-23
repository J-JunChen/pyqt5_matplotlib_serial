class Foo(object):
    def __init__(self):
              self._number_of_times = 0

    def yourfunc(self, x, y):
       for i in range(x):
              for j in range(y):
                     self._number_of_times += 1
       print(self._number_of_times)

yourfunc = Foo().yourfunc(2,5)
