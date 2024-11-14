class DataTypePrinter:
    def __init__(self):
        self.data_types = {
            'str': str,
            'int': int,
            'float': float,
            'complex': complex,
            'list': list,
            'tuple': tuple,
            'range': range,
            'dict': dict,
            'set': set,
            'frozenset': frozenset,
            'bool': bool,
            'bytes': bytes,
            'bytearray': bytearray,
            'memoryview': memoryview,
            'NoneType': type(None)
        }

    def print_data(self, var):
        data_type = type(var).__name__
        if var is None:
            data_type = "NoneType"
        
        print(f"Data Type: {data_type}")
        print(f"Variable Content: {var}\n")

        # Check for nested structures
        for dt in self.data_types.values():
            if isinstance(var, dt):
                self.print_nested_data(dt, var)
                break

    def print_nested_data(self, data_type, var):
        if isinstance(var, dict):
            items = [f'{k}: {self.get_value(v)}' for k, v in var.items()]
            print(f"{data_type}({', '.join(items)})")
        elif isinstance(var, (list, tuple)):
            if len(var) == 0:
                print(f"  [] or ()")
            else:
                print(f"{data_type}({', '.join(map(str, [self.get_value(v) for v in var]))})")
        else:
            print(data_type(var))

    def get_value(self, var):
        if isinstance(var, (list, tuple)):
            return [self.get_value(v) for v in var]
        elif isinstance(var, dict):
            return {k: self.get_value(v) for k, v in var.items()}
        else:
            return str(var)


# Example usage
printer = DataTypePrinter()
print("Integer:")
printer.print_data(10)

print("\nFloat:")
printer.print_data(3.14)

print("\nString:")
printer.print_data("Hello, World!")

print("\nComplex Number:")
printer.print_data(complex(1, 2))

print("\nList of integers:")
printer.print_data([1, 2, 3])

print("\nTuple of strings:")
printer.print_data(('hello', 'world'))

print("\nDictionary with string keys and integer values:")
printer.print_data({'key': 10, 'other_key': 20})

print("\nSet of unique integers:")
printer.print_data({1, 2, 3, 4, 5})

print("\nBoolean value:")
printer.print_data(True)

print("\nBytes object:")
printer.print_data(b'Hello, World!')

print("\nByte array object:")
printer.print_data(bytearray(b'Hello, World!'))

print("\nMemory view object:")
printer.print_data(memoryview(b'Hello, World!'))
