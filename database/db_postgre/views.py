from django.shortcuts import render
import psycopg2
# Create your views here.
from django.shortcuts import render
import json
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import ast
from os import listdir
from os.path import isfile, join
import os


def home(request):
    conn = psycopg2.connect("dbname='d6lsheh0j6mukf' user='vttjdzcrbmnrde'"
                            " host='ec2-35-173-91-114.compute-1.amazonaws.com'"
                            " password='cc014fcd75936158b6229c56c9c3987eb1c30d4cf47cad067b0176a77568ca87'")
    cur = conn.cursor()

    """path = 'C:/Users/Max/ITLab1/database/main/database'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    db_names = []
    for file in files:
        name, ext = file.split('.')
        db_names.append(name)

    data = {
        "db_names": db_names
    }"""
    data = {}
    template = loader.get_template('main/index.html')
    return HttpResponse(template.render(data, request))
