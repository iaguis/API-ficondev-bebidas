# -*- coding: utf-8 -*-
import json

def json_login(session_id):
    return session_id

def json_logout():
    return "success"

def json_error(error):
    return error

def json_signup():
    return "success"

def json_neworder(order_id):
    return json.dumps({"orderId" : order_id}, ensure_ascii=False)

def json_products(products_dict):
    return json.dumps(products_dict, ensure_ascii=False)
