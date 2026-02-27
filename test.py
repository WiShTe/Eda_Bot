import random

products = 'рис - 100г, мясо - 500г, лук - 100г, лук - 500г'
products = products.split(", ")
SpisokPokuopok = dict()
sum = 0
for product in products:
    name_of_product = product.split('-')[0].replace(" ", "")
    print(name_of_product)
    weight_of_product = int(product.split('-')[1].replace("г", ''))
    print(weight_of_product)
    print(name_of_product, weight_of_product)
    if name_of_product not in SpisokPokuopok:
        SpisokPokuopok[name_of_product] = weight_of_product
    else:
        SpisokPokuopok[name_of_product] += weight_of_product

print(SpisokPokuopok)

lst = list(SpisokPokuopok.keys())
for i in range(21):
    roll = random.randint(1, 6)
    print(roll)