from rest_framework import serializers

from main.models import Product, Review, OrderItems, Order


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'image')

class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance) # чтобы добавить
        representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
        return representation

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('id', 'author')

    def validate_product(self, product):
        request = self.context.get('request')
        if product.reviews.filter(author=request.user).exists():
            raise serializers.ValidationError('Вы не можете добавить второй отзыв на этот товар')
        return product

    def validate_rating(self, rating):
        if not rating in range(1, 6):
            raise serializers.ValidationError('Рейтинг должен быть от 1 до 5')
        return rating

    def validate(self, attrs):
        request = self.context.get('request')
        attrs['author'] = request.user
        return attrs

class OrderItemsSerializer(serializers.ModelSerializer):
    class Mets:
        model = OrderItems
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemsSerializer(many=True)

    class Meta:
        model = Order
        fields = ('products', 'notes')

    def create(self, validated_data):
        total_sum = 0
        request = self.context.get('request')
        validated_data['user'] = request.user
        validated_data['status'] = 'new'
        validated_data['total_sum'] = 0
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for prod in products:
            total_sum += prod['product'].price * prod['quantity']
            OrderItems.objects.create(order=order, **prod)
        order.total_sum = total_sum
        order.save()
        return order


