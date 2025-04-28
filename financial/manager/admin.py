from django.contrib import admin
from manager import models as consistente

admin.site.register(consistente.ConsistenteCliente)
admin.site.register(consistente.ConsistenteUsuario)
admin.site.register(consistente.Banco)
admin.site.register(consistente.Categoria)
admin.site.register(consistente.Parceiro)
admin.site.register(consistente.ConsistenteUserCuston)

@admin.register(consistente.Diario)
class DiarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'consistente_cliente', 'parceiro', 'banco', 'descricao', 'tipomov', 'create_user')
    list_filter = ('id', 'consistente_cliente', 'parceiro', 'banco', 'descricao', 'tipomov')
    search_fields = ('id', 'consistente_cliente', 'parceiro', 'banco', 'descricao', 'tipomov')