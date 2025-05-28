import gradio as gr
import redis
import json

def get_redis_data():
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    output = ""

    # Moradores
    output += "=== Moradores ===\n"
    for key in redis_client.scan_iter("morador:*"):
        morador = redis_client.hgetall(key)
        output += f"{key.replace('morador:', '')}: {morador}\n"

    # Unidades
    output += "\n=== Unidades ===\n"
    for key in redis_client.scan_iter("unidade:*"):
        unidade = redis_client.hgetall(key)
        # Decodifica listas se necessário
        for k, v in unidade.items():
            try:
                unidade[k] = json.loads(v)
            except Exception:
                pass
        output += f"{key.replace('unidade:', '')}: {unidade}\n"

    # Condomínios
    output += "\n=== Condomínios ===\n"
    for key in redis_client.scan_iter("condominio:*"):
        condominio = redis_client.hgetall(key)
        # Decodifica listas se necessário
        for k, v in condominio.items():
            try:
                condominio[k] = json.loads(v)
            except Exception:
                pass
        output += f"{key.replace('condominio:', '')}: {condominio}\n"

    return output

iface = gr.Interface(
    fn=get_redis_data,
    inputs=[],
    outputs="text",
    title="Visualização dos Dados do Redis",
    description="Veja os moradores, unidades e condomínios carregados no Redis."
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0")