import json
import redis
from src.models.morador import Morador
from src.models.condominio import Condominio
from src.models.unidade import Unidade

def carregar_dados_iniciais(redis_client):
    """
    Carrega os dados iniciais do arquivo moradores.json para o Redis.
    """
    with open('data/moradores.json', 'r') as file:
        data = json.load(file)
    
    print("\n=== Carregando Dados dos Moradores no Redis ===")
    for morador_data in data['moradores']:
        morador = Morador(
            morador_data['nome'],
            morador_data['email'],
            morador_data['condominio'],
            morador_data['unidade']
        )
        
        # Salva o morador
        redis_client.hset(
            f"morador:{morador.nome}",
            mapping=morador.to_dict()
        )

        # Salva a unidade
        unidade = Unidade(morador.unidade, [morador.nome])
        unidade_dict = unidade.to_dict()
        # Serializa listas para string
        for k, v in unidade_dict.items():
            if isinstance(v, list):
                unidade_dict[k] = json.dumps(v, ensure_ascii=False)
        redis_client.hset(
            f"unidade:{morador.condominio}:{morador.unidade}",
            mapping=unidade_dict
        )

        # Salva o condomínio (adicionando a unidade à lista de unidades)
        condominio_key = f"condominio:{morador.condominio}"
        # Recupera unidades já existentes
        unidades = redis_client.hget(condominio_key, "unidades")
        if unidades:
            unidades = json.loads(unidades)
            if morador.unidade not in unidades:
                unidades.append(morador.unidade)
        else:
            unidades = [morador.unidade]
        condominio = Condominio(morador.condominio, unidades)
        redis_client.hset(
            condominio_key,
            mapping={"nome": condominio.nome, "unidades": json.dumps(condominio.unidades)}
        )
        
    print("\nDados carregados com sucesso no Redis!")

def buscar_moradores(redis_client):
    """
    Busca e exibe todos os moradores cadastrados no Redis.
    """
    print("\n=== Moradores Cadastrados ===")
    morador_keys = redis_client.keys('morador:*')
    if not morador_keys:
        print("Nenhum morador encontrado.")
        return

    for key in morador_keys:
        morador_data = redis_client.hgetall(key)
        print(f"\nNome: {morador_data[b'nome'].decode('utf-8')}")
        print(f"Email: {morador_data[b'email'].decode('utf-8')}")
        print(f"Condomínio: {morador_data[b'condominio'].decode('utf-8')}")
        print(f"Unidade: {morador_data[b'unidade'].decode('utf-8')}")
        print("-" * 30)

def buscar_unidades(redis_client):
    """
    Busca e exibe todas as unidades cadastradas no Redis.
    """
    print("\n=== Unidades Cadastradas ===")
    unidade_keys = redis_client.keys('unidade:*')
    if not unidade_keys:
        print("Nenhuma unidade encontrada.")
        return

    for key in unidade_keys:
        unidade_data = redis_client.hgetall(key)
        moradores = json.loads(unidade_data[b'moradores'].decode('utf-8'))
        print(f"\nUnidade: {unidade_data[b'numero'].decode('utf-8')}")
        print(f"Moradores: {', '.join(moradores)}")
        print("-" * 30)

def buscar_por_nome(redis_client):
    """
    Busca e exibe um morador específico pelo nome.
    """
    nome = input("\nDigite o nome do morador que deseja buscar: ")
    morador_data = redis_client.hgetall(f"morador:{nome}")

    if not morador_data:
        print(f"Morador com o nome '{nome}' não encontrado.")
        return

    print("\n=== Informações do Morador ===")
    print(f"Nome: {morador_data[b'nome'].decode('utf-8')}")
    print(f"Email: {morador_data[b'email'].decode('utf-8')}")
    print(f"Condomínio: {morador_data[b'condominio'].decode('utf-8')}")
    print(f"Unidade: {morador_data[b'unidade'].decode('utf-8')}")
    print("-" * 30)

def main():
    """
    Função principal que inicializa o cliente Redis, carrega os dados
    e exibe o menu de busca.
    """
    redis_client = redis.Redis(host='redis', port=6379, db=0)
    
    # Carrega os dados iniciais do JSON para o Redis
    carregar_dados_iniciais(redis_client)

    while True:
        print("\nO que você deseja fazer?")
        print("1. Buscar por todos os moradores")
        print("2. Buscar por todas as unidades")
        print("3. Buscar por nome de morador")
        print("4. Sair")

        opcao = input("Digite o número da opção desejada: ")

        if opcao == '1':
            buscar_moradores(redis_client)
        elif opcao == '2':
            buscar_unidades(redis_client)
        elif opcao == '3':
            buscar_por_nome(redis_client)
        elif opcao == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()