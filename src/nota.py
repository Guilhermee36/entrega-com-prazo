from dataclasses import dataclass
from datetime import timedelta


@dataclass
class ResultadoEntrega:
    aceita: bool
    nota_final: float
    dias_atraso: int
    desconto_percentual: int
    motivo: str


def calcular_nota_final(nota, prazo, entrega, justificativa_aprovada, novo_prazo):
    if not 0 <= nota <= 10:
        raise ValueError("nota deve estar entre 0 e 10")
    if justificativa_aprovada and novo_prazo is None:
        raise ValueError("novo_prazo e obrigatorio para justificativa aprovada")

    prazo_efetivo = novo_prazo if justificativa_aprovada else prazo
    if entrega <= prazo_efetivo:
        return ResultadoEntrega(
            aceita=True,
            nota_final=round(nota, 2),
            dias_atraso=0,
            desconto_percentual=0,
            motivo="justificativa" if justificativa_aprovada else "no_prazo",
        )

    atraso = entrega - prazo_efetivo
    dias_atraso = atraso // timedelta(days=1)
    if atraso % timedelta(days=1):
        dias_atraso += 1

    if atraso > timedelta(days=5):
        return ResultadoEntrega(
            aceita=False,
            nota_final=0.0,
            dias_atraso=dias_atraso,
            desconto_percentual=50,
            motivo="prazo_esgotado",
        )

    desconto_percentual = min(dias_atraso * 10, 50)
    nota_final = round(nota * (1 - desconto_percentual / 100), 2)
    return ResultadoEntrega(
        aceita=True,
        nota_final=nota_final,
        dias_atraso=dias_atraso,
        desconto_percentual=desconto_percentual,
        motivo="atraso",
    )
