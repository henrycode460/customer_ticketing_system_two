

from django.contrib import admin
from django.urls import path, include, re_path 
import ticketing.routing
from ticketing import routing as ticketing_routing
from django.conf import settings
from django.conf.urls.static import static
# from core.routing import urlpatterns as core_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("", include("apps.home.urls"))  ,
    # UI Kits Html files
      # path('ws/', include(ticketing.routing.websocket_urlpatterns)),
    #   path('core/', include(core_urlpatterns)),
     path('ticketing/', include('ticketing.urls')),
      path('ticketing/', include(('ticketing.urls', 'ticketing'), namespace='ticketing')),
    path('ticketing/', include(ticketing_routing.websocket_urlpatterns)),
   

     
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Telecel Ticketing App Administration Page"
admin.site.site_title = "Admin Page"
admin.site.index_title = "Welcome to the Admin Page"
