from django.urls import path, include

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('polls/<int:question_id>/',
         login_required(views.DetailView.as_view()), name='detail'),
    path('polls/<int:pk>/results/',
         login_required(views.ResultsView.as_view()), name='results'),
    path('polls/<int:question_id>/vote/',
         login_required(views.VoteView.as_view()), name='vote'),

    path('polls/api/', include('polls.api.urls'))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
