from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.conf import settings
from manager import models as consistente

class UserSerialazers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
        ]

class ConsistenteClienteSerialazers(serializers.ModelSerializer):
    create_user_serialazer = UserSerialazers(read_only=True, source='create_user')
    assign_user_serialazer = UserSerialazers(read_only=True, source='assign_user')

    class Meta:
        model = consistente.ConsistenteCliente
        fields = [
            'id',
            'nome',
            'fantasia',
            'doc',
            'create_user_serialazer',
            'created',
            'assign_user_serialazer',
            'modified'
        ]

class ConsistenteUsuarioSerialazers(serializers.ModelSerializer):
    create_user_serialazer = UserSerialazers(read_only=True)
    assign_user_serialazer = UserSerialazers(read_only=True)
    consistente_cliente = serializers.PrimaryKeyRelatedField(queryset=consistente.ConsistenteCliente.objects.all(), write_only=True)
    user_serialazer = UserSerialazers(read_only=True, source='user')
    consistente_cliente_serialazer = ConsistenteClienteSerialazers(read_only=True, source='consistente_cliente')

    class Meta:
        model = consistente.ConsistenteUsuario
        fields = [
            'id',
            'consistente_cliente',
            'consistente_cliente_serialazer',
            'user',
            'user_serialazer',
            'is_admin',
            'create_user_serialazer',
            'created',
            'assign_user_serialazer',
            'modified'
        ]


class BancoSerialazers(serializers.ModelSerializer):
    consistente_cliente = ConsistenteClienteSerialazers()
    consistente_cliente_serialazer = ConsistenteClienteSerialazers(read_only=True, source='consistente_cliente')
    create_user_serialazer = UserSerialazers(read_only=True)
    assign_user_serialazer = UserSerialazers(read_only=True)
    allowed_users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False, write_only=True)
    allowed_users_display = UserSerialazers(many=True, read_only=True, source='allowed_users')
    tipomovDisplay_serialazer = serializers.SerializerMethodField()
    tipocontaDisplay_serialazer = serializers.SerializerMethodField()

    class Meta:
        model = consistente.Banco
        fields = [
            'id',
            'consistente_cliente',
            'consistente_cliente_serialazer',
            'datacadastro',
            'nomebanco',
            'tipomov',
            'tipomovDisplay_serialazer',
            'numero',
            'diavenc',
            'gerafatura',
            'agencia',
            'conta',
            'tipoconta',
            'tipocontaDisplay_serialazer',
            'allowed_users',
            'allowed_users_display',
            'create_user_serialazer',
            'created',
            'assign_user_serialazer',
            'modified',
        ]

    def get_tipomovDisplay_serialazer(self, obj):
        return obj.get_tipomov_display()
    
    def get_tipocontaDisplay_serialazer(self, obj):
        return obj.get_tipoconta_display()

    def __init__(self, *args, **kwargs):
        request = kwargs.get('context', {}).get('request', None)
        super().__init__(*args, **kwargs)

        if request and not request.user.is_staff:
            self.fields.pop('consistente_cliente')
    

class CategoriaSerialazers(serializers.ModelSerializer):
    consistente_cliente = ConsistenteClienteSerialazers()
    consistente_cliente_serialazer = ConsistenteClienteSerialazers(read_only=True, source='consistente_cliente')
    create_user_serialazer = UserSerialazers(read_only=True)
    assign_user_serialazer = UserSerialazers(read_only=True)
    tipomovDisplay_serialazer = serializers.SerializerMethodField()

    class Meta:
        model = consistente.Categoria
        fields = [
            'id',
            'consistente_cliente',
            'consistente_cliente_serialazer',
            'categoria',
            'tipomov',
            'tipomovDisplay_serialazer',
            'limitemensal',
            'classifica',
            'create_user_serialazer',
            'created',
            'assign_user_serialazer',
            'modified'
        ]

    def get_tipomovDisplay_serialazer(self, obj):
        return obj.get_tipomov_display()
    
    def __init__(self, *args, **kwargs):
        request = kwargs.get('context', {}).get('request', None)
        super().__init__(*args, **kwargs)

        if request and not request.user.is_staff:
            self.fields.pop('consistente_cliente')

class ParceiroSerialazers(serializers.ModelSerializer):
    consistente_cliente = ConsistenteClienteSerialazers()
    consistente_cliente_serialazer = ConsistenteClienteSerialazers(read_only=True, source='consistente_cliente')
    create_user_serialazer = UserSerialazers(read_only=True)
    assign_user_serialazer = UserSerialazers(read_only=True)
    tipoDisplay_serialazer = serializers.SerializerMethodField()
    modoDisplay_serialazer = serializers.SerializerMethodField()

    class Meta:
        model = consistente.Parceiro
        fields = [
            'id',
            'consistente_cliente',
            'consistente_cliente_serialazer',
            'datacadastro',
            'nome',
            'nomecompleto',
            'tipo',
            'tipoDisplay_serialazer',
            'doc',
            'endereco',
            'cidade',
            'telefone',
            'observacao',
            'modo',
            'modoDisplay_serialazer',
            'create_user_serialazer',
            'created',
            'assign_user_serialazer',
            'modified',
        ]

    def get_tipoDisplay_serialazer(self, obj):
        return obj.get_tipo_display()
    
    def get_modoDisplay_serialazer(self, obj):
        return obj.get_modo_display()
    
    def __init__(self, *args, **kwargs):
        request = kwargs.get('context', {}).get('request', None)
        super().__init__(*args, **kwargs)

        if request and not request.user.is_staff:
            self.fields.pop('consistente_cliente')

class DiarioSerialazers(serializers.ModelSerializer):
    consistente_cliente = ConsistenteClienteSerialazers()
    consistente_cliente_serialazer = ConsistenteClienteSerialazers(read_only=True, source='consistente_cliente')
    create_user_serialazer = UserSerialazers(read_only=True)
    assign_user_serialazer = UserSerialazers(read_only=True)
    parceiro_serialazer = ParceiroSerialazers(read_only = True)
    banco_serialazer = BancoSerialazers(read_only = True)
    categoria_serialazer = CategoriaSerialazers(read_only = True)
    banco = serializers.PrimaryKeyRelatedField(queryset=consistente.Banco.objects.all(), write_only=True)
    categoria = serializers.PrimaryKeyRelatedField(queryset=consistente.Categoria.objects.all(), write_only=True)
    banco_rec = serializers.PrimaryKeyRelatedField(queryset=consistente.Banco.objects.all(), write_only=True, required=True)


    class Meta:
        model = consistente.Diario
        fields = [
            'id',
            'consistente_cliente',
            'consistente_cliente_serialazer',
            'datafirstupdate',
            'datalastupdate',
            'datadoc',
            'datavenc',
            'datapago',
            'parceiro',
            'parceiro_serialazer',
            'banco',
            'banco_serialazer',
            'banco_rec',
            'fatura',
            'descricao',
            'valor',
            'tipomov',
            'categoria',
            'categoria_serialazer',
            'origin_transfer',
            'create_user_serialazer',
            'created',
            'assign_user_serialazer',
            'modified'
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.get('context', {}).get('request', None)
        super().__init__(*args, **kwargs)

        if request and not request.user.is_staff:
            self.fields.pop('consistente_cliente')

    def create(self, validated_data):
        banco_rec = validated_data.pop('banco_rec', None)
        instance = super().create(validated_data)
        instance.banco_rec = banco_rec
        return instance
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        access_lifetime = settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME')
        refresh_lifetime = settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME')
        
        data['access_token_expires_in'] = access_lifetime.total_seconds() if access_lifetime else None
        data['refresh_token_expires_in'] = refresh_lifetime.total_seconds() if refresh_lifetime else None
        return data