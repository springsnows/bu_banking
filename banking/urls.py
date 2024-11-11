from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, TransactionViewSet, BusinessViewSet



router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'businesses', BusinessViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

#TASK1 Add swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi 
from rest_framework.permissions import AllowAny 

schema_view = get_schema_view(
   openapi.Info(
      title="Banking API",
      default_version='v1',
      description="API documentation for Extra Credit Union",
   ),
   public=True,
   permission_classes=(AllowAny,),
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
#ENDTASK1
