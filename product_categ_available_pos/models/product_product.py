# -*- coding: utf-8 -*-
from odoo import models


class ProductProduct(models.Model):
    _inherit = ["categ.available_in_pos.abstract", "product.product"]
    _name = 'product.product'

    pass
