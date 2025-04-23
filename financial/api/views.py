from django.db.models import Q, Sum
from django.db.models.functions import TruncMonth, TruncDate, TruncDay
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from . import serialazers
from .helpers.pagination import DefaultPagination
from manager import models
from calendar import monthrange
from datetime import date, datetime, timedelta
from decimal import Decimal

class CustonUser(ModelViewSet):
    serializer_class = serialazers.UserSerialazers

    def get_queryset(self):
        return get_user_model().objects.filter(id=self.request.user.id)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serialazers.CustomTokenObtainPairSerializer

class ClienteAPIv1(ModelViewSet):
    queryset = models.ConsistenteCliente.objects.all()
    serializer_class = serialazers.ConsistenteClienteSerialazers
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        filter_seach = Q()
        if not request.user.is_staff:
            crc_user = models.ConsistenteUsuario.objects.filter(user=request.user.id)
            if crc_user:
                filter_seach &= Q(consistente_cliente_id=crc_user.first().consistente_cliente.id)
            else:
                return Response({"error": "Seu usuário não está vinculado a nenhuma conta."},
                                status=status.HTTP_403_FORBIDDEN)
        for key in ['nome', 'fantasia', 'doc']:
            valores = request.GET.getlist(key)
            if valores:
                q_obj = Q()
                for valor in valores:
                    q_obj |= Q(**{f"{key}__icontains": valor})
                filter_seach &= q_obj
        parceiros = models.ConsistenteCliente.objects.filter(filter_seach).order_by('nome')
        serialazer = self.get_serializer(parceiros, many=True)
        return Response(serialazer.data, status=status.HTTP_200_OK)

class ClienteUserAPIv1(ModelViewSet):
    queryset = models.ConsistenteUsuario.objects.all()
    serializer_class = serialazers.ConsistenteUsuarioSerialazers
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        filter_seach = Q()
        if not request.user.is_staff:
            crc_user = models.ConsistenteUsuario.objects.filter(user=request.user.id)
            if crc_user:
                filter_seach &= Q(consistente_cliente_id=crc_user.first().consistente_cliente.id)
            else:
                return Response({"error": "Seu usuário não está vinculado a nenhuma conta."},
                                status=status.HTTP_403_FORBIDDEN)
        for key in ['consistente_cliente', 'user']:
            valores = request.GET.getlist(key)
            if valores:
                q_obj = Q()
                for valor in valores:
                    q_obj |= Q(**{f"{key}__icontains": valor})
                filter_seach &= q_obj
        parceiros = models.ConsistenteUsuario.objects.filter(filter_seach).order_by('nome')
        serialazer = self.get_serializer(parceiros, many=True)
        return Response(serialazer.data, status=status.HTTP_200_OK)

class BancoAPIv1(ModelViewSet):
    queryset = models.Banco.objects.all()
    serializer_class = serialazers.BancoSerialazers
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        crc_user = models.ConsistenteUsuario.objects.filter(user=request.user.id)
        if not request.user.is_staff and not crc_user:
            return Response({"error": "Usuário não tem perfil válido."},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
        consistente_cliente = crc_user.first().consistente_cliente if crc_user else None
        serialazer = serialazers.BancoSerialazers(
            data=request.data, 
            context={
                'request': request,
                'consistente_cliente': consistente_cliente
                })
        if serialazer.is_valid():
            banco = serialazer.save(
                create_user=request.user,
                assign_user=request.user,
                consistente_cliente=consistente_cliente
            )
            if 'allowed_users' in request.data and request.data['allowed_users']:
                for usuariobanco in request.data.get('allowed_users', []):
                    banco.allowed_users.add(usuariobanco)
            return Response({"message": "O banco foi adicionado com sucesso"}, status=status.HTTP_201_CREATED)
        return Response({"error": f"O banco não foi adicionado com sucesso {serialazer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        filter_seach = Q()
        if not request.user.is_staff:
            crc_user = models.ConsistenteUsuario.objects.filter(user=request.user.id)
            if crc_user:
                filter_seach &= Q(consistente_cliente_id=crc_user.first().consistente_cliente.id)
            else:
                return Response({"error": "Seu usuário não está vinculado a nenhuma conta."},
                                status=status.HTTP_403_FORBIDDEN)
        for key in ['consistente_cliente', 'nomebanco', 'tipomov']:
            valores = request.GET.getlist(key)
            if valores:
                q_obj = Q()
                for valor in valores:
                    q_obj |= Q(**{f"{key}__icontains": valor})
                filter_seach &= q_obj
        parceiros = models.Banco.objects.filter(filter_seach).order_by('consistente_cliente')
        serialazer = self.get_serializer(parceiros, many=True)
        return Response(serialazer.data, status=status.HTTP_200_OK)

class CategoriaAPIv1(ModelViewSet):
    queryset = models.Categoria.objects.all()
    serializer_class = serialazers.CategoriaSerialazers
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        crc_user = models.ConsistenteUsuario.objects.filter(user=request.user.id)
        if not request.user.is_staff and not crc_user:
            return Response({"error": "Usuário não tem perfil válido."},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
        consistente_cliente = crc_user.first().consistente_cliente if crc_user else None
        serialazer = serialazers.CategoriaSerialazers(
            data=request.data,
            context={
                'request': request,
                'consistente_cliente':consistente_cliente
            }
        )
        if serialazer.is_valid():
            serialazer.save(
                create_user=request.user,
                assign_user=request.user,
                consistente_cliente=consistente_cliente
            )
            return Response({"message": "A categoria foi adicionada com sucesso"}, status=status.HTTP_201_CREATED)
        return Response({"error": f"A categoria não foi adicionada com sucesso {serialazer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        filter_seach = Q()
        if not request.user.is_staff:
            crc_user = models.ConsistenteUsuario.objects.filter(user=request.user.id)
            if crc_user:
                filter_seach &= Q(consistente_cliente_id=crc_user.first().consistente_cliente.id)
            else:
                return Response({"error": "Seu usuário não está vinculado a nenhuma conta."},
                                status=status.HTTP_403_FORBIDDEN)
        for key in ['consistente_cliente', 'categoria', 'tipomov']:
            valores = request.GET.getlist(key)
            if valores:
                q_obj = Q()
                for valor in valores:
                    q_obj |= Q(**{f"{key}__icontains": valor})
                filter_seach &= q_obj
        parceiros = models.ConsistenteUsuario.objects.filter(filter_seach).order_by('nome')
        serialazer = self.get_serializer(parceiros, many=True)
        return Response(serialazer.data, status=status.HTTP_200_OK)

class ParceiroAPIv1(ModelViewSet):
    queryset = models.Parceiro.objects.all()
    serializer_class = serialazers.ParceiroSerialazers
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        crc_user = models.ConsistenteUsuario.objects.filter(user=request.user.id)
        if not request.user.is_staff and not crc_user:
            return Response({"error": "Usuário não tem perfil válido."},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
        consistente_cliente = crc_user.first().consistente_cliente if crc_user else None
        serialazer = serialazers.ParceiroSerialazers(
            data=request.data,
            context={
                'request': request,
                'consistente_cliente':consistente_cliente
            }
        )
        if serialazer.is_valid():
            serialazer.save(
                create_user=request.user,
                assign_user=request.user,
                consistente_cliente=consistente_cliente
            )
            return Response({"message": "O parceiro foi adicionada com sucesso"}, status=status.HTTP_201_CREATED)
        return Response({"error": f"O parceiro não foi adicionada com sucesso {serialazer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        filter_seach = Q()
        if not request.user.is_staff:
            crc_user = models.ConsistenteUsuario.objects.filter(user=request.user.id)
            if crc_user:
                filter_seach &= Q(consistente_cliente_id=crc_user.first().consistente_cliente.id)
            else:
                return Response({"error": "Seu usuário não está vinculado a nenhuma conta."},
                                status=status.HTTP_403_FORBIDDEN)
        for key in ['nome', 'nomecompleto', 'doc', 'cidade']:
            valores = request.GET.getlist(key)
            if valores:
                q_obj = Q()
                for valor in valores:
                    q_obj |= Q(**{f"{key}__icontains": valor})
                filter_seach &= q_obj
        parceiros = models.Parceiro.objects.filter(filter_seach).order_by('nome')
        serialazer = self.get_serializer(parceiros, many=True)
        return Response(serialazer.data, status=status.HTTP_200_OK)

class ContasAReceberAPIv1(ModelViewSet):
    queryset = models.Diario.objects.filter(tipomov=0)
    serializer_class = serialazers.DiarioSerialazers
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return models.Diario.objects.filter(tipomov=0)
        crc_users = models.ConsistenteUsuario.objects.filter(user=self.request.user).first()
        if not crc_users:
            return models.Diario.objects.none()
        return models.Diario.objects.filter(tipomov=0, consistente_cliente=crc_users.consistente_cliente)
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        crc_user = models.ConsistenteUsuario.objects.filter(user=request.user.id).first()
        if not request.user.is_staff and not crc_user:
            return Response({"error": "Usuário não tem perfil válido."},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
        consistente_cliente_id = crc_user.consistente_cliente.id if crc_user else None

        data['tipomov'] = 0
        data['create_user'] = request.user
        data['assign_user'] = request.user

        serialazer = self.get_serializer(data=data)
        if serialazer.is_valid():
            item = serialazer.save(consistente_cliente_id=consistente_cliente_id)
            parcelas = int(request.data.get('parcelas', 1))
            recorrencia = request.data.get('recorrencia', False)

            if parcelas > 1:
                self._criar_parcelas(item, parcelas, recorrencia)
            return Response(serialazer.data, status=status.HTTP_201_CREATED)
        return Response(serialazer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def duplicar(self, request, pk=None):
        try:
            original = self.get_queryset().get(pk=pk)
        except models.Diario.DoesNotExist:
            return Response({"error": "Registro não encontrato"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_staff:
            consistente_cliente_id = original.consistente_cliente.id
        else:
            crc_user = models.ConsistenteUsuario.objects.filter(user=request.user.id).first()
            if not crc_user:
                return Response({"error": "Seu usuário não está vinculado a nenhuma conta."},
                                status=status.HTTP_403_FORBIDDEN)
            consistente_cliente_id = crc_user.consistente_cliente.id

        data = {
            "descricao": original.descricao + " (Cópia)",
            "valor": original.valor,
            "datadoc": original.datadoc,
            "datavenc": original.datavenc,
            "parceiro": original.parceiro.id,
            "banco": original.banco.id,
            "categoria": original.categoria.id,
            "tipomov": 0,
            "create_user": request.user.id,
            "assign_user": request.user.id,
        }

        parcelas = int(request.data.get("parcelas", 1))
        recorrencia = request.data.get("recorrencia", False)
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            novo_item = serializer.save(consistente_cliente_id=consistente_cliente_id)
            if parcelas > 1:
                self._criar_parcelas(novo_item, parcelas, recorrencia)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_receber(self, request, pk=None):
        diario = self.get_queryset().filter(pk=pk).first()
        if not diario:
            return Response({"error": "Registro não encontrado"}, status=status.HTTP_400_BAD_REQUEST)
        diario.delete()
        return Response({"message": "Registro excluído com sucesso"}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        filter_search = Q()
        if not request.user.is_staff:
            crc_user = models.ConsistenteUsuario.objects.filter(user=request.user.id).first()
            if not crc_user:
                return Response({"error": "Seu usuário não está vinculado a nenhuma conta."},
                                status=status.HTTP_403_FORBIDDEN)
            filter_search &= Q(consistente_cliente_id=crc_user.consistente_cliente.id)

        filtros = {
            'consistente_cliente': 'consistente_cliente_id',
            'banco': 'banco_id',
            'parceiro': 'parceiro_id',
            'categoria': 'categoria_id',
            'data_inicial': 'datadoc__gte',
            'data_final': 'datadoc__lte',
            'venc_inicial': 'datavenc__gte',
            'venc_final': 'datavenc__lte',
            'pag_inicial': 'datapago__gte',
            'pag_final': 'datapago__lte'
        }
        for param, field in filtros.items():
            valor = request.GET.get(param)
            if valor:
                filter_search &= Q(**{field: valor})

        filter_search &= Q(tipomov=0)
        list_receber = models.Diario.objects.filter(filter_search).order_by('datadoc')
        soma = list_receber.aggregate(total=Sum('valor'))['total'] or 0.00
        serialazer = self.get_serializer(list_receber, many=True)

        return Response({
            "soma": round(soma, 2),
            "data": serialazer.data
        }, status=status.HTTP_200_OK)

    def _criar_parcelas(self, item, parcelas, recorrencia):
        origin = models.Diario.objects.filter(id=item.id).values()[0]
        del origin['id']
        origin['datapago'] = None
        datavenc = origin['dataven']
        datadoc = origin['datadoc']
        fatura = origin['fatura']
        for i in range(2, parcelas + 1):
            year, month, day = datavenc.year, datavenc.month + 1, origin['dataven'].day
            if month == 13:
                year += 1
                month = 1
            day = min(day, monthrange(year, month)[1])
            datavenc = datavenc.replace(year=year, month=month, day=day)
            if recorrencia:
                year, month, day = datavenc.year, datavenc.month + 1, origin['dataven'].day
                if month == 13:
                    year += 1
                    month = 1
                day = min(day, monthrange(year, month)[1])
                datavenc = datavenc.replace(year=year, month=month, day=day)
            new_item = origin.copy()
            new_item['datavenc'] = datavenc
            new_item['descricao'] += f"{i}/{parcelas}"
            new_item['origin_transfer'] = item.id
            if fatura:
                new_item['fatura'] = str(datavenc)[:7]
            if recorrencia:
                new_item['datadoc'] = datadoc
            models.Diario.objects.create(**new_item)

class ContasAPagarAPIv1(ModelViewSet):
    queryset = models.Diario.objects.filter(tipomov=1)
    serializer_class = serialazers.DiarioSerialazers
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return models.Diario.objects.filter(tipomov=1)
        crc_users = models.ConsistenteUsuario.objects.filter(user=self.request.user).first()
        if not crc_users:
            return models.Diario.objects.none()
        return models.Diario.objects.filter(tipomov=1, consistente_cliente=crc_users.consistente_cliente)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        crc_user = models.ConsistenteUsuario.objects.filter(user=request.user.id).first()
        if not request.user.is_staff and not crc_user:
            return Response({"error": "Usuário não tem perfil válido."},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
        consistente_cliente_id = crc_user.consistente_cliente.id if crc_user else None

        data['tipomov'] = 1
        data['create_user'] = request.user
        data['assign_user'] = request.user

        banco_id = data.get('banco')
        if not banco_id:
            return Response({"error": "O campo 'banco' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
        
        banco = models.Banco.objects.get(id=banco_id)
        if banco.tipomov == 2 and banco.diavenc:
            if 'fatura' in data and data['fatura']:
                date_ref = data['fatura'].split('-')
                if len(date_ref) == 2:
                    year, month = int(date_ref[0], int(date_ref[1]))
                    day = banco.diavenc
                    data['datavenc'] = datetime(year, month, day).strftime('%Y-%m-%d')
            else:
                hoje = datetime.strptime(data['datadoc'], '%Y-%m-%d') + timedelta(days=10)
                dia, mes, ano = hoje.day, hoje.month, hoje.year
                if banco.diavenc < dia:
                    mes += 1
                    if mes == 13:
                        mes = 1
                        ano += 1
                data['fatura'] = f"{ano}-{str(mes).zfill(2)}"
                data['datavenc'] = date(ano, mes, banco.diavenc).strftime('%Y-%m-%d')

        if banco.tipomov == 2 and data.get('fatura'):
            nomecartao = models.Diario.objects.filter(fatura=data['fatura'], banco=banco, tipomov=3)
            if nomecartao.exists() and nomecartao.first().datapago:
                return Response({"error": "A fatura do cartão já foi paga. Não é possível inserir esse pagamento."},
                                status=status.HTTP_400_BAD_REQUEST)

        serialazer = self.get_serializer(data=data)
        if serialazer.is_valid():
            item = serialazer.save(consistente_cliente_id=consistente_cliente_id)
            parcelas = int(request.data.get('parcelas', 1))
            recorrencia = request.data.get('recorrencia', False)

            if parcelas > 1:
                self._criar_parcelas(item, parcelas, recorrencia)

            if banco.tipomov == 2 and banco.diavenc and data.get('fatura'):
                self._atualiza_cartao(item)

            return Response(serialazer.data, status=status.HTTP_201_CREATED)
        return Response(serialazer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def duplicar(self, request, pk=None):
        try:
            original = self.get_queryset().get(pk=pk)
        except models.Diario.DoesNotExist:
            return Response({"error": "Registro não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_staff:
            consistente_cliente_id = original.consistente_cliente.id
        else:
            crc_user = models.ConsistenteUsuario.objects.filter(user=request.user.id).first()
            if not crc_user:
                return Response({"error": "Seu usuário não está vinculado a nenhuma conta."},
                                status=status.HTTP_403_FORBIDDEN)
            consistente_cliente_id = crc_user.consistente_cliente.id

        data = {
            "descricao": original.descricao + " (Cópia)",
            "valor": original.valor,
            "datadoc": original.datadoc,
            "datavenc": original.datavenc,
            "parceiro": original.parceiro.id,
            "banco": original.banco.id,
            "categoria": original.categoria.id,
            "tipomov": 1,
            "create_user": request.user.id,
            "assign_user": request.user.id,
        }

        parcelas = int(request.data.get("parcelas", 1))
        recorrencia = request.data.get("recorrencia", False)
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            novo_item = serializer.save(consistente_cliente_id=consistente_cliente_id)
            if parcelas > 1:
                self._criar_parcelas(novo_item, parcelas, recorrencia)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_pagar(self, request, pk=None):
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response({"error": "Não é possível excluir uma conta já paga."}, status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response({"message": "Registro apagado com sucesso!"}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
            filter_search = Q()
            if not request.user.is_staff:
                crc_user = models.ConsistenteUsuario.objects.filter(user=request.user.id).first()
                if not crc_user:
                    return Response({"error": "Seu usuário não está vinculado a nenhuma conta."},
                                    status=status.HTTP_403_FORBIDDEN)
                filter_search &= Q(consistente_cliente_id=crc_user.consistente_cliente.id)

            filtros = {
                'consistente_cliente': 'consistente_cliente_id',
                'banco': 'banco_id',
                'parceiro': 'parceiro_id',
                'categoria': 'categoria_id',
                'data_inicial': 'datadoc__gte',
                'data_final': 'datadoc__lte',
                'venc_inicial': 'datavenc__gte',
                'venc_final': 'datavenc__lte',
                'pag_inicial': 'datapago__gte',
                'pag_final': 'datapago__lte'
            }
            for param, field in filtros.items():
                valor = request.GET.get(param)
                if valor:
                    filter_search &= Q(**{field: valor})

            filter_search &= Q(tipomov=1)
            list_receber = models.Diario.objects.filter(filter_search).order_by('datadoc')
            soma = list_receber.aggregate(total=Sum('valor'))['total'] or 0.00
            serialazer = self.get_serializer(list_receber, many=True)

            return Response({
                "soma": round(soma, 2),
                "data": serialazer.data
            }, status=status.HTTP_200_OK)

    def _criar_parcelas(self, item, parcelas, recorrencia):
        origin = models.Diario.objects.filter(id=item.id).values()[0]
        del origin['id']
        origin['datapago'] = None
        datavenc = origin['datavenc']
        datadoc = origin['datadoc']
        fatura = origin['fatura']
        for i in range(2, parcelas + 1):
            year, month, day = datavenc.year, datavenc.month + 1, origin['datavenc'].day
            if month == 13:
                year += 1
                month = 1
            day = min(day, monthrange(year, month)[1])
            datavenc = datavenc.replace(year=year, month=month, day=day)
            if recorrencia:
                year, month, day = datavenc.year, datavenc.month + 1, origin['dataven'].day
                if month == 13:
                    year += 1
                    month = 1
                day = min(day, monthrange(year, month)[1])
                datavenc = datavenc.replace(year=year, month=month, day=day)
            new_item = origin.copy()
            new_item['datavenc'] = datavenc
            new_item['descricao'] += f"{i}/{parcelas}"
            new_item['origin_transfer'] = item.id
            if fatura:
                new_item['fatura'] = str(datavenc)[:7]
            if recorrencia:
                new_item['datadoc'] = datadoc
            models.Diario.objects.create(**new_item)

    def _atualiza_cartao(self, item):
        banco = item.banco
        models.Diario.objects.filter(fatura=item.fatura, banco=banco, tipomov=1).update(datapago=item.datapago)

class TransfirirAPIv1(ModelViewSet):
    queryset = models.Diario.objects.filter(tipomov__in=[3,4])
    serializer_class = serialazers.DiarioSerialazers
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return models.Diario.objects.filter(tipomov__in=[3,4])
        crc_users = models.ConsistenteUsuario.objects.filter(user=self.request.user).first()
        if not crc_users:
            return models.Diario.objects.none()
        return models.Diario.objects.filter(tipomov__in=[3,4], consistente_cliente=crc_users.consistente_cliente)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        crc_user = models.ConsistenteUsuario.objects.filter(user=request.user.id).first()
        if not request.user.is_staff and not crc_user:
            return Response({"error": "Usuário não tem perfil válido."},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
        consistente_cliente_id = crc_user.consistente_cliente.id if crc_user else None

        parceiro = models.Parceiro.objects.filter(consistente_cliente_id=consistente_cliente_id).order_by('id').first()
        categoria = models.Categoria.objects.filter(consistente_cliente_id=consistente_cliente_id, tipomov=2).order_by('id').first()
        banco_sai = models.Banco.objects.filter(id=data.get("banco")).first()
        banco_rec = models.Banco.objects.filter(id=data.get("banco_rec")).first()
        
        if not banco_rec or not banco_sai:
            return Response({"error": "Banco destinatário ou sainte não encontrado."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not parceiro or not categoria:
            return Response({"error": "Parceiro ou categoria não encontrados para esta conta."}, status=status.HTTP_400_BAD_REQUEST)

        try:    
            sainte = models.Diario.objects.create(
            consistente_cliente_id=consistente_cliente_id,
            datadoc=data.get("datadoc"),
            datavenc=data.get("datavenc"),
            descricao=data.get("descricao"),
            valor=data.get("valor"),
            banco=banco_sai,  # Banco de origem
            parceiro=parceiro,
            categoria=categoria,
            tipomov=4,  # Indica saída de dinheiro
            create_user=request.user,
            assign_user=request.user,
            )

        
            entrante = models.Diario.objects.create(
                consistente_cliente_id=consistente_cliente_id,
                datadoc=sainte.datadoc,
                datavenc=sainte.datavenc,
                descricao=sainte.descricao,
                valor=sainte.valor,
                banco=banco_rec,
                parceiro=parceiro,
                categoria=categoria,
                tipomov=3,
                origin_transfer=sainte.id,
                create_user=request.user,
                assign_user=request.user,
            )
            return Response({
                "transferencia": serialazers.DiarioSerialazers(sainte).data,
                "entrada": serialazers.DiarioSerialazers(entrante).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(f'erro: {str(e)}', status=status.HTTP_400_BAD_REQUEST)

    def delete_transferir(self, request, pk=None):
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response({"error": "Não é possível excluir uma conta já paga."}, status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response({"message": "Registro apagado com sucesso!"}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        filter_search = Q(tipomov=4)

        if not request.user.is_staff:
            crc_user = models.ConsistenteUsuario.objects.filter(user=request.user.id).first()
            if not crc_user:
                return Response({"error": "Seu usuário não está vinculado a nenhuma conta."},
                                status=status.HTTP_403_FORBIDDEN)
            filter_search &= Q(consistente_cliente_id=crc_user.consistente_cliente.id)

        filtros = {
            'consistente_cliente': 'consistente_cliente_id',
            'banco': 'banco_id',
            'parceiro': 'parceiro_id',
            'categoria': 'categoria_id',
            'data_inicial': 'datadoc__gte',
            'data_final': 'datadoc__lte',
            'venc_inicial': 'datavenc__gte',
            'venc_final': 'datavenc__lte',
            'pag_inicial': 'datapago__gte',
            'pag_final': 'datapago__lte'
        }

        for param, field in filtros.items():
            valor = request.GET.get(param)
            if valor:
                filter_search &= Q(**{field: valor})

        filter_search &= ~Q(descricao="<CRED.CARD>")
        list_transferencias = models.Diario.objects.filter(filter_search).order_by('datadoc')
        soma = list_transferencias.aggregate(total=Sum('valor'))['total'] or 0.00
        serializer = self.get_serializer(list_transferencias, many=True)

        return Response({
            "soma": round(soma, 2),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class CartoesAPIv1(ModelViewSet):
    queryset = models.Diario.objects.all()
    serializer_class = serialazers.DiarioSerialazers
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        filter_search = Q()
        if not self.request.user.is_staff:
            crc_user = models.ConsistenteUsuario.objects.filter(user=self.request.user).first()
            if crc_user:
                filter_search &= Q(consistente_cliente_id=crc_user.consistente_cliente_id)
            else:
                return models.Diario.objects.none()
        return models.Diario.objects.filter(filter_search).order_by('datadoc')

    def update(self, request, *args, **kwargs):
        try:
            diario_id = kwargs.get('pk')
            cartao = models.Diario.objects.get(id=diario_id)
            if not request.user.is_staff:
                crc_user = models.ConsistenteUsuario.objects.filter(user=request.user).first()
                if crc_user:
                    if cartao.consistente_cliente_id != crc_user.consistente_cliente_id:
                        return Response({"error": "Você não tem permissão para editar este cartão."},
                                        status=status.HTTP_403_FORBIDDEN)
            serializer = serialazers.DiarioSerialazers(cartao, data=request.data, partial=True)
            if serializer.is_valid():
                updated_cartao = serializer.save(assign_user=request.user)
                if 'datapago' in request.data:
                    cartao_rec = models.Diario.objects.get(origin_transfer=diario_id)
                    cartao_rec.datapago = request.data.get('datapago', None)
                    cartao_rec.save()

                    cartao.datapago = cartao_rec.datapago
                    cartao.save()

                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Erro na validação dos dados."}, status=status.HTTP_400_BAD_REQUEST)

        except models.Diario.DoesNotExist:
            return Response({"error": "Cartão de crédito não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        filter_search = Q(descricao='<CRED.CARD>')
        filter_customer = {}

        if not request.user.is_staff:
            crc_user = models.ConsistenteUsuario.objects.filter(user=request.user).first()
            if crc_user:
                filter_customer['consistente_cliente_id'] = crc_user.consistente_cliente_id
            else:
                return Response(
                    {'detail': 'Seu usuário não está vinculado a nenhuma conta Consistente.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        banco_rec = request.GET.get('banco_rec')
        if banco_rec:
            filter_search &= Q(banco_id=banco_rec, tipomov=3)

        data_inicial = request.GET.get('data_inicial')
        data_final = request.GET.get('data_final')
        if data_inicial:
            filter_search &= Q(datadoc__gte=data_inicial)
        if data_final:
            filter_search &= Q(datadoc__lte=data_final)

        for key, value in request.GET.items():
            if key in ['consistente_cliente', 'banco'] and value:
                filter_search &= Q(**{key: value})
            elif key in ['venc_inicial', 'venc_final', 'pag_inicial', 'pag_final'] and value:
                chave = {
                    'venc_inicial': 'datavenc',
                    'pag_inicial': 'datapago',
                    'venc_final': 'datavenc',
                    'pag_final': 'datapago',
                }
                if key in chave:
                    filter_search &= Q(**{f"{chave[key]}__gte" if 'inicial' in key else f"{chave[key]}__lte": value})

        list_cartoes = models.Diario.objects.filter(filter_search).filter(**filter_customer).order_by('datadoc')

        if not list_cartoes.exists():
            return Response({'detail': 'Nenhum cartão encontrado para os filtros aplicados.'},
                            status=status.HTTP_404_NOT_FOUND)

        data = []
        for cartao in list_cartoes:
            new_item = {
                'id': cartao.id,
                'datadoc': cartao.datadoc,
                'banco': cartao.banco.nomebanco if cartao.banco else None,
                'descricao': cartao.descricao,
                'valor': str(cartao.valor),
                'datavenc': cartao.datavenc,
                'datapago': cartao.datapago,
            }
            data.append(new_item)

        soma = str(sum([Decimal(c['valor']) for c in data]))
        data = {
            'list_cartoes': data,
            'soma': soma,
        }
        return Response(data, status=status.HTTP_200_OK)

class FluxoCaixaAPIv1(ModelViewSet):
    queryset = models.Diario.objects.all()
    serializer_class = serialazers.DiarioSerialazers
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        filter_customer = {}
        filter_search = {}
        filter_initial = {}
        list_diario = []

        if not request.user.is_staff:
            crc_user = models.ConsistenteUsuario.objects.filter(user=request.user)
            if crc_user.exists():
                filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
            else:
                return Response(
                    {'detail': 'Seu usuário não está vinculado a nenhuma conta Consistente.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        if request.query_params:
            banco_id = request.query_params.get('banco')
            if banco_id:
                filter_search['banco'] = banco_id
                filter_initial['banco'] = banco_id

            venc_inicial = request.query_params.get('venc_inicial')
            venc_final = request.query_params.get('venc_final')
            if venc_inicial:
                filter_search['datavenc__gte'] = venc_inicial
                filter_initial['datavenc__lt'] = venc_inicial
            if venc_final:
                filter_search['datavenc__lte'] = venc_final
            if not banco_id:
                filter_search['banco__tipomov__in'] = [0, 1]
                filter_initial['banco__tipomov__in'] = [0, 1]

            filter_initial['tipomov__in'] = [0, 3]
            soma_entradas = models.Diario.objects.filter(**filter_customer).filter(**filter_initial)
            filter_initial['tipomov__in'] = [1, 4]
            soma_saidas = models.Diario.objects.filter(**filter_customer).filter(**filter_initial)

            soma_entradas = soma_entradas.aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')
            soma_saidas = soma_saidas.aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')

            saldo_inicial = round(soma_entradas - soma_saidas, 2)

            new_item = {
                'banco': '',
                'parceiro': '',
                'categoria': '',
                'valor_entra': '',
                'valor_sai': '',
                'valor_saldo': saldo_inicial,
                'datavenc': '',
                'datapago': '',
            }
            list_diario.append(new_item)
            saldo_atual = saldo_inicial
            soma_entradas = Decimal('0.0')
            soma_saidas = Decimal('0.0')

            diario_pagos = (models.Diario.objects
                            .filter(**filter_customer)
                            .filter(**filter_search)
                            .exclude(datapago=None)
                            .order_by('datapago', 'datavenc'))

            for i in diario_pagos:
                valor_entra = Decimal('0.00') if i.tipomov in [1, 4] else i.valor
                valor_sai = Decimal('0.00') if i.tipomov in [0, 3] else i.valor

                soma_entradas += valor_entra
                soma_saidas += valor_sai
                saldo_atual += (valor_entra - valor_sai)

                nomecartao = None
                if i.tipomov == 4:
                    transf = models.Diario.objects.filter(origin_transfer=i.id).first()
                    nomecartao = transf.banco.nomebanco if transf else None
                if i.tipomov == 3:
                    transf = models.Diario.objects.filter(id=i.origin_transfer).first()
                    nomecartao = transf.banco.nomebanco if transf else None

                new_item = {
                    'id': i.id,
                    'banco': str(i.banco.nomebanco) if i.banco else None,
                    'parceiro': str(i.parceiro) if not nomecartao else nomecartao,
                    'categoria': str(i.categoria) if i.descricao != '<CRED.CARD>' else 'Cartão de Crédito',
                    'valor_entra': str(valor_entra) if valor_entra else '',
                    'valor_sai': str(valor_sai) if valor_sai else '',
                    'valor_saldo': str(saldo_atual),
                    'datavenc': i.datavenc,
                    'datapago': i.datapago,
                }

                if 'somente_aberto' in request.query_params:
                    continue

                list_diario.append(new_item)

            if 'somente_aberto' in request.query_params:
                list_diario[0]['valor_saldo'] = str(saldo_atual)

            diario_abertos = (models.Diario.objects
                            .filter(**filter_customer)
                            .filter(**filter_search)
                            .filter(datapago=None)
                            .order_by('datapago', 'datavenc'))
            for i in diario_abertos:
                valor_entra = Decimal('0.00') if i.tipomov in [1, 4] else i.valor
                valor_sai = Decimal('0.00') if i.tipomov in [0, 3] else i.valor

                soma_entradas += valor_entra
                soma_saidas += valor_sai
                saldo_atual += (valor_entra - valor_sai)

                nomecartao = None
                if i.tipomov in (3, 4) and i.descricao == '<CRED.CARD>':
                    transf = models.Diario.objects.filter(
                        origin_transfer=i.id if i.tipomov == 4 else None,
                        id=i.origin_transfer if i.tipomov == 3 else None
                    ).first()
                    if transf and transf.banco:
                        nomecartao = transf.banco.nomebanco

                new_item = {
                    'id': i.id,
                    'banco': str(i.banco.nomebanco) if i.banco else None,
                    'parceiro': str(i.parceiro) if i.descricao != '<CRED.CARD>' else nomecartao,
                    'categoria': (str(i.categoria) if i.descricao != '<CRED.CARD>'
                                else 'Cartão de Crédito'),
                    'valor_entra': str(valor_entra) if valor_entra else '',
                    'valor_sai': str(valor_sai) if valor_sai else '',
                    'valor_saldo': str(saldo_atual),
                    'datavenc': i.datavenc,
                    'datapago': i.datapago,
                }
                list_diario.append(new_item)

            retorno = {
                'lista': list_diario,
                'soma_entradas': str(soma_entradas),
                'soma_saidas': str(soma_saidas),
                'confronto': str(soma_entradas - soma_saidas),
                'saldo_fim': str(saldo_atual),
            }
            return Response(retorno, status=status.HTTP_200_OK)

        else:
            data_inicial = str(date.today().replace(day=1))
            data_final = str(date.today().replace(day=monthrange(date.today().year, date.today().month)[1]))

            retorno = {
                'mensagem': 'Nenhum parâmetro informado.',
                'periodo_inicial': data_inicial,
                'periodo_final': data_final,
                'lista': []
            }
            return Response(retorno, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['post'])
    def pagar(self, request, pk=None):
        diario = get_object_or_404(models.Diario, pk=pk, datapago=None)
        if diario.tipomov in [0, 1] and diario.banco.tipomov != 2:
            diario.datapago = date.today()
            diario.save()
            return Response(
                {"detail": "Pagamento confirmado com sucesso!"},
                status=status.HTTP_200_OK
            )
        elif diario.tipomov in [0, 1] and diario.banco.tipomov == 2:
            return Response(
                {"detail": "Não é possível fazer pagamento individual de compra de cartão de crédito. Realize o pagamento do cartão."},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif diario.tipomov == 3 and diario.banco.tipomov == 2:
            models.Diario.objects.filter(
                fatura=diario.fatura,
                banco=diario.banco,
                tipomov=1,
            ).update(datapago=date.today())
            nomecartao = models.Diario.objects.filter(origin_transfer=diario.id).first()
            if nomecartao:
                nomecartao.datapago = date.today()
                nomecartao.save()
            diario.datapago = date.today()
            diario.save()
            return Response({"detail": "Pagamento confirmado com sucesso!"}, status=status.HTTP_200_OK)
        elif diario.tipomov == 4 and diario.descricao == '<CRED.CARD>':
            nomecartao = models.Diario.objects.filter(origin_transfer=diario.id, tipomov=3).first()
            if nomecartao:
                models.Diario.objects.filter(
                    fatura=nomecartao.fatura,
                    banco=nomecartao.banco,
                    tipomov=1
                ).update(datapago=date.today())

                nomecartao.datapago = date.today()
                nomecartao.save()

            diario.datapago = date.today()
            diario.save()
            return Response({"detail": "Pagamento confirmado com sucesso!"}, status=status.HTTP_200_OK)
        elif diario.tipomov == 3 and diario.banco.tipomov != 2:
            transf = models.Diario.objects.filter(id=diario.origin_transfer, tipomov=4).first()
            if transf:
                transf.datapago = date.today()
                transf.save()
            diario.datapago = date.today()
            diario.save()
            return Response({"detail": "Pagamento confirmado com sucesso!"}, status=status.HTTP_200_OK)
        elif diario.tipomov == 4 and diario.descricao != '<CRED.CARD>':
            transf = models.Diario.objects.filter(origin_transfer=diario.id, tipomov=3).first()
            if transf:
                transf.datapago = date.today()
                transf.save()
            diario.datapago = date.today()
            diario.save()
            return Response({"detail": "Pagamento confirmado com sucesso!"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "Não foi possível confirmar esse documento. Favor, verificar se já está pago ou se tipomov está correto."},
                status=status.HTTP_400_BAD_REQUEST
            )

class ResumoDiarioAPIv1(ModelViewSet):
    queryset = models.Diario.objects.none()
    serializer_class = serialazers.DiarioSerialazers
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        filter_customer = {}
        filter_search = {}

        if not request.user.is_staff:
            crc_user = models.ConsistenteUsuario.objects.filter(user=request.user).first()
            if crc_user:
                filter_customer['consistente_cliente_id'] = crc_user.consistente_cliente_id
            else:
                return Response({
                    'detail': 'Seu usuário não está vinculado a nenhuma conta Consistente.'
                }, status=status.HTTP_403_FORBIDDEN)

        query_params = request.query_params
        data_inicial_param = query_params.get('data_inicial')
        categoria_param = query_params.getlist('categoria')

        if data_inicial_param:
            try:
                ano, mes = data_inicial_param.split('-')
                ano = int(ano)
                mes = int(mes)
                dia_final = monthrange(ano, mes)[1]
                data_inicial = f"{data_inicial_param}-01"
                data_final = f"{data_inicial_param}-{dia_final}"
                filter_search['datadoc__range'] = [data_inicial, data_final]
            except (ValueError, IndexError):
                return Response({
                    'detail': 'Parâmetro data_inicial inválido. Use YYYY-MM.'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            hoje = date.today()
            dia_final = monthrange(hoje.year, hoje.month)[1]
            data_inicial = date(hoje.year, hoje.month, 1)
            data_final = date(hoje.year, hoje.month, dia_final)
            filter_search['datadoc__range'] = [data_inicial, data_final]

        if categoria_param:
            filter_search['categoria__in'] = categoria_param

        filter_search['categoria__classifica'] = True
        filter_search['tipomov__in'] = [1, 4]
        filter_categoria = filter_customer.copy()
        filter_categoria['tipomov'] = 1
        filter_categoria['classifica'] = True
        if categoria_param:
            filter_categoria['id__in'] = categoria_param

        limites = models.Categoria.objects.filter(**filter_categoria).aggregate(Sum('limitemensal'))
        limite = limites['limitemensal__sum'] or Decimal('0.00')
        limite = round(limite, 2)

        diario_qs = (models.Diario.objects
                    .annotate(data=TruncDay('datadoc'))
                    .filter(**filter_customer)
                    .filter(**filter_search)
                    .values('data')
                    .annotate(valor=Sum('valor'))
                    .order_by('data'))
        
        list_diario = []
        acumulado = Decimal('0.00')
        saldo = Decimal(str(limite))

        for row in diario_qs:
            data_diario = row['data']
            valor_diario = row['valor'] or Decimal('0.00')
            valor_diario = round(valor_diario, 2)

            acumulado += valor_diario
            saldo -= valor_diario

            new_item = {
                'data': data_diario,
                'valor': str(valor_diario),
                'valor_acum': str(acumulado),
                'valor_disp': str(saldo),
            }
            list_diario.append(new_item)

        retorno = {
            'list_diario': list_diario,
            'limite': str(limite),
            'acumulado': str(acumulado),
            'saldo': str(saldo),
        }
        return Response(retorno, status=status.HTTP_200_OK)

class ResumoCategoriaAPIv1(ModelViewSet):
    queryset = models.Diario.objects.none()
    serializer_class = serialazers.DiarioSerialazers
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        filter_customer = {}
        filter_search = {}
        filter_initial = {}
        soma_meses = {}
        list_diario = []

        if not request.user.is_staff:
            crc_user = models.ConsistenteUsuario.objects.filter(user=request.user).first()
            if crc_user:
                filter_customer['consistente_cliente_id'] = crc_user.consistente_cliente_id
            else:
                return Response(
                    {'detail': 'Seu usuário não está vinculado a nenhuma conta Consistente.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        query_params = request.query_params
        data_inicial_str = query_params.get('data_inicial')
        data_final_str = query_params.get('data_final')
        banco_id = query_params.get('banco')

        if banco_id:
            filter_search['banco'] = banco_id
            filter_initial['banco'] = banco_id

        if data_inicial_str:
            filter_search['datadoc__gte'] = f"{data_inicial_str}-01"
            filter_initial['datadoc__lt'] = f"{data_inicial_str}-01"

        if data_final_str:
            ano, mes = data_final_str.split('-')
            ano, mes = int(ano), int(mes)
            ultimo_dia = monthrange(ano, mes)[1]
            filter_search['datadoc__lte'] = f"{data_final_str}-{ultimo_dia}"

        filter_initial['tipomov__in'] = [0, 3]
        soma_entradas_qs = models.Diario.objects.filter(**filter_customer).filter(**filter_initial)

        filter_initial['tipomov__in'] = [1, 4]
        soma_saidas_qs = models.Diario.objects.filter(**filter_customer).filter(**filter_initial)

        soma_entradas = soma_entradas_qs.aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')
        soma_saidas = soma_saidas_qs.aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')
        saldo_inicial = round(soma_entradas - soma_saidas, 2)

        saldo_atual = saldo_inicial
        soma_entradas = Decimal('0.00')
        soma_saidas = Decimal('0.00')

        filter_search['tipomov__in'] = [1, 4]
        filter_search['categoria__classifica'] = True

        qs_meses = (models.Diario.objects
                    .filter(**filter_customer)
                    .filter(**filter_search)
                    .annotate(mes=TruncMonth('datadoc'))
                    .values('mes')
                    .annotate(Sum('valor'))
                    .order_by('mes'))

        meses_dict = {str(x['mes'])[:7]: Decimal('0.00') for x in qs_meses}
        soma_meses = meses_dict.copy()

        qs_diario = (models.Diario.objects
                    .filter(**filter_customer)
                    .filter(**filter_search)
                    .annotate(mes=TruncMonth('datadoc'))
                    .values_list('categoria__categoria', 'mes')
                    .annotate(Sum('valor'))
                    .order_by('categoria__categoria', 'mes'))

        new_item = {'categoria': ''}
        primeiro = True

        for i in qs_diario:
            cat_nome = i[0]
            mes_data = i[1]
            valor_sum = i[2] or Decimal('0.00')
            valor_sum = round(valor_sum, 2)

            if cat_nome != new_item['categoria']:
                if not primeiro:
                    list_diario.append(new_item)
                else:
                    primeiro = False
                new_item = {
                    'categoria': cat_nome,
                    'meses': meses_dict.copy()
                }
            mes_str = str(mes_data)[:7]
            new_item['meses'][mes_str] = valor_sum
            soma_meses[mes_str] += valor_sum

        if not primeiro:
            list_diario.append(new_item)
        response_data = {
            'saldo_inicial': str(saldo_inicial),
            'list_diario': list_diario,
            'soma_meses': {k: str(v) for k, v in soma_meses.items()},
        }
        return Response(response_data, status=status.HTTP_200_OK)

class ResumoParceiroAPIv1(ModelViewSet):
    queryset = models.Diario.objects.none()
    serializer_class = serialazers.DiarioSerialazers
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        filter_customer = {}
        filter_search = {}
        filter_initial = {}
        list_diario = []

        if not request.user.is_staff:
            crc_user = models.ConsistenteUsuario.objects.filter(user=request.user).first()
            if crc_user:
                filter_customer['consistente_cliente_id'] = crc_user.consistente_cliente_id
            else:
                return Response(
                    {'detail': 'Seu usuário não está vinculado a nenhuma conta Consistente.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        query_params = request.query_params
        data_inicial_str = query_params.get('data_inicial')
        data_final_str = query_params.get('data_final')
        banco_id = query_params.get('banco')

        if banco_id:
            filter_search['banco'] = banco_id
            filter_initial['banco'] = banco_id

        if data_inicial_str:
            filter_search['datadoc__gte'] = f"{data_inicial_str}-01"
            filter_initial['datadoc__lt'] = f"{data_inicial_str}-01"

        if data_final_str:
            try:
                ano, mes = data_final_str.split('-')
                ano, mes = int(ano), int(mes)
                ultimo_dia = monthrange(ano, mes)[1]
                filter_search['datadoc__lte'] = f"{data_final_str}-{ultimo_dia}"
            except (ValueError, IndexError):
                return Response(
                    {'detail': 'Formato inválido para data_final (use YYYY-MM).'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        filter_initial['tipomov__in'] = [0, 3]
        soma_entradas_qs = models.Diario.objects.filter(**filter_customer).filter(**filter_initial)
        filter_initial['tipomov__in'] = [1, 4]
        soma_saidas_qs = models.Diario.objects.filter(**filter_customer).filter(**filter_initial)
        soma_entradas = soma_entradas_qs.aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')
        soma_saidas = soma_saidas_qs.aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')
        saldo_inicial = round(soma_entradas - soma_saidas, 2)

        saldo_atual = saldo_inicial

        filter_search['tipomov__in'] = [1, 4]
        filter_search['categoria__classifica'] = True

        qs_meses = (models.Diario.objects
                    .filter(**filter_customer)
                    .filter(**filter_search)
                    .annotate(mes=TruncMonth('datadoc'))
                    .values('mes')
                    .annotate(Sum('valor'))
                    .order_by('mes'))
        meses_dict = {str(x['mes'])[:7]: Decimal('0.00') for x in qs_meses}

        diario_qs = (models.Diario.objects
                    .filter(**filter_customer)
                    .filter(**filter_search)
                    .annotate(mes=TruncMonth('datadoc'))
                    .values_list('parceiro__nome', 'mes')
                    .annotate(Sum('valor'))
                    .order_by('parceiro__nome', 'mes'))

        new_item = {'parceiro': ''}
        primeiro = True
        for row in diario_qs:
            parceiro_nome = row[0] or ''
            data_mes = str(row[1])[:7]
            valor_sum = row[2] or Decimal('0.00')
            valor_sum = round(valor_sum, 2)

            if parceiro_nome != new_item['parceiro']:
                if not primeiro:
                    list_diario.append(new_item)
                else:
                    primeiro = False

                new_item = {
                    'parceiro': parceiro_nome,
                    'meses': meses_dict.copy()
                }

            new_item['meses'][data_mes] = valor_sum

        if not primeiro:
            list_diario.append(new_item)

        response_data = {
            'saldo_inicial': str(saldo_inicial),
            'list_diario': list_diario,
        }
        return Response(response_data, status=status.HTTP_200_OK)