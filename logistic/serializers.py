from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        exclude = ['stock']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        exclude = ['products']

    def create(self, validated_data):
        positions = validated_data.pop('positions')

        stock = super().create(validated_data)

        for i in positions:
            i['stock_id'] = stock.id
            StockProduct.objects.create(**i)

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)

        for i in positions:
            i['stock_id'] = stock.id
            i['product_id'] = i['product'].id
            del i['product']
            StockProduct.objects.filter(product_id=i.get('product_id'), stock_id=i.get('stock_id')).update_or_create(
                defaults={
                    'price': i.get('price'),
                    'quantity': i.get('quantity'),
                    'product_id': i.get('product_id'),
                    'stock_id': i.get('stock_id'),
                }
            )

        return stock
