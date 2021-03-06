from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, serializers, viewsets
from rest_framework.exceptions import APIException, NotFound

from .models import Signup, SignupTarget


class SignupTargetSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='identifier')

    class Meta:
        model = SignupTarget
        fields = ('id', 'name')


class SignupTargetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list: Return a list of all signup targets.

    retrieve: Return the given sign-up target.
    """
    queryset = SignupTarget.objects.all()
    serializer_class = SignupTargetSerializer
    lookup_field = 'identifier'


class SignupSerializer(serializers.ModelSerializer):
    target = serializers.SlugRelatedField(
        slug_field='identifier', queryset=SignupTarget.objects.all(),
        help_text=_('The identifier of the sign-up target for the sign-up.')
    )
    cancelled_at = serializers.ReadOnlyField()

    class Meta:
        model = Signup
        fields = ('id', 'target', 'created_at', 'cancelled_at')


class SignupAlreadyExists(APIException):
    status_code = 409
    default_detail = _('The sign-up already exists.')
    default_code = 'signup_already_exists'


class SignupFilter(filters.FilterSet):
    include_cancelled = filters.BooleanFilter(method='filter_include_cancelled', help_text=_(
        'Include also cancelled sign-ups. '
        'Accepts boolean values "true" and "false". '
        'Just giving the key without a value is also interpreted as true.'
    ))
    target = filters.CharFilter(name='target__identifier', help_text=_(
        'Include only sign-ups for the given sign-up target. The given value should be a sign-up target identifier.'
    ))

    class Meta:
        model = Signup
        fields = ('include_cancelled', 'target')

    def __init__(self, data=None, *args, **kwargs):
        data = data.copy()
        if 'include_cancelled' not in data:
            data['include_cancelled'] = False
        super().__init__(data, *args, **kwargs)

    def filter_include_cancelled(self, queryset, name, value):
        if not value:
            queryset = queryset.filter(cancelled_at=None)
        return queryset


class SignupViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """

    list: Return a list of all the request user's sign-ups. By default cancelled sign-ups aren't included.

    retrieve: Return the given sign-up.

    create: Create a new sign-up instance.

    delete: Cancel the given sign-up.
    """
    queryset = Signup.objects.select_related('target')
    serializer_class = SignupSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = SignupFilter

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        queryset = Signup.objects.filter(
            user=self.request.user, target=serializer.validated_data['target'], cancelled_at=None
        )

        if queryset.exists():
            raise SignupAlreadyExists()

        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.cancelled_at:
            raise NotFound()

        instance.cancelled_at = now()
        instance.save(update_fields=('cancelled_at',))
