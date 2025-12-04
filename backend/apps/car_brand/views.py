from django.utils.decorators import method_decorator

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from drf_yasg.utils import swagger_auto_schema

from .filter import CarBrandFilter
from .models import CarBrandModel
from .permissions import IsAdminOrSuperUser
from .serializers import CarBrandSerializer


@method_decorator(name='get', decorator=swagger_auto_schema( security=[] ))
class CarBrandListCreateView(ListCreateAPIView):
    """
        get:
            get car brand list
        post:
            create new car brand
    """
    queryset = CarBrandModel.objects.all()
    serializer_class = CarBrandSerializer
    filterset_class = CarBrandFilter

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminOrSuperUser()]
        return [AllowAny()]


@method_decorator( name='get', decorator=swagger_auto_schema( security=[] ))
class CarBrandRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
        get:
            get car brand detail by id
        put:
            full update car brand by id
        patch:
            partial update car brand by id
        delete:
            delete car brand by id
    """

    queryset = CarBrandModel.objects.all()
    serializer_class = CarBrandSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminOrSuperUser()]
        return [AllowAny()]