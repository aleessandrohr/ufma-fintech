import json
from pathlib import Path
from .cliente import Cliente
from .proposta import Proposta

def carregar_propostas_mock(caminho: Path | None = None) -> list[Proposta]:
    """Lê o arquivo JSON e retorna uma lista de propostas mockadas."""
    if caminho is None:
        # Por padrão, assume que o script roda da raiz e acessa data/clientes_teste.json
        caminho = Path("data/clientes_teste.json")
        
    with caminho.open("r", encoding="utf-8") as f:
        dados = json.load(f)
        
    propostas = []
    for d in dados:
        cliente = Cliente(
            id=d["id"],
            nome=d["nome"],
            idade=d["idade"],
            renda_mensal=d["renda_mensal"],
            score=d["score"],
            dividas_em_aberto=d["dividas_em_aberto"],
            atrasos_ultimos_12_meses=d["atrasos_ultimos_12_meses"]
        )
        proposta = Proposta(
            cliente=cliente,
            valor_solicitado=d["valor_solicitado"],
            parcelas=d["parcelas"],
            finalidade=d["finalidade"]
        )
        propostas.append(proposta)
        
    return propostas

def buscar_proposta_por_id(id_cliente: str, caminho: Path | None = None) -> Proposta | None:
    """Busca uma proposta específica pelo ID do cliente."""
    propostas = carregar_propostas_mock(caminho)
    for p in propostas:
        if p.cliente.id == id_cliente:
            return p
    return None
