# -*- coding: utf-8 -*-
from bottle import route, request, run
from DAO import DAO

@route("/login/<email>/<password>", method="POST")
def login(email='', password=''):
    return dao.login(email, password)

@route("/logout/<session_id>")
def logout(session_id=''):
    return dao.logout(session_id)

@route("/signup/<name>/<email>/<password>/<telephone>", method="POST")
def signup(name='', email='', password='', telephone=''):
    return dao.signup(name, email, password, telephone)

@route("/neworder/<session_id>", method="POST")
def neworder(session_id=''):
    json_order = request.forms.get("order")
    return dao.neworder(session_id, json_order)

@route("/listproducts/<session_id>")
def listproducts(session_id=''):
    dao.renew_session()
    return dao.list_products(session_id)

@route("/pendingorders/<session_id>")
def pendingorders(session_id=''):
    dao.renew_session()
    return dao.pending_orders(session_id)

@route("/readyorders/<session_id>/<since>")
def readyorders(session_id='', since=''):
    dao.renew_session()
    return dao.ready_orders(session_id, since)


#@route("/getStories/<session_id>/<searchterm>/<page>")
#def get_stories(session_id='', searchterm='', page=''):
    #return dao.get_stories(session_id, searchterm, page)

#@route("/getStoriesByCity/<session_id>/<city>/<page>")
#def get_stories_by_city(session_id='', city='', page=''):
    #return dao.get_stories_by_city(session_id, city, page)

#@route("/getStoriesByUser/<session_id>/<page>")
#def get_stories_by_user(session_id='', page=''):
    #return dao.get_stories_by_user(session_id, page)

#@route("/getStory/<session_id>/<story_id>")
#def get_story(session_id='', story_id=''):
    #return dao.get_story(session_id, story_id)

#@route("/addStory", method="POST")
#def add_story():
    #title = request.forms.get("title")
    #description = request.forms.get("description")
    #price = request.forms.get("price")
    #city = request.forms.get("city")
    #creator = request.forms.get("creator")
    #json_text = request.forms.get("json_text")
    #json_images = request.forms.get("json_images")

    #return dao.add_story(title, description, price, city, creator, json_text, json_images)

#@route("/validate/<validation_hash>")
#def validate(validation_hash=''):
    #return dao.validate(validation_hash)

dao = DAO()
run (host='localhost', port=8080, debug=True)
