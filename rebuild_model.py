# -*- coding: utf-8 -*-
import model
from DAO import DAO

model._Base.metadata.create_all(model._engine)
d = DAO()

d.signup("Luso", "luso@luso.com", "1111", "666-666")

p1 = model.Product("Red Bull sin azúcar", "La versión sin azúcar de la popular bebida Red Bull")
p2 = model.Product("CocaCola Zero", "Bebe CocaCola sin preocuparte por engordar")
p3 = model.Product("Fanta Zero", "Bebe Fanta sin preocuparte por engordar")

session = model.loadSession()

session.add(p1)
session.add(p2)
session.add(p3)

session.commit()
