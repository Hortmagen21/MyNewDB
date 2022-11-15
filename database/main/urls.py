from django.urls import path, include

from . import views

urlpatterns = [
        path('home', views.home, name='home'),
        path('home/create_db', views.create_db, name='create_db'),
        path('home/upload', views.upload_db, name='upload'),
        path('home/db/<slug:db_name>', views.db, name='watch_db'),
        path('home/db/<slug:db_name>/edit_name', views.edit_db_name, name='edit_db_name'),
        path('home/db/<slug:db_name>/delete', views.delete_db, name='edit_db_name'),
        path('home/db/<slug:db_name>/download', views.download, name='download'),
        path('home/db/<slug:db_name>/create_table', views.create_table, name='create_table'),
        path('home/db/<slug:db_name>/table/<slug:table_name>/create_cols_names', views.create_cols_names,
             name='create_cols_names'),
        path('home/db/<slug:db_name>/table/<slug:table_name>/create_cols/<slug:cols_num>', views.create_cols,
             name='create_cols'),
        path('home/db/<slug:db_name>/table/<slug:table_name>/add_row', views.add_row, name='table_add_row'),
        path('home/db/<slug:db_name>/table/<slug:table_name>/view_table', views.view_table, name='view_table'),
        path('home/db/<slug:db_name>/table/<slug:table_name>/delete_row/<slug:id_delete>', views.delete_row,
             name='table_delete_row'),
        path('home/db/<slug:db_name>/table/<slug:table_name>/edit_row', views.edit_row, name='table_edit_row'),
        path('home/db/<slug:db_name>/table/<slug:table_name>/delete_table', views.delete_table, name='delete_table'),
        path('home/db/<slug:db_name>/table/<slug:table_name>/del_same_rows', views.del_same_rows,
             name='table_del_same_rows'),




]