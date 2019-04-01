# -*- coding: utf-8 -*-
# Copyright 2011 Akretion (http://www.akretion.com).
# @author Benoît GUILLOT <benoit.guillot@akretion.com>
# @author Raphaël VALYI <raphael.valyi@akretion.com>
# Copyright 2015 Savoir-faire Linux
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AttributeGroup(models.Model):
    _name = "attribute.group"
    _description = "Attribute Group"
    _order = "sequence"

    name = fields.Char(
        'Name',
        size=128,
        required=True,
        translate=True
    )

    sequence = fields.Integer('Sequence')

    attribute_set_id = fields.Many2one(
        'attribute.set',
        'Attribute Set',
        required=True,
    )

    attribute_ids = fields.One2many(
        'attribute.location',
        'attribute_group_id',
        'Attributes'
    )

    model_id = fields.Many2one(
        'ir.model',
        'Model',
        readonly=True,
        related='attribute_set_id.model_id',
    )
