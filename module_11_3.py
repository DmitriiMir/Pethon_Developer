def introspection_info(obj):
    info = {
        'type': type(obj).__name__,
        'attributes': [attr for attr in dir(obj) if not callable(getattr(obj, attr))],
        'methods': [method for method in dir(obj) if callable(getattr(obj, method))],
        'module': getattr(obj, '__module__', 'built-in')
    }

    # Информвция по каждому элементу
    print(f"'type': {info['type']}")
    print(f"'attributes': {', '.join(info['attributes'])}")
    print(f"'methods': {', '.join(info['methods'])}")
    print(f"'module': {info['module']}")

# Вывод примера из д/з
introspection_info(42)

# Пример на собственном классе
class ExampleClass:
    def __init__(self, value):
        self.value = value

    def example_method(self):
        return self.value

example_obj = ExampleClass('MyString')
introspection_info(example_obj)
