from django.shortcuts import render
import json
from django.http import HttpResponse
from django.template import loader
from main.forms import NameForm
from django.http import HttpResponseRedirect
from django.template import Context


class DB:
    def __init__(self, db_name):
        self.name = db_name

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


class Table:
    def __init__(self, db_instance, table_name):
        self.db_instance = db_instance
        self.name = table_name

    def get_cols_type_json(self):
        return self.db_instance["tables"][self.name]["cols_type"]

    def get_cols_name_json(self):
        return self.db_instance["tables"][self.name]["cols_name"]

    def get_rows_json(self):
        return self.db_instance["tables"][self.table_name]["rows"]

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
        table.append(new_data)


def add_row(request):
    if request.method == 'GET':
        db_name = request.GET.get('db_name', '')
        table_name = request.GET.get('table_name', '')
        database = DB(db_name=db_name)
        db_instance = database.get_db_info_json()
        table_inst = Table(db_instance=db_instance, table_name=table_name)
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
        db_name = request.POST.get('db_name', '')
        table_name = request.POST.get('table_name', '')
        fields = request.POST.getlist('fields', '')
        new_data = {}
        database = DB(db_name=db_name)
        db_instance = database.get_db_info_json()
        table_inst = Table(db_instance=db_instance, table_name=table_name)
        cols_name = table_inst.get_cols_name_json()
        # new_data = list(zip(cols_name, fields))
        for i in range(len(fields)):
            new_data[f"{cols_name[i]}"] = fields[i]
        table = table_inst.get_rows_json()
        try:
            last_row = table[-1]
            last_id = last_row["id"]
        except Exception:
            last_id = 0
        new_data["id"] = last_id+1

        table.append(new_data)
        database.set_db_info_json(db_instance)
        return HttpResponseRedirect(f"/main/home/db?name={db_name}")


def home(request):
    template = loader.get_template('main/index.html')
    return HttpResponse(template.render({}, request))


def create_db(request):
    if request.method == 'POST':
        form = NameForm(request.POST)

        db_name = form.data.get('db_name')
        link = f'C:/Users/Max/ITLab1/database/main/database/{db_name}.json'
        data = {
            "name": db_name,
            "tables": {}
        }
        json_object = json.dumps(data, indent=4)
        with open(link, 'w+') as f:
            f.write(json_object)
            print("The database was created")

        return HttpResponseRedirect(f"db?name={db_name}")


def db(request):
    if request.method == 'GET':
        db_name = request.GET.get('name', '')
        link = f'C:/Users/Max/ITLab1/database/main/database/{db_name}.json'
        with open(link, 'r') as f:
            data_json = json.load(f)
            print(data_json["name"])
            data = {
                "tables": data_json["tables"],
                "db_name": db_name,
            }

    template = loader.get_template('main/db.html')
    return HttpResponse(template.render(data, request))


def create_table(request):
    if request.method == 'GET':
        db_name = request.GET.get('db_name', '')
        data = {
            "name": db_name
        }
        template = loader.get_template('main/create_table.html')
        return HttpResponse(template.render(data, request))
    if request.method == 'POST':
        form = NameForm(request.POST)
        table_name = form.data.get('table_name')
        cols_num = form.data.get('cols_num')
        db_name = form.data.get('db_name')
        link = f'C:/Users/Max/ITLab1/database/main/database/{db_name}.json'
        with open(link, 'r+') as f:
            data = json.load(f)
            new_data = {table_name: {}}
            data["tables"].update(new_data)
            json_object = json.dumps(data, indent=4)
            f.seek(0)
            f.write(json_object)
            f.truncate()
            print("The table in " + db_name + " was created and have name " + table_name)
            cols_value = ""
            for j in range(int(cols_num)):
                cols_value += str(j)

        return HttpResponseRedirect(f"create_table/create_cols?table_name={table_name}&cols_num={cols_value}&db_name={db_name}")


def create_cols(request):
    if request.method == 'GET':
        db_name = request.GET.get('db_name', '')
        table_name = request.GET.get('table_name', '')
        cols_num = request.GET.get('cols_num', '')
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
        new_data = {"cols_type": types}
        link = f'C:/Users/Max/ITLab1/database/main/database/{db_name}.json'
        with open(link, 'r+') as f:
            data = json.load(f)
            data["tables"][f"{table_name}"].update(new_data)
            json_object = json.dumps(data, indent=4)
            f.seek(0)
            f.write(json_object)
            f.truncate()
        # types , cols don't need
        data = {
            "db_name": db_name,
            "table_name": table_name,
            "cols_num": cols_num,
            "cols_type": types,
        }
        template = loader.get_template('main/cols_names.html')
        return HttpResponse(template.render(data, request))


# types, cols don't need
#CHECK IF NOT NAME COL ID
#CHECK DUBLS NAMES
def create_cols_names(request):
    if request.method == 'POST':
        db_name = request.POST.get('db_name', '')
        cols_num = request.POST.get('cols_num', '')
        table_name = request.POST.get('table_name', '')
        types = request.POST.getlist('type', '')
        names = request.POST.getlist('field', '')
        new_data = {"cols_name": names}
        empty_rows = {"rows": []}
        link = f'C:/Users/Max/ITLab1/database/main/database/{db_name}.json'
        with open(link, 'r+') as f:
            data = json.load(f)
            data["tables"][f"{table_name}"].update(new_data)
            data["tables"][f"{table_name}"].update(empty_rows)
            json_object = json.dumps(data, indent=4)
            f.seek(0)
            f.write(json_object)
            f.truncate()
        return HttpResponseRedirect(f"/main/home/db?name={db_name}")


def view_table(request):
    if request.method == 'GET':
        db_name = request.GET.get('db_name', '')
        table_name = request.GET.get('table_name', '')
        link = f'C:/Users/Max/ITLab1/database/main/database/{db_name}.json'
        with open(link, 'r+') as f:
            data_json = json.load(f)
            rows = data_json["tables"][f"{table_name}"]["rows"]
            cols_name = data_json["tables"][f"{table_name}"]["cols_name"]
        data = {
            "db_name": db_name,
            "table_name": table_name,
            "rows": rows,
            "cols_name": cols_name,
        }
        template = loader.get_template('main/view_table.html')
        return HttpResponse(template.render(data, request))


def delete_row(request):
    if request.method == 'GET':
        db_name = request.GET.get('db_name', '')
        table_name = request.GET.get('table_name', '')
        data = {
            "db_name": db_name,
            "table_name": table_name,
        }
        template = loader.get_template('main/table_delete_row.html')
        return HttpResponse(template.render(data, request))
    if request.method == 'POST':
        db_name = request.POST.get('db_name', '')
        table_name = request.POST.get('table_name', '')
        row_id = request.POST.get('id_field', '')
        link = f'C:/Users/Max/ITLab1/database/main/database/{db_name}.json'
        with open(link, 'r+') as f:
            data_json = json.load(f)
            rows = data_json["tables"][f"{table_name}"]["rows"]
            i = 0
            for row in rows:
                if row['id'] == int(row_id):
                    break
                i += 1
            try:
                del rows[i]
            except IndexError:
                print(f"Row with id:{row_id} does not exist")
            json_object = json.dumps(data_json, indent=4)
            f.seek(0)
            f.write(json_object)
            f.truncate()
        return HttpResponseRedirect(f"/main/home/db?name={db_name}")


def edit_row(request):
    if request.method == 'GET':
        db_name = request.GET.get('db_name', '')
        table_name = request.GET.get('table_name', '')
        link = f'C:/Users/Max/ITLab1/database/main/database/{db_name}.json'
        with open(link, 'r+') as f:
            data_json = json.load(f)
            col_type = data_json["tables"][f"{table_name}"]["cols_type"]
            col_name = data_json["tables"][f"{table_name}"]["cols_name"]
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
        db_name = request.POST.get('db_name', '')
        table_name = request.POST.get('table_name', '')
        fields = request.POST.getlist('fields', '')
        row_id = request.POST.get('id_field', '')
        print("Fieds:")
        print(fields)
        link = f'C:/Users/Max/ITLab1/database/main/database/{db_name}.json'
        with open(link, 'r+') as f:
            data_json = json.load(f)
            rows = data_json["tables"][f"{table_name}"]["rows"]
            i = 0
            for row in rows:
                if row['id'] == int(row_id):
                    break
                i += 1
            try:
                row_to_edit = rows[i]
                j = 0
                for row_field_name in row_to_edit.keys():
                    row_to_edit[f"{row_field_name}"] = fields[j]
                    j += 1

            except IndexError:
                print(f"Row with ID:{row_id} does not exist")
            print("Row edited: ")
            print(row_to_edit)
            json_object = json.dumps(data_json, indent=4)
            f.seek(0)
            f.write(json_object)
            f.truncate()
        return HttpResponseRedirect(f"/main/home/db?name={db_name}")


def del_same_rows(request):
    if request.method == 'GET':
        db_name = request.GET.get('db_name', '')
        table_name = request.GET.get('table_name', '')
        link = f'C:/Users/Max/ITLab1/database/main/database/{db_name}.json'
        with open(link, 'r+') as f:
            data_json = json.load(f)
            rows = data_json["tables"][f"{table_name}"]["rows"]
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
                    if row == row2:
                        same_rows_list.add(i)
                        same_rows_list.add(j)

                    row2['id'] = temp_id
                    j += 1
                i += 1
            for el in sorted(same_rows_list, reverse=True):
                del rows[el]
            json_object = json.dumps(data_json, indent=4)
            f.seek(0)
            f.write(json_object)
            f.truncate()
        return HttpResponseRedirect(f"/main/home/db?name={db_name}")


def download(request):
    if request.method == 'GET':
        db_name = request.GET.get('db_name', '')
        link = f'C:/Users/Max/ITLab1/database/main/database/{db_name}.json'
        with open(link, 'r+') as f:
            data_json = json.load(f)
        response = HttpResponse(content_type='application/json; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="db.json"'

        t = loader.get_template('main/download.json')
        c = {
            "db": data_json,
        }

        response.write(t.render(c))
        return response


def upload_db(request):
    if request.method == "POST":

        file = request.FILES
        print(request)
        print(file)

    return HttpResponse(status=200)
