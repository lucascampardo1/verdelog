from django.contrib import admin

from .models import Carga


@admin.register(Carga)
class CargaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'cliente', 'origem', 'destino', 'data_coleta', 'status')
    list_filter = ('status', 'data_coleta')
    search_fields = ('codigo', 'cliente', 'descricao', 'origem', 'destino')
