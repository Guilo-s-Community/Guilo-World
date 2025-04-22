import zmq
import msgpack
import sys
ctx = zmq.Context()

client = ctx.socket(zmq.REQ)
client.connect("tcp://localhost:7001")
n1 = 0
n2 = 0

while True:
    op = int(input("Escreva a operação desejada: \n"
                 "1 - Soma\n"
                 "2 - Subtração\n"
                 "3 - Divisão\n"
                 "4 - Divisão Flutuante\n"
                 "5 - Multiplicação\n"
                 "6 - Raiz Quadrada\n"
                 "0 - Sair\n"))
    
    if op == 1 or op == 2 or op == 5:
        n1 = int(input("Digite o primeiro valor: "))
        n2 = int(input("Digite o segundo valor: "))
    elif op == 3 or op == 4:
        n1 = float(input("Digite o primeiro valor: "))
        n2 = float(input("Digite o segundo valor: "))
    elif op == 6:
        n1 = int(input("Digite o valor: "))
    elif op == 0:
        sys.exit()
    else:
        print("incorreto")


    msg = {"Operações" : op, "n1": n1, "n2" : n2}
    msg_p = msgpack.packb(msg)
    client.send(msg_p)

    reply_p = client.recv()
    reply = msgpack.unpackb(reply_p)
    print(f"Resultado da conta: {reply}")
