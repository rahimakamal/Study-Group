from django.urls import path
from . import views

urlpatterns = [
    path("notes/", views.notes, name="notes"),
    path("notes/download/<int:note_id>/", views.download_note, name="download_note"),
    path("notes/report/<int:note_id>/", views.report_note, name="report_note"),
]
