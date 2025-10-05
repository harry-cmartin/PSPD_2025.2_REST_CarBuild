from django.contrib import admin
from .models import Car, Peca, Pedido, ItemPedido

# Configuração do admin para Car
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'ano')
    list_filter = ('ano',)
    search_fields = ('modelo',)
    ordering = ('modelo', 'ano')

# Configuração do admin para Peca
@admin.register(Peca)
class PecaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor', 'owner')
    list_filter = ('owner', 'valor')
    search_fields = ('nome',)
    ordering = ('nome',)

# Inline para ItemPedido dentro de Pedido
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1
    readonly_fields = ('subtotal',)

# Configuração do admin para Pedido
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id_unico', 'valor_total', 'data_pedido')
    list_filter = ('data_pedido',)
    search_fields = ('id_unico',)
    readonly_fields = ('id_unico', 'data_pedido')
    ordering = ('-data_pedido',)
    inlines = [ItemPedidoInline]
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Se está editando um pedido existente
            return self.readonly_fields + ('valor_total',)
        return self.readonly_fields

# Configuração do admin para ItemPedido
@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'peca', 'quantidade', 'subtotal')
    list_filter = ('pedido', 'peca')
    search_fields = ('peca__nome', 'pedido__id_unico')
    readonly_fields = ('subtotal',)
    ordering = ('pedido', 'peca')
