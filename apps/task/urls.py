from django.urls import path

from apps.task.views import SchemasView, SchemaUpdateView, SchemaCreateView, SchemaDeleteView, SchemaDetailView

urlpatterns = [
    path('', SchemasView.as_view(), name='schemas'),
    path('schema/create/', SchemaCreateView.as_view(), name='schema-create'),
    path('schema/update/<int:pk>/', SchemaUpdateView.as_view(), name='schema-update'),
    path('schema/delete/<int:pk>/', SchemaDeleteView.as_view(), name='schema-delete'),
    path('schema/<int:pk>/', SchemaDetailView.as_view(), name='schema-detail'),
]
