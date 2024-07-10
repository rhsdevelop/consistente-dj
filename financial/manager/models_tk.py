# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Bancos(models.Model):
    datacadastro = models.CharField()
    nomebanco = models.CharField()
    tipomov = models.IntegerField()
    numero = models.CharField(blank=True, null=True)
    diavenc = models.IntegerField(blank=True, null=True)
    gerafatura = models.IntegerField(blank=True, null=True)
    agencia = models.CharField(blank=True, null=True)
    conta = models.CharField(blank=True, null=True)
    tipoconta = models.IntegerField(blank=True, null=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='usuario', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bancos'


class Categorias(models.Model):
    categoria = models.CharField()
    tipomov = models.IntegerField()
    classifica = models.IntegerField()
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='usuario', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categorias'


class Diarios(models.Model):
    datafirstupdate = models.CharField(blank=True, null=True)
    datalastupdate = models.CharField(blank=True, null=True)
    datadoc = models.CharField(blank=True, null=True)
    datavenc = models.CharField(blank=True, null=True)
    datapago = models.CharField(blank=True, null=True)
    parceiro = models.IntegerField()
    banco = models.IntegerField()
    fatura = models.CharField(blank=True, null=True)
    descricao = models.CharField()
    valor = models.FloatField()
    tipomov = models.IntegerField()
    categoriamov = models.IntegerField()
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='usuario', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diario'


class Drive(models.Model):
    arquivo = models.CharField()
    idgoogle = models.CharField()

    class Meta:
        managed = False
        db_table = 'drive'


class Parceiros(models.Model):
    datacadastro = models.CharField()
    nome = models.CharField()
    nomecompleto = models.CharField()
    tipo = models.IntegerField()
    doc = models.CharField(blank=True, null=True)
    endereco = models.CharField(blank=True, null=True)
    telefone = models.CharField(blank=True, null=True)
    observacao = models.CharField(blank=True, null=True)
    modo = models.IntegerField(blank=True, null=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='usuario', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parceiros'


class Usuarios(models.Model):
    nome = models.CharField()
    senha = models.CharField()
    observacao = models.CharField()

    class Meta:
        managed = False
        db_table = 'usuarios'
