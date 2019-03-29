from django.contrib import admin
from .models import Cliente, Tpfilme, Tpadesivo, Acabamento, Filme_bopp, Adesivo, Orcamento_filme, Orcamento_adesivo

admin.site.register(Cliente)
admin.site.register(Tpfilme)
admin.site.register(Tpadesivo)
admin.site.register(Acabamento)
admin.site.register(Filme_bopp)
admin.site.register(Adesivo)
admin.site.register(Orcamento_filme)
admin.site.register(Orcamento_adesivo)
