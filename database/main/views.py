from django.shortcuts import render
import json
from django.http import HttpResponse
from django.template import loader
from main.forms import NameForm
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import ast
from os import listdir
from os.path import isfile, join
import os


class DB:
    def __init__(self, db_name):
        self.name = db_name

    def create_db(self):
        link = f'C:/Users/Max/ITLab1/database/main/database/{self.name}.json'
        data = {
            "name": self.name,
            "tables": {}
        }
        json_object = json.dumps(data, indent=4)
        with open(link, 'w+') as f:
            f.write(json_object)
            print("The database was created")

    def get_db_info_json(self):
        link = f'C:/Users/Max/ITLab1/database/main/database/{self.name}.json'
        with open(link, 'r+') as f:
            data = json.load(f)
            db_instance = data
        return db_instance

    def set_db_info_json(self, db_instance):
        link = f'C:/Users/Max/ITLab1/database/main/database/{self.name}.json'
        with open(link, 'r+') as f:
            json_object = json.dumps(db_instance, indent=4)
            f.seek(0)
            f.write(json_object)
            f.truncate()

    def view_db(self):
        db_instance = self.get_db_info_json()
        data = {
            "tables": db_instance["tables"],
            "db_name": self.name,
        }
        return data

    def create_table(self, table_name, cols_num):
        db_instance = self.get_db_info_json()
        new_data = {table_name: {}}
        db_instance["tables"].update(new_data)
        self.set_db_info_json(db_instance)
        print("The table in " + self.name + " was created and have name " + table_name)
        cols_value = ""
        for j in range(int(cols_num)):
            cols_value += str(j)
        return cols_value

    def download(self):
        db_instance = self.get_db_info_json()
        response = HttpResponse(content_type='application/json; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="db.json"'

        t = loader.get_template('main/download.json')
        c = {
            "db": db_instance,
        }

        response.write(t.render(c))
        return response

    def edit_db_name(self, new_db_name):
        link_old = f'C:/Users/Max/ITLab1/database/main/database/{self.name}.json'
        link_new = f'C:/Users/Max/ITLab1/database/main/database/{new_db_name}.json'
        os.rename(link_old, link_new)
        self.name = new_db_name
        db_instance = self.get_db_info_json()

        db_instance["name"] = new_db_name

    def delete_table(self, table_name):
        db_instance = self.get_db_info_json()
        del db_instance["tables"][f"{table_name}"]
        self.set_db_info_json(db_instance)


class Table:
    def __init__(self, db_obj, table_name):
        self.db_obj = db_obj
        self.name = table_name
        self.db_instance = self.db_obj.get_db_info_json()

    def get_cols_type_json(self):
        return self.db_instance["tables"][self.name]["cols_type"]

    def get_cols_name_json(self):
        return self.db_instance["tables"][self.name]["cols_name"]

    def get_rows_json(self):
        return self.db_instance["tables"][self.name]["rows"]

    def set_rows_json(self, row):
        self.db_instance["tables"][self.name]["rows"].append(row)
        return self.db_instance

    def add_row_json(self, fields):
        new_data = {}
        cols_name = self.get_cols_name_json()
        for i in range(len(fields)):
            new_data[f"{cols_name[i]}"] = fields[i]
        table = self.get_rows_json()
        try:
            last_row = table[-1]
            last_id = last_row["id"]
        except Exception:
            last_id = 0
        new_data["id"] = last_id+1
        new_db_instance = self.set_rows_json(new_data)
        self.db_obj.set_db_info_json(new_db_instance)

    def create_cols(self, types):
        new_data = {"cols_type": types}

        self.db_instance["tables"][f"{self.name}"].update(new_data)
        self.db_obj.set_db_info_json(self.db_instance)

    def create_names(self, names):
        if len(names) != len(set(names)):
            print("ERROR: Some cols have same names")

            del self.db_instance["tables"][f"{self.name}"]
            self.db_obj.set_db_info_json(self.db_instance)
            return HttpResponseRedirect(f"/main/home/db/{self.db_obj.name}")
        else:
            new_data = {"cols_name": names}
            empty_rows = {"rows": []}
            self.db_instance["tables"][f"{self.name}"].update(new_data)
            self.db_instance["tables"][f"{self.name}"].update(empty_rows)
            self.db_obj.set_db_info_json(self.db_instance)
            return HttpResponseRedirect(f"/main/home/db/{self.db_obj.name}")

    def view_table(self):
        rows = self.db_instance["tables"][f"{self.name}"]["rows"]
        cols_name = self.db_instance["tables"][f"{self.name}"]["cols_name"]
        data = {
            "db_name": self.db_obj.name,
            "table_name": self.name,
            "rows": rows,
            "cols_name": cols_name,
        }
        return data

    def delete_row(self, row_id):
        rows = self.db_instance["tables"][f"{self.name}"]["rows"]
        i = 0
        for row in rows:
            if row['id'] == int(row_id):
                break
            i += 1
        print(f"Row with id:{i + 1} was deleted")
        try:
            del rows[i]
        except IndexError:
            print(f"Row with id:{row_id + 1} does not exist")
        self.db_obj.set_db_info_json(self.db_instance)

    def edit_row(self, row_id, fields):
        print("Fields")
        print(fields)
        rows = self.db_instance["tables"][f"{self.name}"]["rows"]
        i = 0
        for row in rows:
            if row['id'] == int(row_id):
                break
            i += 1
        try:
            row_to_edit = rows[i]
            j = 0
            cols_name = self.get_cols_name_json()
            for row_field_name in cols_name:
                row_to_edit[f"{row_field_name}"] = fields[j]
                j += 1

        except IndexError:
            print(f"Row with ID:{row_id+1} does not exist")
        print("Row edited: ")
        print(row_to_edit)
        self.db_obj.set_db_info_json(self.db_instance)

    def del_same_rows(self):
            rows = self.db_instance["tables"][f"{self.name}"]["rows"]
            same_rows_list = set()
            i = 0
            for row in rows:
                j = 0
                for row2 in rows:
                    if row2['id'] == row['id']:
                        j += 1
                        continue
                    temp_id = row2['id']
                    row2['id'] = row['id']
                    print(row)
                    print(row2)
                    if row == row2:
                        same_rows_list.add(i)
                        same_rows_list.add(j)

                    row2['id'] = temp_id
                    j += 1
                i += 1
            print(same_rows_list)
            for el in sorted(same_rows_list, reverse=True):
                del rows[el]

            self.db_obj.set_db_info_json(self.db_instance)


@csrf_exempt
def delete_table(request, db_name, table_name):
    if request.method == 'DELETE':
        database = DB(db_name=db_name)
        database.delete_table(table_name)
        return HttpResponse(status=200)


# check db_name for .json, .png ...
def edit_db_name(request, db_name):
    if request.method == "GET":
        data = {
            "db_name": db_name
        }
        template = loader.get_template('main/db_edit_name.html')
        return HttpResponse(template.render(data, request))
    if request.method == "POST":
        new_db_name = request.POST.get('db_name', '')
        database = DB(db_name=db_name)
        database.edit_db_name(new_db_name=new_db_name)

    return HttpResponseRedirect(f"/main/home/db/{new_db_name}")


def upload_db(request):
    if request.method == "GET":
        template = loader.get_template('main/upload.html')
        return HttpResponse(template.render({}, request))
    if request.method == "POST":
        f = request.FILES['db_name']
        link = f'C:/Users/Max/ITLab1/database/main/database/{f.name}'
        byte_str = f.read()
        dict_str = byte_str.decode("UTF-8")
        mydata = ast.literal_eval(dict_str)
        path = f.name.split('.')
        mydata["name"] = path[0]
        with open(link, 'w+') as destination:

            json_object = json.dumps(mydata, indent=4)
            destination.write(json_object)

    return HttpResponseRedirect(f"/main/home/db/{path[0]}")


def download(request, db_name):
    if request.method == 'GET':
        database = DB(db_name=db_name)
        return database.download()


@csrf_exempt
def del_same_rows(request, db_name, table_name):
    if request.method == 'DELETE':
        print(db_name)
        print(table_name)
        database = DB(db_name=db_name)
        table_inst = Table(db_obj=database, table_name=table_name)
        table_inst.del_same_rows()
        return HttpResponse(status=200)


def edit_row(request, db_name, table_name):
    if request.method == 'GET':
        database = DB(db_name=db_name)
        table_inst = Table(db_obj=database, table_name=table_name)
        col_type = table_inst.get_cols_type_json()
        col_name = table_inst.get_cols_name_json()
        cols_info = []
        for i in range(len(col_type)):
            cols_info.insert(i, {"id": i, "name": col_name[i], "type": col_type[i]})
        data = {
            "db_name": db_name,
            "table_name": table_name,
            "cols_info": cols_info,
        }
        template = loader.get_template('main/table_edit_row.html')
        return HttpResponse(template.render(data, request))
    if request.method == 'POST':
        db_name = db_name
        table_name = table_name
        fields = request.POST.getlist('fields', '')
        row_id = request.POST.get('id_field', '')
        database = DB(db_name=db_name)
        table_inst = Table(db_obj=database, table_name=table_name)
        table_inst.edit_row(row_id=row_id, fields=fields)
        return HttpResponseRedirect(f"/main/home/db/{db_name}")


@csrf_exempt
def delete_row(request, db_name, table_name, id_delete):
    if request.method == 'GET':
        db_name = db_name
        table_name = table_name
        data = {
            "db_name": db_name,
            "table_name": table_name,
        }
        template = loader.get_template('main/table_delete_row.html')
        return HttpResponse(template.render(data, request))
    if request.method == 'DELETE':
        db_name = db_name
        table_name = table_name
        row_id = id_delete
        database = DB(db_name=db_name)
        table_inst = Table(db_obj=database, table_name=table_name)
        table_inst.delete_row(row_id=row_id)
        return HttpResponse(status=200)


def view_table(request, db_name, table_name):
    if request.method == 'GET':
        database = DB(db_name=db_name)
        table_inst = Table(db_obj=database, table_name=table_name)
        data = table_inst.view_table()
        template = loader.get_template('main/view_table.html')
        return HttpResponse(template.render(data, request))


def create_cols_names(request, db_name, table_name):
    if request.method == 'POST':
        db_name = db_name
        table_name = table_name
        names = request.POST.getlist('field', '')
        database = DB(db_name=db_name)
        table_inst = Table(db_obj=database, table_name=table_name)
        return table_inst.create_names(names)


def create_cols(request, db_name, table_name, cols_num):
    if request.method == 'GET':
        db_name = db_name
        table_name = table_name
        cols_num = cols_num
        data = {
            "db_name": db_name,
            "table_name": table_name,
            "cols_num": cols_num,
        }
        template = loader.get_template('main/create_cols.html')
        return HttpResponse(template.render(data, request))
    if request.method == 'POST':
        db_name = request.POST.get('db_name', '')
        cols_num = request.POST.get('cols_num', '')
        table_name = request.POST.get('table_name', '')
        types = request.POST.getlist('type', '')
        database = DB(db_name=db_name)
        table_inst = Table(db_obj=database, table_name=table_name)
        table_inst.create_cols(types=types)
        data = {
            "db_name": db_name,
            "table_name": table_name,
            "cols_num": cols_num,
            "cols_type": types,
        }
        template = loader.get_template('main/cols_names.html')
        return HttpResponse(template.render(data, request))


def create_table(request, db_name):
    if request.method == 'GET':
        data = {
            "db_name": db_name
        }
        template = loader.get_template('main/create_table.html')
        return HttpResponse(template.render(data, request))
    if request.method == 'POST':
        form = NameForm(request.POST)
        table_name = form.data.get('table_name')
        cols_num = form.data.get('cols_num')
        db_name = form.data.get('db_name')
        database = DB(db_name=db_name)
        cols_value = database.create_table(table_name=table_name,cols_num=cols_num)
        return HttpResponseRedirect(f"table/{table_name}/create_cols/{cols_value}")


def db(request, db_name):
    if request.method == 'GET':
        database = DB(db_name=db_name)
        data = database.view_db()
    template = loader.get_template('main/db.html')
    return HttpResponse(template.render(data, request))


def add_row(request, db_name, table_name):
    if request.method == 'GET':
        db_name = db_name
        table_name = table_name
        database = DB(db_name=db_name)
        table_inst = Table(db_obj=database, table_name=table_name)
        col_type = table_inst.get_cols_type_json()
        col_name = table_inst.get_cols_name_json()
        cols_info = []
        for i in range(len(col_type)):
            cols_info.insert(i, {"id": i, "name": col_name[i], "type": col_type[i]})
        data = {
            "db_name": db_name,
            "table_name": table_name,
            "cols_info": cols_info,
        }
        template = loader.get_template('main/table_add_row.html')
        return HttpResponse(template.render(data, request))
    if request.method == 'POST':
        db_name = db_name
        table_name = table_name
        fields = request.POST.getlist('fields', '')
        database = DB(db_name=db_name)
        table_inst = Table(db_obj=database, table_name=table_name)
        table_inst.add_row_json(fields)
        return HttpResponseRedirect(f"/main/home/db/{db_name}")


def home(request):
    path = 'C:/Users/Max/ITLab1/database/main/database'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    db_names = []
    for file in files:
        name, ext = file.split('.')
        db_names.append(name)

    data = {
        "db_names": db_names
    }
    template = loader.get_template('main/index.html')
    return HttpResponse(template.render(data, request))


@csrf_exempt
def create_db(request, db_name):
    if request.method == 'POST':
        database = DB(db_name=db_name)
        database.create_db()
        return HttpResponse(status=200)


@csrf_exempt
def delete_db(request, db_name):
    if request.method == 'DELETE':
        link = f'C:/Users/Max/ITLab1/database/main/database/{db_name}.json'
        os.remove(link)
        return HttpResponse(status=200)



