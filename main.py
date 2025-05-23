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
        
        redis_client.hset(
            f"morador:{morador.nome}",
            mapping=morador.to_dict()
        )
        
    print("\nDados carregados com sucesso no Redis!")

if __name__ == "__main__":
    main() 