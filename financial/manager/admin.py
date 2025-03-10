from django.contrib import admin
from manager import models as consistente

admin.site.register(consistente.ConsistenteCliente)
admin.site.register(consistente.ConsistenteUsuario)
admin.site.register(consistente.Banco)
admin.site.register(consistente.Categoria)
admin.site.register(consistente.Parceiro)
admin.site.register(consistente.Diario)