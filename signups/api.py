from rest_framework import serializers, viewsets

from .models import Signup, SignupTarget


class SignupTargetSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='identifier')

    class Meta:
        model = SignupTarget
        fields = ('id', 'name')


class SignupTargetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SignupTarget.objects.all()
    serializer_class = SignupTargetSerializer
    lookup_field = 'identifier'


class SignupSerializer(serializers.ModelSerializer):
    target = serializers.SlugRelatedField(slug_field='identifier', queryset=SignupTarget.objects.all())

    class Meta:
        model = Signup
        fields = ('id', 'target', 'created_at', 'cancelled_at')


class SignupViewSet(viewsets.ModelViewSet):
    queryset = Signup.objects.select_related('target')
    serializer_class = SignupSerializer
