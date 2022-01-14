
produtos = ["1", "2", "3", "4", "5", "6"]

def buscarProduto (codigo):
    for p in produtos:
        if p == codigo:
            return True
    return False

fechouCompra = False

while not fechouCompra:
    p = input("Digite o numero do produto: ")

    achou = buscarProduto(p)

    if achou:
        print("Produto encontrado")
    else:
        print("Produto não encontrado")

    fechou = input("A compra foi fechada (s/n)? ")
    if fechou == 's':
        fechouCompra = True