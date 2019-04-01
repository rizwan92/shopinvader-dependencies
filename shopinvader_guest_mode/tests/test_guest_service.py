# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from werkzeug.exceptions import Forbidden, NotFound

from odoo.addons.shopinvader.tests.common import CommonCase


class TestGuestService(CommonCase):

    def setUp(self, *args, **kwargs):
        super(TestGuestService, self).setUp(*args, **kwargs)
        self.data = {
            'email': 'new@customer.example.com',
            'name': 'Purple',
            'street': 'Rue du jardin',
            'zip': '43110',
            'city': 'Aurec sur Loire',
            'phone': '0485485454',
            'country': {'id': self.env.ref('base.fr').id},
            }
        with self.work_on_services(
                partner=None,
                shopinvader_session=self.shopinvader_session) as work:
            self.service = work.component(usage='guest')
        self.shopinvader_config = self.env['shopinvader.config.settings']
        self.backend.is_guest_mode_allowed = True

    def _create_guest(self):
        res = self.service.dispatch('create', params=self.data)['data']
        partner = self.env['res.partner'].browse(res['id'])
        return partner.shopinvader_bind_ids

    def test_create_guest(self):
        res = self.service.dispatch('create', params=self.data)['data']
        partner = self.env['res.partner'].browse(res['id'])
        self.assertEqual(partner.email, self.data['email'])
        first_binding = partner.shopinvader_bind_ids
        self.assertEqual(first_binding.is_guest, True)
        # if we create a new guest with the same email, a new binding is
        # created and the first one is archived
        # moreover in no duplicate mode, the partner remains the same
        self.shopinvader_config.create({
            "no_partner_duplicate": True,
        }).execute()
        res = self.service.dispatch('create', params=self.data)['data']
        new_partner = self.env['res.partner'].browse(res['id'])
        self.assertEqual(partner, new_partner)
        self.assertFalse(first_binding.active)
        new_binding = partner.shopinvader_bind_ids
        self.assertEqual(new_binding.is_guest, True)
        self.assertNotEquals(first_binding, new_binding)

    def test_search_guest(self):
        self._create_guest()
        res = self.service.search(email='toto')
        self.assertFalse(res['found'])
        res = self.service.search(email=self.data['email'])
        self.assertTrue(res['found'])

    def test_register_guest(self):
        email = self.data['email']
        external_id = 'pajrth78'
        with self.assertRaises(NotFound), self.env.cr.savepoint():
            self.service.register(email, external_id)
        binding = self._create_guest()
        self.assertTrue(binding.is_guest)
        self.service.register(email, external_id)
        self.assertFalse(binding.is_guest)

    def test_guest_mode_allowed(self):
        self.backend.is_guest_mode_allowed = False
        with self.assertRaises(Forbidden), self.env.cr.savepoint():
            self._create_guest()
        self.backend.is_guest_mode_allowed = True
        binding = self._create_guest()
        self.assertTrue(binding.is_guest)
