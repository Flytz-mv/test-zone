import json
import redis
from src.models.morador import Morador
from src.models.condominio import Condominio
from src.models.unidade import Unidade

def main():
    redis_client = redis.Redis(host='redis', port=6379, db=0)
    
    with open('data/moradores.json', 'r') as file:
        data = json.load(file)
    
    print("\n=== Dados dos Moradores ===")
    for morador_data in data['moradores']:
        print(f"\nNome: {morador_data['nome']}")
        print(f"Email: {morador_data['email']}")
        print(f"Condomínio: {morador_data['condominio']}")
        print(f"Unidade: {morador_data['unidade']}")
        print("-" * 30)
        
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

if __name__ == "__main__":
    main()