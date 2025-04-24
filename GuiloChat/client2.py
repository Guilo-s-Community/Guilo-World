import httpx

with httpx.Client() as client:
    try:
        r = client.get("http://localhost:8000/")
        if r.status_code == 200:
            print(r.text)
        else:
            print("Erro no servidor da porta 8000")
    except httpx.RequestError:
        print("Não foi possível conectar ao servidor da porta 8000. Tentando a porta 8001...")
        try:
            r1 = client.get("http://localhost:8001/")
            if r1.status_code == 200:
                print(r1.text)
            else:
                print("Erro no servidor da porta 8001")
        except httpx.RequestError:
            print("Não foi possível conectar ao servidor da porta 8001. Tentando a porta 8002...")
            try:
                r2 = client.get("http://localhost:8002/")
                if r2.status_code == 200:
                    print(r1.text)
                else:
                    print("Erro no servidor da porta 8002")
            except httpx.RequestError:
                print("Não foi possível conectar ao servidor da porta 8002. Encerrando programa")