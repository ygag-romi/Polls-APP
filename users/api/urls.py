from django.urls import include, path

app_name = 'api'
urlpatterns = [
    path('v1/', include('users.api.v1.urls'))
]
