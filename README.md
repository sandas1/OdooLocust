# OdooLocust

An Odoo load testing solution, using openerplib and Locust

## Links

* odoolib: <a href="https://github.com/odoo/odoo-client-lib">odoo-client-lib</a>
* Locust: <a href="http://locust.io">locust.io</a>
* Odoo: <a href="https://odoo.com">odoo.com</a>

# HowTo

To load test Odoo, you create tasks like you'll have done it with Locust:

```
from configparser import ConfigParser

from locust import task

from src.odoo_locust import OdooLocust

parser = ConfigParser()
parser.read("odoo_locust.conf")


class Task(OdooLocust):
    host = parser.get("odoo_locust_config", "host")
    database = parser.get("odoo_locust_config", "database")
    min_wait = parser.getint("odoo_locust_config", "min_wait")
    max_wait = parser.getint("odoo_locust_config", "max_wait")
    weight = parser.getint("odoo_locust_config", "weight")

    @task
    def read_partner(self):
        partner_model = self.client.get_model("res.partner")
        partner_ids = partner_model.search([("personal_code", "=", "750000351")])
        partners = partner_model.read(partner_ids)

    @task
    def read_contract(self):
        sale_sub_model = self.client.get_model("sale.subscription")
        subs_ids = sale_sub_model.search([("code", "=", "SUB4254")])
        subs = sale_sub_model.read(subs_ids)
```

then you create a profile config file (odoo_locust.conf)
```
[odoo_locust_config]
port = 80
login = admin
password = secretpassword
protocol = jsonrpc
user_id = 2

host = 127.0.0.1
database = test_db
min_wait = 100
max_wait = 1000
weight = 3

use_https = False

```

and you finally run your locust tests the usual way:

```
locust -f task.py Task
```

Navigate to http://0.0.0.0:8089/ after running locust.

![image](https://user-images.githubusercontent.com/69576212/179865181-50f18335-2e51-4dd5-9b22-c468bc76e4e3.png)
