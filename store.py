import json

from bottle import run, template, static_file, get, post, delete, request
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
    category_name = request.forms.get("name")
    with connection.cursor() as cursor:
        sql = "select count(1) from category where cat_name='{}'".format(category_name)
        cursor.execute(sql)
        result = cursor.fetchall()

        if result == [{'count(1)': 1}]:
            return ({"STATUS": "ERROR - The category was not created due to an error", "MSG": "category already exists",
                     "code": "200"})

        elif category_name == " ":

            return (
            {"STATUS": "ERROR - The category was not created due to an error", "MSG": "Name parameter is missing",
             "code": "400"})


        elif result == [{'count(1)': 0}]:
            adding_category = 'INSERT INTO category (cat_name)  values ("{}")'.format(category_name)
            cursor.execute(adding_category)
            connection.commit()
            return json.dumps(
                {'STATUS': 'SUCCESS', "MSG": "The category was created successfully", {cat_id: cursor.lastrowid},
                 "code":"201"})

            else:
            return ({
                "STATUS": "ERROR - The category was not created due to an error", "MSG": "Internal error",
                "code": "500"})


@delete('/category/<id>')
def delete_category(id):
    with connection.cursor() as cursor:
        sql = "select count(1) from category where cat_name='{}'".format(category_name)
        cursor.execute(sql)
        result = cursor.fetchall()

        if result == [{'count(1)': 0}]:
            return ({"STATUS": "ERROR - The category was not deleted due to an error", "MSG": "Category not found",
                     "code": "404"})

        elif result == [{'count(1)': 1}]:
            sqlDelete_cat = "DELETE FROM CATEGORY where cat_id={}".format(id)
            cursor.execute(sqlDelete_cat)
            connection.commit()
            return json.dumps({"STATUS": "SUCCESS - The category was deleted successfully", "code": "201"})

        else:
            return json.dumps(
                {"STATUS": "ERROR - The category was not deleted due to an error", "MSG": "internal error",
                 "code": "500"})


@get('/categories')
def list_categories():
    try:
        categories = []
    with connection.cursor() as cursor:
        sql = "SELECT * FROM categories"
        cursor.execute(sql)
        result = cursor.fetchall()
        for element in result:
            cat_to_add = {"id": element['cat_id'], "name": element["cat_name"]}
            categories.append(cat_to_add)
            return json.dumps({"STATUS": "SUCCESS - Categories fetched", "code": "200"})
        except:
        return json.dumps({"STATUS": "ERROR -internal error", "MSG": "Internal error", code": "500"})




                           run(host='localhost', port=7000)
