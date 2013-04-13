from DAO import DAO
from model import Order
from datetime import datetime

def order_ready(order_id):
    d = DAO()
    o = d.session.query(Order).filter(Order.order_id == order_id).one()
    o.date_ready = datetime.utcnow()
    d.session.commit()
    d.session.close()

def pick_order(order_id):
    d = DAO()
    o = d.session.query(Order).filter(Order.order_id == order_id).one()
    if not o.date_ready:
        print "Order not ready"
        return
    o.date_picked = datetime.utcnow()
    d.session.commit()
    d.session.close()

