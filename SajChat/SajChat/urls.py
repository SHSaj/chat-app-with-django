from django.contrib import admin
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView

from core.views import(
    home_screen_view,
    chat_view,
    sentMessages,
    receivedMessages,
    chatNotification,
)

from account.views import(
    register_view,
    login_view,
    logout_view,
    account_search_view,
)


urlpatterns = [
    path('',home_screen_view, name='home'),
    path('account/', include('account.urls', namespace='account')),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('search/', account_search_view, name='search'),
    path('chat/<str:pk>', chat_view, name='chat'),
    path('sent_msg/<str:pk>', sentMessages, name='sent_msg'),
    path('rec_msg/<str:pk>', receivedMessages, name='rec_msg'),
    path('notification/', chatNotification, name = "notification"),
]

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
