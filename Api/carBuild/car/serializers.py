from rest_framework import serializers
from .models import Car, Peca, Pedido, ItemPedido

class CarSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Car"""
    
    class Meta:
        model = Car
        fields = ['id', 'modelo', 'ano']
        read_only_fields = ['id']

class PecaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Peca"""
    owner_details = CarSerializer(source='owner', read_only=True)
    
    class Meta:
        model = Peca
        fields = ['id', 'nome', 'valor', 'owner', 'owner_details']
        read_only_fields = ['id']

class ItemPedidoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo ItemPedido"""
    peca_details = PecaSerializer(source='peca', read_only=True)
    subtotal = serializers.ReadOnlyField()
    
    class Meta:
        model = ItemPedido
        fields = ['id', 'peca', 'peca_details', 'quantidade', 'subtotal']
        read_only_fields = ['id', 'subtotal']

class PedidoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Pedido"""
    itens = ItemPedidoSerializer(many=True, read_only=True)
    id_unico = serializers.UUIDField(read_only=True)
    data_pedido = serializers.DateTimeField(read_only=True)
    relatorio = serializers.SerializerMethodField()
    
    class Meta:
        model = Pedido
        fields = ['id', 'id_unico', 'valor_total', 'data_pedido', 'itens', 'relatorio']
        read_only_fields = ['id', 'id_unico', 'data_pedido']
    
    def get_relatorio(self, obj):
        """Retorna o relatório do pedido"""
        return obj.gerar_relatorio()

class PedidoCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de pedidos com itens"""
    itens = ItemPedidoSerializer(many=True, write_only=True)
    
    class Meta:
        model = Pedido
        fields = ['valor_total', 'itens']
        read_only_fields = ['valor_total']
    
    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        pedido = Pedido.objects.create(**validated_data)
        
        for item_data in itens_data:
            ItemPedido.objects.create(pedido=pedido, **item_data)
        
        # Recalcular valor total
        pedido.calcular_total()
        return pedido

class PedidoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de pedidos"""
    total_itens = serializers.SerializerMethodField()
    
    class Meta:
        model = Pedido
        fields = ['id', 'id_unico', 'valor_total', 'data_pedido', 'total_itens']
        read_only_fields = ['id', 'id_unico', 'data_pedido', 'valor_total']
    
    def get_total_itens(self, obj):
        """Retorna o número total de itens no pedido"""
        return obj.itens.count()


