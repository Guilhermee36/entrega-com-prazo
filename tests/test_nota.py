# Criterios de aceitacao da issue #1, no formato Dado / Quando / Entao.
# Um teste por criterio. Os testes NAO podem ser alterados depois que o codigo existir.
#
# Contrato (da issue): calcular_nota_final(nota, prazo, entrega, justificativa_aprovada, novo_prazo)
#   nota: float de 0 a 10 | prazo, entrega, novo_prazo: datetime (novo_prazo pode ser None)
#   devolve um objeto com os atributos:
#     aceita (bool), nota_final (float, 2 casas), dias_atraso (int),
#     desconto_percentual (int, 0 a 50),
#     motivo (str: "no_prazo" | "justificativa" | "atraso" | "prazo_esgotado")
#   entrada invalida -> ValueError
#
# Em todos os criterios: nota 8,0 e prazo em 10/11/2026 23h59.
#
# RF-001
#   Dado um trabalho com prazo em 10/11/2026 23h59 e nota 8,0, sem justificativa
#   Quando o aluno entrega em 10/11/2026 23h59 (exatamente no limite)
#   Entao a entrega e aceita, com nota final 8,0, 0 dias de atraso, 0% de desconto e motivo "no_prazo"
#
# RF-002
#   Dado um trabalho com prazo em 10/11/2026 23h59 e nota 8,0, sem justificativa
#   Quando o aluno entrega em 11/11/2026 00h00 (1 minuto de atraso)
#   Entao a entrega conta 1 dia de atraso, com 10% de desconto e nota final 7,2
#
# RF-003
#   Dado um trabalho com prazo em 10/11/2026 23h59 e nota 8,0, sem justificativa
#   Quando o aluno entrega em 13/11/2026 00h59 (2 dias e 1 hora de atraso)
#   Entao a entrega conta 3 dias de atraso, com 30% de desconto e nota final 5,6
#
# RF-004
#   Dado um trabalho com prazo em 10/11/2026 23h59 e nota 8,0, sem justificativa
#   Quando o aluno entrega em 15/11/2026 23h59 (exatamente 5 dias de atraso)
#   Entao a entrega e aceita, com 5 dias de atraso, 50% de desconto e nota final 4,0
#
# RF-005
#   Dado um trabalho com prazo em 10/11/2026 23h59 e nota 8,0, sem justificativa
#   Quando o aluno entrega em 16/11/2026 00h00 (5 dias e 1 minuto de atraso)
#   Entao a entrega e recusada (aceita = False), com nota final 0,0 e motivo "prazo_esgotado"
#
# RF-006
#   Dado um trabalho com prazo em 10/11/2026 23h59, nota 8,0, justificativa aprovada
#   e novo prazo em 20/11/2026 23h59
#   Quando o aluno entrega em 18/11/2026 10h00
#   Entao a entrega e aceita, com nota final 8,0, 0% de desconto e motivo "justificativa"
#
# RF-007
#   Dado um trabalho com prazo em 10/11/2026 23h59, nota 8,0, justificativa aprovada
#   e novo prazo em 20/11/2026 23h59
#   Quando o aluno entrega em 21/11/2026 08h00 (8 horas e 1 minuto depois do novo prazo)
#   Entao a entrega conta 1 dia de atraso, com 10% de desconto e nota final 7,2
#
# RF-008
#   Dado um trabalho com prazo em 10/11/2026 23h59, nota 8,0, SEM justificativa aprovada,
#   mas com novo prazo informado em 20/11/2026 23h59
#   Quando o aluno entrega em 12/11/2026 10h00
#   Entao o novo prazo e ignorado: 2 dias de atraso, 20% de desconto e nota final 6,4
#
# RF-009
#   Dado um trabalho com prazo em 10/11/2026 23h59 e nota 8,0, sem justificativa
#   Quando o aluno entrega em 12/11/2026 10h00
#   Entao o resultado traz aceita = True, dias_atraso = 2, desconto_percentual = 20,
#   motivo = "atraso" e nota_final = 6,4
#
# RF-010
#   Dado um trabalho com prazo em 10/11/2026 23h59 e nota 11,0
#   Quando o aluno entrega em 10/11/2026 22h00
#   Entao a funcao lanca ValueError
#
# RF-011
#   Dado um trabalho com prazo em 10/11/2026 23h59, nota 8,0, justificativa aprovada
#   e novo prazo None
#   Quando o aluno entrega em 12/11/2026 10h00
#   Entao a funcao lanca ValueError

from datetime import datetime

import pytest

from src.nota import calcular_nota_final


def test_rf001_entrega_no_limite():
    resultado = calcular_nota_final(
        8.0, datetime(2026, 11, 10, 23, 59), datetime(2026, 11, 10, 23, 59), False, None
    )

    assert resultado.aceita is True
    assert resultado.nota_final == pytest.approx(8.0)
    assert resultado.dias_atraso == 0
    assert resultado.desconto_percentual == 0
    assert resultado.motivo == "no_prazo"


def test_rf002_entrega_um_minuto_atrasada():
    resultado = calcular_nota_final(
        8.0, datetime(2026, 11, 10, 23, 59), datetime(2026, 11, 11, 0, 0), False, None
    )

    assert resultado.dias_atraso == 1
    assert resultado.desconto_percentual == 10
    assert resultado.nota_final == pytest.approx(7.2)


def test_rf003_entrega_com_dois_dias_e_uma_hora_de_atraso():
    resultado = calcular_nota_final(
        8.0, datetime(2026, 11, 10, 23, 59), datetime(2026, 11, 13, 0, 59), False, None
    )

    assert resultado.dias_atraso == 3
    assert resultado.desconto_percentual == 30
    assert resultado.nota_final == pytest.approx(5.6)


def test_rf004_entrega_exatamente_cinco_dias_atrasada():
    resultado = calcular_nota_final(
        8.0, datetime(2026, 11, 10, 23, 59), datetime(2026, 11, 15, 23, 59), False, None
    )

    assert resultado.aceita is True
    assert resultado.dias_atraso == 5
    assert resultado.desconto_percentual == 50
    assert resultado.nota_final == pytest.approx(4.0)


def test_rf005_entrega_apos_o_limite_de_atraso():
    resultado = calcular_nota_final(
        8.0, datetime(2026, 11, 10, 23, 59), datetime(2026, 11, 16, 0, 0), False, None
    )

    assert resultado.aceita is False
    assert resultado.nota_final == pytest.approx(0.0)
    assert resultado.motivo == "prazo_esgotado"


def test_rf006_entrega_dentro_do_novo_prazo_justificado():
    resultado = calcular_nota_final(
        8.0,
        datetime(2026, 11, 10, 23, 59),
        datetime(2026, 11, 18, 10, 0),
        True,
        datetime(2026, 11, 20, 23, 59),
    )

    assert resultado.aceita is True
    assert resultado.nota_final == pytest.approx(8.0)
    assert resultado.desconto_percentual == 0
    assert resultado.motivo == "justificativa"


def test_rf007_entrega_um_dia_apos_o_novo_prazo_justificado():
    resultado = calcular_nota_final(
        8.0,
        datetime(2026, 11, 10, 23, 59),
        datetime(2026, 11, 21, 8, 0),
        True,
        datetime(2026, 11, 20, 23, 59),
    )

    assert resultado.dias_atraso == 1
    assert resultado.desconto_percentual == 10
    assert resultado.nota_final == pytest.approx(7.2)


def test_rf008_novo_prazo_sem_justificativa_e_ignorado():
    resultado = calcular_nota_final(
        8.0,
        datetime(2026, 11, 10, 23, 59),
        datetime(2026, 11, 12, 10, 0),
        False,
        datetime(2026, 11, 20, 23, 59),
    )

    assert resultado.dias_atraso == 2
    assert resultado.desconto_percentual == 20
    assert resultado.nota_final == pytest.approx(6.4)


def test_rf009_entrega_atrasada_retorna_resultado_completo():
    resultado = calcular_nota_final(
        8.0, datetime(2026, 11, 10, 23, 59), datetime(2026, 11, 12, 10, 0), False, None
    )

    assert resultado.aceita is True
    assert resultado.dias_atraso == 2
    assert resultado.desconto_percentual == 20
    assert resultado.motivo == "atraso"
    assert resultado.nota_final == pytest.approx(6.4)


def test_rf010_nota_fora_do_intervalo_lanca_value_error():
    with pytest.raises(ValueError):
        calcular_nota_final(
            11.0, datetime(2026, 11, 10, 23, 59), datetime(2026, 11, 10, 22, 0), False, None
        )


def test_rf011_justificativa_sem_novo_prazo_lanca_value_error():
    with pytest.raises(ValueError):
        calcular_nota_final(
            8.0, datetime(2026, 11, 10, 23, 59), datetime(2026, 11, 12, 10, 0), True, None
        )
