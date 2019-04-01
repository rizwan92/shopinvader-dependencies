# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Rating",
    "summary": "Rate your product",
    "version": "8.0.1.0.0",
    "category": "Uncategorized",
    "website": "www.akretion.com",
    "author": " Akretion",
    "license": "AGPL-3",
    "application": False,
    'installable': False,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "product",
    ],
    "data": [
        "views/product_rating_view.xml",
        "views/product_view.xml",
        "data/product_rating_data.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
