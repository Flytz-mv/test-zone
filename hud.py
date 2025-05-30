import redis

def listar_moradores_por_condominio(condominio_nome, redis_client):
    moradores = []
    for key in redis_client.scan_iter("morador:*"):
        morador = redis_client.hgetall(key)
        if morador.get("condominio") == condominio_nome:
            moradores.append(morador)
    return moradores

def buscar_morador_por_nome(nome, redis_client):
    for key in redis_client.scan_iter("morador:*"):
        morador = redis_client.hgetall(key)
        if morador.get("nome", "").lower() == nome.lower():
            return morador
    return None

def listar_condominios(redis_client):
    condominios = []
    for key in redis_client.scan_iter("condominio:*"):
        condominio = redis_client.hgetall(key)
        condominios.append(condominio.get("nome"))
    return condominios

def main():
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    while True:
        print("\n=== HUD - Consulta de Dados ===")
        print("Opções disponíveis:")
        print("1 - Listar moradores por condominio")
        print("2 - Buscar morador por nome")
        print("3 - Listar todos os condominios")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            condominio = input("Digite o nome do condominio: ")
            moradores = listar_moradores_por_condominio(condominio, redis_client)
            if moradores:
                print(f"\nMoradores do condominio '{condominio}':")
                for m in moradores:
                    print(f"- {m.get('nome')} (Unidade: {m.get('unidade')}, Email: {m.get('email')})")
            else:
                print("Nenhum morador encontrado para esse condominio.")
        elif opcao == "2":
            nome = input("Digite o nome do morador: ")
            morador = buscar_morador_por_nome(nome, redis_client)
            if morador:
                print(f"\nMorador encontrado:")
                print(f"Nome: {morador.get('nome')}")
                print(f"Email: {morador.get('email')}")
                print(f"Condominio: {morador.get('condominio')}")
                print(f"Unidade: {morador.get('unidade')}")
            else:
                print("Morador não encontrado")
        elif opcao == "3":
            condominios = listar_condominios(redis_client)
            if condominios:
                print("\ncondominios cadastrados:")
                for c in condominios:
                    print(f"- {c}")
            else:
                print("nenhum condominio cadastrado")
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("opcao invalida tente novamente")

if __name__ == "__main__":
    main()