from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = 'api'

routers = DefaultRouter()
routers.register(r'v1/cliente', views.ClienteAPIv1)
routers.register(r'v1/clienteuser', views.ClienteUserAPIv1)
routers.register(r'v1/banco', views.BancoAPIv1)
routers.register(r'v1/categoria', views.CategoriaAPIv1)
routers.register(r'v1/parceiro', views.ParceiroAPIv1)
routers.register(r'v1/contasreceber', views.ContasAReceberAPIv1)
routers.register(r'v1/contaspagar', views.ContasAPagarAPIv1, basename='contasApagar')
routers.register(r'v1/transferir', views.TransfirirAPIv1, basename='transferir')
routers.register(r'v1/fluxo', views.FluxoCaixaViewSet, basename='fluxo')
routers.register(r'v1/resumodiario', views.ResumoDiarioViewSet, basename='resumoDiario')
routers.register(r'v1/resumocategoria', views.ResumoCategoriaViewSet, basename='resumoCategoria')
routers.register(r'v1/resumoparceiro', views.ResumoParceiroViewSet, basename='resumoParceiro')


urlpatterns = [
    path('v1/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(routers.urls))
]
