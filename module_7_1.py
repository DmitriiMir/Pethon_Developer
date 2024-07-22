class Product:
    def __init__(self, name, weight, category):
        self.name = name
        self.weight = weight
        self.category = category

    def __str__(self):
        return f"{self.name}, {self.weight}, {self.category}"


class Shop:
    __file_name = 'products.txt'

    def __init__(self):
        open(self.__file_name, 'a').close()

    def get_products(self):
        with open(self.__file_name, 'r') as file:
            return file.read()

    def add(self, *products):
        existing_products = self._load_existing_products()
        with open(self.__file_name, 'a') as file:
            for product in products:
                if product.name in existing_products:
                    print(f"Продукт {product.name} уже есть в магазине")
                else:
                    file.write(str(product) + '\n')
                    existing_products[product.name] = product

    def _load_existing_products(self):
        products = {}
        with open(self.__file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(', ')
                if len(parts) == 3:
                    name, weight, category = parts
                    products[name] = Product(name, float(weight), category)
        return products


# Пример работы программы:
s1 = Shop()
p1 = Product('Potato', 50.5, 'Vegetables')
p2 = Product('Spaghetti', 3.4, 'Groceries')
p3 = Product('Potato', 5.5, 'Vegetables')

print(p2)

s1.add(p1, p2, p3)

print(s1.get_products())
