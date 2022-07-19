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
