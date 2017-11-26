from django.conf.urls import url
from . import views
urlpatterns = [
            url(r"^$", views.index, name="index"),
            url(r"^lectures/$", views.lectures, name="lectures"),
            url(r"^homework/$", views.homework, name="homework"),
            url(r"^info/$", views.info, name="info"),
            url(r"^meetings/$", views.meetings, name="meetings"),
            url(r"^postNewLection/$", views.lectures, name="postNewLecure"),
            url(r"^downloads/(.*)/(.*)/$", views.download, name="download"),
            url(r"^registration/$", views.registration, name="registration"),
            url(r"^signin/$", views.signin, name="signin"),
            url(r"^logout/$", views.signout, name="logout")
        ]
