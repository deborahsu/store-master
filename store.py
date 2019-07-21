import json

from bottle import run, template, static_file, get, post, request, delete
from pymysql import connect, cursors

connection = connect(host='127.0.0.1',
                     user='root',
                     password='1234567890',
                     db='store',
                     charset='utf8',
                     cursorclass=cursors.DictCursor)


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@post("/category/<category>")
def assign_category():
    return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


@post('/category')
def add_category():
    try:
        category_name = request.forms.get("name")
        with connection.cursor() as cursor:
            sql = "select * from category where cat_name='{}'".format(category_name)
            count = cursor.execute(sql)
            if count >= 1:
                return ({"STATUS": "ERROR", "MSG": "The category was not created due to an error - category already exists",
                         "code": "200"})

            elif not category_name.strip():

                return (
                    {"STATUS": "ERROR", "MSG": "The category was not created due to an error - Name parameter is missing",
                     "code": "400"})

            else:
                adding_category = 'INSERT INTO category (cat_name)  values ("{}")'.format(category_name)
                cursor.execute(adding_category)
                connection.commit()
                return json.dumps(
                    {'STATUS': 'SUCCESS', 'MSG': 'The category was created successfully', 'CAT_ID': cursor.lastrowid,
                    'code':'201'})
    except Exception as e:
        return ({
            "STATUS": "ERROR", "MSG": "Internal error - The category was not created due to an error - " + str(e),
            "code": "500"})

@delete('/category/<id>')
def delete_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "select * from category where cat_id='{}'".format(id)
            count = cursor.execute(sql)
        if count == 0:
            return ({"STATUS": "ERROR", "MSG": "The category was not deleted due to an error - Category not found",
                  "code": "404"})

        elif count == 1:
            sqlDelete_cat = "DELETE FROM CATEGORY where cat_id={}".format(id)
            cursor.execute(sqlDelete_cat)
            connection.commit()
            return json.dumps({"STATUS": "SUCCESS - The category was deleted successfully", "code": "201"})

    except Exception as e:
        return json.dumps(
            {"STATUS": "ERROR", "MSG": "Internal error - The category was not deleted due to an error - " + str(e),
             "code": "500"})


@get('/categories')
def list_categories():
    try:
        categories = []
        with connection.cursor() as cursor:
            sql = "SELECT * FROM category"
            cursor.execute(sql)
            result = cursor.fetchall()
        for element in result:
            cat_to_add = {"id": element['cat_id'], "name": element["cat_name"]}
            categories.append(cat_to_add)
        return json.dumps({"STATUS": "SUCCESS", "MSG":"Categories fetched", "code": "200", "CATEGORIES":categories})
    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": "Internal error - " + str(e), "code": "500"})

run(host='localhost', port=7000)
