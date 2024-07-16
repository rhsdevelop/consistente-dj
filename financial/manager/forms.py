from calendar import monthrange
from datetime import datetime, date, timedelta

from django import forms
from .models import TIPO_CONTA, TIPO_MOV, TIPO_MOVIMENTO, ConsistenteCliente, ConsistenteUsuario, Banco, Categoria, Parceiro, Diario


class AddClienteForm(forms.ModelForm):
    class Meta:
        model = ConsistenteCliente
        exclude = ['id', 'create_user', 'created', 'assign_user', 'modified']


class FindClienteForm(forms.ModelForm):
    class Meta:
        model = ConsistenteCliente
        exclude = ['id', 'create_user', 'created', 'assign_user', 'modified']


class AddClienteUserForm(forms.ModelForm):
    is_admin = forms.BooleanField(label='Administrador', initial=False, required=False)

    class Meta:
        model = ConsistenteUsuario
        exclude = ['id', 'create_user', 'created', 'assign_user', 'modified']


class FindClienteUserForm(forms.ModelForm):
    class Meta:
        model = ConsistenteUsuario
        exclude = ['id', 'create_user', 'created', 'assign_user', 'modified']


class AddBancoForm(forms.ModelForm):
    datacadastro = forms.DateField(
        label='Data Cadastro',
        widget=forms.widgets.DateInput(
            attrs={'type': "date"},
            format='%Y-%m-%d'
        ),
    )
    tipomov = forms.ChoiceField(label='Tipo de Banco', choices=TIPO_MOV)
    tipoconta = forms.ChoiceField(label='Modalidade', choices=TIPO_CONTA)

    class Meta:
        model = Banco
        exclude = ['id', 'create_user', 'created', 'assign_user', 'modified']


class FindBancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = ['consistente_cliente', 'nomebanco', 'tipomov']


class AddCategoriaForm(forms.ModelForm):
    tipomov = forms.ChoiceField(label='Tipo de Banco', choices=TIPO_MOVIMENTO)

    class Meta:
        model = Categoria
        exclude = ['id', 'create_user', 'created', 'assign_user', 'modified']


class FindCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        exclude = ['id', 'create_user', 'created', 'assign_user', 'modified']


class AddParceiroForm(forms.ModelForm):
    datacadastro = forms.DateField(
        label='Data Cadastro',
        widget=forms.widgets.DateInput(
            attrs={'type': "date"},
            format='%Y-%m-%d'
        ),
    )
    class Meta:
        model = Parceiro
        exclude = ['id', 'create_user', 'created', 'assign_user', 'modified']


class FindParceiroForm(forms.ModelForm):
    class Meta:
        model = Parceiro
        fields = ['consistente_cliente', 'nome', 'nomecompleto', 'tipo', 'doc', 'endereco']


class AddDiarioForm(forms.ModelForm):
    datadoc = forms.DateField(
        label='Data Evento',
        widget=forms.widgets.DateInput(
            attrs={'type': "date"},
            format='%Y-%m-%d'
        ),
    )
    datavenc = forms.DateField(
        label='Vencimento',
        widget=forms.widgets.DateInput(
            attrs={'type': "date"},
            format='%Y-%m-%d'
        ),
    )
    datapago = forms.DateField(
        label='Pagamento',
        widget=forms.widgets.DateInput(
            attrs={'type': "date"},
            format='%Y-%m-%d'
        ),
        required=False,
    )
    parcelas = forms.ChoiceField(choices=[[x, '%sx' % x] for x in range(1, 361)], label='Parcelas', initial=1)
    recorrencia = forms.BooleanField(label='Pagamento recorrente no mes competente.', initial=False, required=False)
    class Meta:
        model = Diario
        exclude = ['id', 'datafirstupdate', 'datalastupdate', 'tipomov', 'origin_transfer', 'create_user', 'created', 'assign_user', 'modified']


class TransfereDiarioForm(forms.ModelForm):
    banco_rec = forms.ModelChoiceField(queryset=Banco.objects.all().order_by('nomebanco'), label='Para banco')
    datadoc = forms.DateField(
        label='Data Evento',
        widget=forms.widgets.DateInput(
            attrs={'type': "date"},
            format='%Y-%m-%d'
        ),
    )
    datavenc = forms.DateField(
        label='Vencimento',
        widget=forms.widgets.DateInput(
            attrs={'type': "date"},
            format='%Y-%m-%d'
        ),
    )
    datapago = forms.DateField(
        label='Pagamento',
        widget=forms.widgets.DateInput(
            attrs={'type': "date"},
            format='%Y-%m-%d'
        ),
        required=False,
    )
    class Meta:
        model = Diario
        fields = ['consistente_cliente', 'datadoc', 'banco', 'descricao', 'valor', 'datavenc', 'datapago']


class FindDiarioForm(forms.Form):
    consistente_cliente = forms.ModelChoiceField(queryset=ConsistenteCliente.objects.all().order_by('fantasia'), required=False, label='Cliente TGI')
    parceiro = forms.ModelMultipleChoiceField(queryset=Parceiro.objects.all().order_by('nome'), required=False, label='Parceiro')
    categoria = forms.ModelMultipleChoiceField(queryset=Categoria.objects.all().order_by('categoria'), required=False, label='Categoria')
    banco = forms.ModelChoiceField(queryset=Banco.objects.all().order_by('nomebanco'), required=False, label='Banco')
    banco_rec = forms.ModelChoiceField(queryset=Banco.objects.all().order_by('nomebanco'), required=False, label='Cartão de Crédito')
    data_inicial = forms.DateField(
        label='Data Inicial',
        widget=forms.widgets.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        initial=str(date.today().replace(day=1)),
        required=False,
    )
    data_final = forms.DateField(
        label='Data Final',
        widget=forms.widgets.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        initial=str(date.today().replace(day=monthrange(date.today().year, date.today().month)[1])),
        required=False,
    )
    venc_inicial = forms.DateField(
        label='Vencimento Inicial',
        widget=forms.widgets.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        required=False,
    )
    venc_final = forms.DateField(
        label='Vencimento Final',
        widget=forms.widgets.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        required=False,
    )
    pag_inicial = forms.DateField(
        label='Pagamento Inicial',
        widget=forms.widgets.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        required=False,
    )
    pag_final = forms.DateField(
        label='Pagamento Final',
        widget=forms.widgets.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        required=False,
    )


class FluxoCaixaForm(forms.Form):
    consistente_cliente = forms.ModelChoiceField(queryset=ConsistenteCliente.objects.all().order_by('fantasia'), required=False, label='Cliente TGI')
    banco = forms.ModelChoiceField(queryset=Banco.objects.all().order_by('nomebanco'), required=False, label='Banco')
    venc_inicial = forms.DateField(
        label='Vencimento Inicial',
        widget=forms.widgets.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        required=False,
    )
    venc_final = forms.DateField(
        label='Vencimento Final',
        widget=forms.widgets.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        required=False,
    )
    somente_aberto = forms.BooleanField(required=False, label='Documentos em aberto (não pagos)')


class ResumoForm(forms.Form):
    consistente_cliente = forms.ModelChoiceField(queryset=ConsistenteCliente.objects.all().order_by('fantasia'), required=False, label='Cliente TGI')
    banco = forms.ModelChoiceField(queryset=Banco.objects.all().order_by('nomebanco'), required=False, label='Banco')
    categoria = forms.ModelMultipleChoiceField(queryset=Categoria.objects.all().order_by('categoria'), required=False, label='Categoria')
    parceiro = forms.ModelMultipleChoiceField(queryset=Parceiro.objects.all().order_by('nome'), required=False, label='Parceiro')
    data_inicial = forms.DateField(
        label='Mês Inicial',
        widget=forms.widgets.DateInput(
            attrs={'type': 'month'},
            format='%Y-%m'
        ),
        required=False,
    )
    data_final = forms.DateField(
        label='Vencimento Final',
        widget=forms.widgets.DateInput(
            attrs={'type': 'month'},
            format='%Y-%m'
        ),
        required=False,
    )
