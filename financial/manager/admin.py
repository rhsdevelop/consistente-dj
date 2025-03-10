from django.contrib import admin
from manager import models as consistente

admin.site.register(consistente.ConsistenteCliente)
admin.site.register(consistente.ConsistenteUsuario)
admin.site.register(consistente.Banco)
admin.site.register(consistente.Categoria)
admin.site.register(consistente.Parceiro)
<<<<<<< HEAD
admin.site.register(consistente.Diario)
admin.site.register(consistente.ConsistenteUserCuston)
=======
admin.site.register(consistente.Diario)
>>>>>>> 65ab2d5 (Implementação da estrutura inicial da API financeira com modelos, rotas e configuração de autenticação JWT.)
