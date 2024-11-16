class data_dumper:
    data_types = {
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
    
    def __init__(self):
        pass

    def print_data(self, var):
        data_type = type(var).__name__
        if var is None:
            data_type = "NoneType"
        
        print(f"Data Type: {data_type}")
        print(f"Variable Content: {var}\n")

        # Check for nested structures
        for dt in data_dumper.data_types.values():
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
