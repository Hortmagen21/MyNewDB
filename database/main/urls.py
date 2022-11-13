from django.urls import path, include

from . import views

urlpatterns = [
        path('home', views.home, name='home'),
        path('home/create_db', views.create_db, name='create_db'),
        path('home/db', views.db, name='watch_db'),
        path('home/upload', views.upload_db, name='upload'),
        path('home/download', views.download, name='download'),
        path('home/create_table', views.create_table, name='create_table'),
        path('home/create_table/create_cols', views.create_cols, name='create_cols'),
        path('home/create_table/create_cols_names', views.create_cols_names, name='create_cols_names'),
        path('home/table/add_row', views.add_row, name='table_add_row'),
        path('home/table/view_table', views.view_table, name='view_table'),
        path('home/table/delete_row', views.delete_row, name='table_delete_row'),
        path('home/table/edit_row', views.edit_row, name='table_edit_row'),
        path('home/table/del_same_rows', views.del_same_rows, name='table_del_same_rows'),
]