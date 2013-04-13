# -*- coding: utf-8 -*-
import json
from datetime import datetime

def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0

def json_login(session_id):
    return session_id

def json_logout():
    return "success"

def json_error(error):
    return error

def json_signup():
    return "success"

def json_neworder(order_id):
    return json.dumps({"order_id" : order_id}, ensure_ascii=False)

def json_products(products_dict):
    return json.dumps(products_dict, ensure_ascii=False)

def json_pending_orders(pendingorders):
    pendingorders_dict = {"orders" : []}
    for order in pendingorders:
        order_dict = { "order_id"     : order.order_id,
                       "product_id"   : order.product_id,
                       "product_name" : order.products.name,
                       "amount"       : order.amount,
                       "date_ordered" : int(round(unix_time_millis(order.date_ordered))),
                       "order_price"  : order.amount * order.products.price
                     }
        pendingorders_dict["pendingorders"].append(order_dict)
    return json.dumps(pendingorders_dict, ensure_ascii=False)

def json_ready_orders(readyorders):
    readyorders_dict = {"orders" : []}
    for order in readyorders:
        order_dict = { "order_id"     : order.order_id,
                       "product_id"      : order.product_id,
                       "product_name"      : order.products.name,
                       "amount"       : order.amount,
                       "date_ordered" : int(round(unix_time_millis(order.date_ordered))),
                       "date_ready"   : int(round(unix_time_millis(order.date_ready))),
                       "order_price" : order.amount * order.products.price
                     }
        readyorders_dict["readyorders"].append(order_dict)
    return json.dumps(readyorders_dict, ensure_ascii=False)
