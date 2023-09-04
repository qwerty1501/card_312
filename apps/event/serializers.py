from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.users.models import User
from apps.event.models import Event, EventImage


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class EventImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = '__all__'


class EventCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    photo = EventImageListSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = '__all__'

    def validate(self, data):
        user = data['user']
        if user.user_type == 1:
            raise ValidationError({'user': 'Мероприятие может создать только Партнер'})
        return data


class EventListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    photo = EventImageListSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'


class EventUpdateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    photo = EventImageListSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = ('user', 'title', 'location', 'date', 'description', 'start_price', 'end_price', 'photo')

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.location = validated_data.get('location', instance.location)
        instance.date = validated_data.get('date', instance.date)
        instance.description = validated_data.get('description', instance.description)
        instance.start_price = validated_data.get('start_price', instance.start_price)
        instance.end_price = validated_data.get('end_price', instance.end_price)

        # Обработка связей Many-to-Many для поля 'photo'
        if 'photo' in validated_data:
            instance.photo.set(validated_data['photo'])

        instance.save()

        return instance

    def validate(self, data):
        user = data['user']
        if user.user_type == 1:
            raise ValidationError({'user': 'Мероприятие может изменять только Партнер'})
        return data