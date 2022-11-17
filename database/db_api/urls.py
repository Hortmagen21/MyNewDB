from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from . import views

urlpatterns = [
        path('home/db/<slug:db_name>/create_db', views.create_db, name='create_db'),
        path('home/db/<slug:db_name>', views.db, name='watch_db'),
        path('home/db/<slug:db_name>/create_table', views.create_table, name='create_table'),
        path('home/db/<slug:db_name>/table/<slug:table_name>/create_cols_names',
             views.create_cols_names, name='create_cols_names'),
        path('home/db/<slug:db_name>/table/<slug:table_name>/create_cols/<slug:cols_num>', views.create_cols,
             name='create_cols'),

        path('home/db/<slug:db_name>/table/<slug:table_name>/add_row', views.add_row, name='table_add_row'),
        path('home/db/<slug:db_name>/table/<slug:table_name>/view_table', views.view_table, name='view_table'),
        path('home/db/<slug:db_name>/table/<slug:table_name>/delete_row', views.delete_row, name='table_delete_row'),
        path('home/db/<slug:db_name>/table/<slug:table_name>/edit_row', views.edit_row, name='table_edit_row'),
        path('home/db/<slug:db_name>/table/<slug:table_name>/del_same_rows', views.del_same_rows,
             name='table_del_same_rows'),
        path('schema', get_schema_view(title="db_api", description="api for db", version="1.0.0"), name='openapi-schema'),
        path('docs/', include_docs_urls(title="db_api" )),
]
