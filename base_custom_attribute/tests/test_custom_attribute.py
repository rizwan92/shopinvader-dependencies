# -*- coding: utf-8 -*-
# Copyright 2011 Akretion (http://www.akretion.com).
# @author Benoît GUILLOT <benoit.guillot@akretion.com>
# @author Raphaël VALYI <raphael.valyi@akretion.com>
# Copyright 2015 Savoir-faire Linux
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
import mock


class TestCustomAttribute(common.TransactionCase):

    def setUp(self):
        super(TestCustomAttribute, self).setUp()
        self.model_id = self.env.ref('base.model_res_partner').id
        # Do not commit
        self.env.cr.commit = mock.Mock()

    def _create_attribute(self, vals):
        vals.update({
            'model_id': self.model_id,
            'field_description': 'Attribute %s' % vals['attribute_type'],
            'name': 'x_%s' % vals['attribute_type'],
            })
        return self.env['attribute.attribute'].create(vals)

    def test_create_attribute_char(self):
        attribute = self._create_attribute({
            'attribute_type': 'char',
            })
        self.assertEqual(attribute.ttype, 'char')

    def test_create_attribute_selection(self):
        attribute = self._create_attribute({
            'attribute_type': 'select',
            'option_ids': [
                (0, 0, {
                    'name': 'Value 1',
                }),
                (0, 0, {
                    'name': 'Value 2',
                }),
            ]
        })

        self.assertEqual(attribute.ttype, 'many2one')
        self.assertEqual(attribute.relation, 'attribute.option')

    def test_create_attribute_multiselect(self):
        attribute = self._create_attribute({
            'attribute_type': 'multiselect',
            'option_ids': [
                (0, 0, {
                    'name': 'Value 1',
                }),
                (0, 0, {
                    'name': 'Value 2',
                }),
            ]
        })

        self.assertEqual(attribute.ttype, 'many2many')
        self.assertEqual(attribute.relation, 'attribute.option')

#    def test_wizard(self):
#        sequence_type_model = self.env['res.partner.category']
#        sequence_type = sequence_type_model.create({
#            'name': 'Sequence type 1',
#        })
#        model = self.model_model.search([
#           ('name', '=', 'res.partner.category')])
#
#        self.vals.update({
#            'attribute_type': 'multiselect',
#            'name': 'x_attribute_multiselect_2',
#            'relation_model_id': model.id,
#        })
#
#        attribute = self.attribute_model.create(self.vals)
#
#        self.wizard_model.create({
#            'attribute_id': attribute.id,
#            'option_ids': [(6, 0, [sequence_type.id])]
#        })
#
#        attribute.refresh()
#
#        self.assertEqual(len(attribute.option_ids), 1)
#        option = attribute.option_ids[0]
#        self.assertEqual(option.value_ref, sequence_type)
