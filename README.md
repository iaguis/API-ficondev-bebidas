API bebidas
===========

Servidor que ofrece una API REST con serialización en JSON para la [aplicación
android][ficondev-android] desarrollada junto con @SantiMunin para la [FicOnDev 2013][ficondev].

Se trata de una aplicación de gestión de pedidos para distribuidores de bebidas
no azucaradas. Nuestra API incluye métodos de autenticación, desautenticación.
listar productos, hacer un pedido y ver los pedidos pendientes de preparación,
preparados para recoger y recogidos por el distribuidor. El estado se mantiene
con una session id hasta que el usuario hace logout de la aplicación.

Por cuestiones de tiempo, un pedido solo puede tener un producto pero se podría
ampliar en el futuro de forma sencilla.

El servidor asume que hay una base de datos MySQL con el usuario y password
indicados en config.py y con permisos totales para una base de datos llamada
bebidas. Para crear la base de datos se puede utilizar el script SQL ejecutado
en la consola MySQL como el usuario bebidasmaster

    mysql> source recreate_db.sql

y el script Python

    $ python rebuild_model.py

que incluye datos de prueba.

El servidor se arranca en el puerto 8080 por defecto con

    python server.py

A continuación se pueden hacer las peticiones REST definidas en server.py

El archivo utils.py incluye un par de métodos que serían los que la empresa de
fabricación de bebidas utilizaría para marcar un pedido como preparado para
recoger y para marcarlo como recogido. Para ejecutarlos, por ejemplo, en el pedido con id
número 1, en una consola Python:

    >>> import utils
    >>> utils.order_ready(1)
    >>> utils.pick_order(1)

Requisitos:

    python-bottle
    python-sqlalchemy
    python-MySQLdb
    python-m2crypto

[ficondev-android]: https://github.com/SantiMunin/FicOnDev-Android "FicOnDev-Android"
[ficondev]: http://ficondev.es/
