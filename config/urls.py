from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.documentation import include_docs_urls

v1_urls = [
    re_path(r'', include('bookit.access.urls')),
    re_path(r'', include('bookit.common.urls')),
    re_path(r'', include('bookit.session.urls')),
]

urlpatterns = [
    re_path(r'admin/?', admin.site.urls),
    re_path(r'rest-auth/?', include('rest_auth.urls')),
    re_path(r'api/v1/', include((v1_urls, 'v1'), namespace='v1')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        # rest-auth
        path(
            'docs/',
            include_docs_urls(title='APIs',
                              authentication_classes=[],
                              permission_classes=[])),
    ]
