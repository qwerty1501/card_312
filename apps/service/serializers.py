from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.users.models import Partners, User
from apps.categories.models import Service_category

from apps.service.models import ProductImage, Characteristic, Product, AdditionalInformation, Promotion, PromotionType


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partners
        fields = '__all__'


class CharacteristicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = '__all__'


class ProductImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class AdditionalInformationListSerializer(serializers.ModelSerializer):
    characteristic = CharacteristicListSerializer(many=True)

    class Meta:
        model = AdditionalInformation
        fields = '__all__'


class ParentCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_category
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):
    parent = ParentCategoryListSerializer()

    class Meta:
        model = Service_category
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    images = ProductImageListSerializer(many=True, required=False)
    characteristic = AdditionalInformationListSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        characteristics_data = validated_data.pop('characteristic', [])

        product = Product.objects.create(**validated_data)

        if images_data:
            for image_data in images_data:
                image, created = ProductImage.objects.get_or_create(**image_data)
                product.images.add(image)

        for characteristic_data in characteristics_data:
            characteristic, created = AdditionalInformation.objects.get_or_create(**characteristic_data)
            product.characteristic.add(characteristic)

        return product

    def validate(self, data):
        user = data['user']
        if user.user_type == 1:
            raise ValidationError({'user': 'Товар/Услугу может создать только Партнер'})
        return data


class ProductUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('city', 'description', 'quantity', 'price')

    def update(self, instance, validated_data):

        instance.city = validated_data.get('city', instance.city)
        instance.description = validated_data.get('description', instance.description)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price = validated_data.get('price', instance.price)
        instance.save()

        return instance

    def validate(self, data):
        user = data['user']
        if user.user_type == 1:
            raise ValidationError({'user': 'Товар/Услугу может изменять только Партнер'})
        return data


class AdditionalInformationSerializer(serializers.ModelSerializer):
    characteristic = CharacteristicListSerializer()

    class Meta:
        model = AdditionalInformation
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    images = ProductImageListSerializer(many=True)
    characteristic = AdditionalInformationSerializer(many=True)
    category = CategoryListSerializer()

    class Meta:
        model = Product
        fields = '__all__'


class PromotionTypeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PromotionType
        fields = '__all__'


class PromotionCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Promotion
        fields = '__all__'

    def validate(self, data):
        user = data['user']
        if user.user_type == 1:
            raise ValidationError({'user': 'Акцию может создать только Партнер'})
        return data


class PromotionUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promotion
        fields = (
            'user',
            'promotion_type',
            'title',
            'description',
            'limitation',
            'start',
            'end',
            'old_price',
            'new_price',
            'percentage_amount',
            'cashback_amount',
            'products'
        )

