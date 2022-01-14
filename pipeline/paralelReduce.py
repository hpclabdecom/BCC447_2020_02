import concurrent.futures
import os


class OperationParalel:
    def __init__(self, operation, operation2, cpu_count=os.cpu_count()):
        self.operation = operation
        self.cpu_count = cpu_count
        self.operation2 = operation2

    def run(self, values, higth=0):
        if len(values) <= 2 or 2 ** higth > self.cpu_count:
            return self.operation(values)
        else:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # dividir vetor
                values_left = values[:len(values) // 2]
                values_right = values[len(values) // 2:]

                # chamadas recusivas, esquerda e direita
                left_future = executor.submit(self.run, values_left, higth + 1)
                right_future = executor.submit(self.run, values_right, higth + 1)

                # results
                result_left = None
                result_right = None

                if not left_future.running():
                    if left_future.cancel():
                        print("Cancel Left")
                        result_left = self.operation(values_left)

                if not right_future.running():
                    if right_future.cancel():
                        result_right = self.operation(values_right)

                if result_left is None:
                    result_left = left_future.result()

                if result_right is None:
                    result_right = right_future.result()

                return self.operation2(result_left, result_right)

class OperationParalel2:
    def __init__(self, operation):
        self.operation = operation
        self.cpu_count = os.cpu_count()

    def run(self, values, higth=0):
        if len(values) <= 2 or 2 ** higth > self.cpu_count:
            return self.operation(values)
        else:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # dividir vetor
                values_left = values[:len(values) // 2]
                values_right = values[len(values) // 2:]

                # chamadas recusivas, esquerda e direita
                left_future = executor.submit(self.run, values_left, higth + 1)
                right_future = executor.submit(self.run, values_right, higth + 1)

                # results
                result_left = None
                result_right = None

                if not left_future.running():
                    if left_future.cancel():
                        print("Cancel Left")
                        result_left = self.operation(values_left)

                if not right_future.running():
                    if right_future.cancel():
                        result_right = self.operation(values_right)

                if result_left is None:
                    result_left = left_future.result()

                if result_right is None:
                    result_right = right_future.result()

                return self.operation([result_left, result_right])


if __name__ == "__main__":
    pass
