from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


TIPO_MOV = [
    (0, 'Dinheiro em mãos'),
    (1, 'Conta bancária'),
    (2, 'Cartão de Crédito'),
    (3, 'Pré pago'),
]

TIPO_CONTA = [
    (0, 'Conta Corrente'),
    (1, 'Poupança'),
    (2, 'CDB/Outras'),
]
TIPO_MOVIMENTO = [
    (0, 'Receita'),
    (1, 'Despesa'),
    (2, 'Transferência'),
]
PESSOA = [
    (0, 'Pessoa Física'),
    (1, 'Pessoa Jurídica'),
]
RELACIONAMENTO = [
    (0, 'Ambos'),
    (1, 'Cliente'),
    (2, 'Fornecedor'),
]

class ConsistenteCliente(models.Model):
    nome = models.CharField(verbose_name='Nome', max_length=40)
    fantasia = models.CharField(verbose_name='Fantasia', max_length=80)
    doc = models.CharField(verbose_name='CNPJ/CPF', max_length=20, blank=True, null=True)
    create_user = models.ForeignKey(User, verbose_name='Criado por', on_delete=models.PROTECT, related_name='cliente_user_create', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    assign_user = models.ForeignKey(User, verbose_name='Modificado por', on_delete=models.PROTECT, related_name='cliente_user_assign', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.fantasia


class ConsistenteUsuario(models.Model):
    consistente_cliente = models.ForeignKey(ConsistenteCliente, verbose_name='Cliente do Consistente', on_delete=models.PROTECT, related_name='consistente_customer')
    user = models.ForeignKey(User, verbose_name='Usuário associado', on_delete=models.PROTECT, related_name='consistente_user')
    is_admin = models.BooleanField()
    create_user = models.ForeignKey(User, verbose_name='Criado por', on_delete=models.PROTECT, related_name='usuario_user_create', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    assign_user = models.ForeignKey(User, verbose_name='Modificado por', on_delete=models.PROTECT, related_name='usuario_user_assign', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.nome


class Banco(models.Model):
    consistente_cliente = models.ForeignKey(ConsistenteCliente, verbose_name='Cliente do Consistente', on_delete=models.PROTECT, related_name='bank_customer')
    datacadastro = models.DateField(verbose_name='Data Cadastro', max_length=10)  # Campo do programa antigo.
    nomebanco = models.CharField(verbose_name='Nome do Banco', max_length=50)
    tipomov = models.IntegerField(verbose_name='Tipo de Banco', choices=TIPO_MOV)
    numero = models.CharField(verbose_name='Número do cartão', max_length=19, blank=True, null=True)
    diavenc = models.IntegerField(verbose_name='Dia vencimento fatura', blank=True, null=True)
    gerafatura = models.BooleanField(verbose_name='Gera fatura?', default=False)
    agencia = models.CharField(verbose_name='Agência', max_length=10, blank=True, null=True)
    conta = models.CharField(verbose_name='Conta', max_length=12, blank=True, null=True)
    tipoconta = models.IntegerField(verbose_name='Modalidade', choices=TIPO_CONTA)
    allowed_users = models.ManyToManyField(User, verbose_name='Usuários autorizados', related_name='bank_user_allowed', blank=True)  # Usuários autorizados a visualizar banco.
    create_user = models.ForeignKey(User, verbose_name='Criado por', on_delete=models.PROTECT, related_name='bank_user_create', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    assign_user = models.ForeignKey(User, verbose_name='Modificado por', on_delete=models.PROTECT, related_name='bank_user_assign', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.nomebanco


class Categoria(models.Model):
    consistente_cliente = models.ForeignKey(ConsistenteCliente, verbose_name='Cliente do Consistente', on_delete=models.PROTECT, related_name='category_customer')
    categoria = models.CharField(verbose_name='Categoria', max_length=50)
    tipomov = models.IntegerField(verbose_name='Tipo de Movimento', choices=TIPO_MOVIMENTO)
    limitemensal = models.DecimalField(verbose_name='Orçamento Mensal', decimal_places=2, max_digits=30, default=Decimal('0.00'))
    classifica = models.BooleanField(verbose_name='Contempla no painel')
    create_user = models.ForeignKey(User, verbose_name='Criado por', on_delete=models.PROTECT, related_name='category_user_create', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    assign_user = models.ForeignKey(User, verbose_name='Modificado por', on_delete=models.PROTECT, related_name='category_user_assign', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.categoria


class Parceiro(models.Model):
    consistente_cliente = models.ForeignKey(ConsistenteCliente, verbose_name='Cliente do Consistente', on_delete=models.PROTECT, related_name='partner_customer')
    datacadastro = models.DateField(verbose_name='Data do Cadastro', max_length=10)  # Campo do programa antigo.
    nome = models.CharField(verbose_name='Nome Curto', max_length=30)
    nomecompleto = models.CharField(verbose_name='Nome Completo', max_length=100)
    tipo = models.IntegerField(verbose_name='Tipo', choices=PESSOA)
    doc = models.CharField(verbose_name='CNPJ/CPF', max_length=30, blank=True, null=True)
    endereco = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=40, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    modo = models.IntegerField(verbose_name='Relacionamento', choices=RELACIONAMENTO)
    create_user = models.ForeignKey(User, verbose_name='Criado por', on_delete=models.PROTECT, related_name='partner_user_create', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    assign_user = models.ForeignKey(User, verbose_name='Modificado por', on_delete=models.PROTECT, related_name='partner_user_assign', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.nome


class Diario(models.Model):
    consistente_cliente = models.ForeignKey(ConsistenteCliente, on_delete=models.PROTECT, related_name='daily_customer')
    datafirstupdate = models.CharField(max_length=10, blank=True, null=True)  # Campo do programa antigo.
    datalastupdate = models.CharField(max_length=10, blank=True, null=True)  # Campo do programa antigo.
    datadoc = models.DateField(verbose_name='Data Evento')
    datavenc = models.DateField(verbose_name='Vencimento')
    datapago = models.DateField(verbose_name='Pagamento', blank=True, null=True)
    parceiro = models.ForeignKey(Parceiro, on_delete=models.PROTECT)
    banco = models.ForeignKey(Banco, on_delete=models.PROTECT)
    fatura = models.CharField(verbose_name='Fatura', max_length=20, blank=True, null=True)
    descricao = models.CharField(verbose_name='Descrição', max_length=100)
    valor = models.DecimalField(verbose_name='Valor', decimal_places=2, max_digits=30)
    # TipoMov INTEGER NOT NULL, ') # 0 para Receita e 1 para Despesa 3 Transf Ent 4 Transf Sai
    tipomov = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    origin_transfer = models.IntegerField(blank=True, null=True) # Campo pra uso interno. Inserir id do tipomov 4 (evento que paga) no tipomov 3 (evento que recebe). Para trasnferências e cartões de crédito.
    create_user = models.ForeignKey(User, verbose_name='Criado por', on_delete=models.PROTECT, related_name='daily_user_create', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    assign_user = models.ForeignKey(User, verbose_name='Modificado por', on_delete=models.PROTECT, related_name='daily_user_assign', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)
