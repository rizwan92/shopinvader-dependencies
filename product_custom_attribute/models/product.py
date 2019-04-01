# -*- coding: utf-8 -*-
# Copyright 2011 Akretion (http://www.akretion.com).
# @author Benoit Guillot <benoit.guillot@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api
from lxml import etree


class ProductTemplate(models.Model):
    _inherit = "product.template"

    attribute_set_id = fields.Many2one('attribute.set', 'Attribute Set')

    attribute_group_ids = fields.One2many(
        comodel_name='attribute.group',
        inverse_name='attribute_set_id',
        related='attribute_set_id.attribute_group_ids',
        string='Groups',
        store=False,
    )

    @api.model
    def create(self, vals):
        if not vals.get('attribute_set_id') and vals.get('categ_id'):
            category = self.env['product.category'].browse(vals['categ_id'])
            vals['attribute_set_id'] = category.attribute_set_id.id
        return super(ProductTemplate, self).create(vals)

    @api.multi
    def write(self, vals):
        if not vals.get('attribute_set_id') and vals.get('categ_id'):
            category = self.env['product.category'].browse(vals['categ_id'])
            vals['attribute_set_id'] = category.attribute_set_id.id
        super(ProductTemplate, self).write(vals)
        return True

    @api.multi
    def open_attributes(self):
        self.ensure_one()

        view = self.env.ref(
            'product_custom_attribute.product_attributes_form_view')

        grp_ids = self.attribute_group_ids.ids
        ctx = {'open_attributes': True, 'attribute_group_ids': grp_ids}

        return {
            'name': 'Product Attributes',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view.id,
            'res_model': self._name,
            'context': ctx,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'res_id': self.id,
        }

    @api.multi
    def save_and_close_product_attributes(self):
        return True

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        context = self.env.context

        result = super(ProductTemplate, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)

        if view_type == 'form' and context.get('attribute_group_ids'):
            eview = etree.fromstring(result['arch'])

            # hide button under the name
            button = eview.xpath("//button[@name='open_attributes']")

            if button:
                button = button[0]
                button.getparent().remove(button)

            attributes_notebook, toupdate_fields = (
                self.env['attribute.attribute']._build_attributes_notebook(
                    context['attribute_group_ids']))
            result['fields'].update(self.fields_get(toupdate_fields))

            if context.get('open_attributes'):
                placeholder = eview.xpath(
                    "//separator[@string='attributes_placeholder']")[0]
                placeholder.getparent().replace(
                    placeholder, attributes_notebook)

            elif context.get('open_product_by_attribute_set'):
                notebook = eview.xpath(
                    "//notebook")[0]
                page = etree.SubElement(
                    notebook, 'page', name="attributes_page",
                    colspan="2", col="4", string="Custom attributes")
                page.append(attributes_notebook)

            result['arch'] = etree.tostring(eview, pretty_print=True)
        return result
