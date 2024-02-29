from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from .models import Product, Lesson, GroupMembership
from .serializers import ProductSerializer, LessonSerializer, ProductStatsSerializer, GroupMembershipSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user
        products = Product.objects.exclude(group__groupmembership__user=user)

        return products


class GroupMembershipViewSet(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = GroupMembershipSerializer
    queryset = GroupMembership.objects.all()

    def create(self, request, *args, **kwargs):
        product_id = self.kwargs['product_pk']
        product = Product.objects.get(pk=product_id)
        if error := product.subscribe(self.request.user):
            return Response(status=status.HTTP_400_BAD_REQUEST, data=error)
        return Response(status=status.HTTP_201_CREATED, data='Вы успешно записаны на курс')


class ProductStatsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductStatsSerializer
    queryset = Product.objects.all()


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_pk']
        user = self.request.user
        lessons = Lesson.objects.filter(product_id=product_id, product__group__groupmembership__user=user)

        return lessons
