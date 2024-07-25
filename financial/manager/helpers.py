from datetime import date, timedelta

from django.db.models import Sum

from .models import Banco, Categoria, Diario, Parceiro


def atualiza_cartao(user, consistente_cliente, fatura, banco, datavenc):
    data = Diario.objects.filter(fatura=fatura, banco=banco, tipomov=3)
    if data:
        fatura_ajusta = data[0]
        novo_valor = round(Diario.objects.filter(banco=banco, fatura=fatura, tipomov=1).aggregate(Sum('valor'))['valor__sum'], 2)
        fatura_ajusta.valor = novo_valor
        fatura_ajusta.save()
        replica = Diario.objects.filter(id=fatura_ajusta.origin_transfer, tipomov=4)
        print(replica)
        replica.update(valor=novo_valor)
    else:
        new_item = {
            'consistente_cliente': consistente_cliente,
            'datadoc': datavenc.replace(day=1),
            'datavenc': datavenc,
            'parceiro': Parceiro.objects.filter(consistente_cliente=consistente_cliente).order_by('id').first(),
            'banco': Banco.objects.filter(consistente_cliente=consistente_cliente).exclude(tipomov=2).order_by('id').first(),
            'fatura': fatura,
            'descricao': '<CRED.CARD>',
            'valor': round(Diario.objects.filter(banco=banco, fatura=fatura, tipomov=1).aggregate(Sum('valor'))['valor__sum'], 2),
            'tipomov': 4,
            'categoria': Categoria.objects.filter(consistente_cliente=consistente_cliente, tipomov=2).order_by('id').first(),
            'create_user': user,
            'assign_user': user,
        }
        data = Diario(**new_item)
        data.save()
        new_item['banco'] = banco
        new_item['tipomov'] = 3
        new_item['origin_transfer'] = data.id
        data = Diario(**new_item)
        data.save()
