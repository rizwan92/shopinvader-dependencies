# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.addons.connector.session import ConnectorSession
from odoo.addons.connector_locomotivecms.connector import get_environment
from odoo.addons.shopinvader.services.sale import SaleService
from odoo.addons.shopinvader_claim.services.claim import ClaimService
from odoo.addons.shopinvader.services.address import AddressService
import json
import urllib


class ShopinvaderNotification(models.Model):
    _inherit = 'shopinvader.notification'

    def _get_service(self, record, service_class):
        session = ConnectorSession.from_env(self.env)
        env = get_environment(session, record._name, self.backend_id.id)
        service = env.backend.get_class(service_class, session, record._name)
        return service(env, None, {})

    def _send(self, record):
        msg_ids = super(ShopinvaderNotification, self)._send(record)
        message = self.env['mail.mail'].browse(msg_ids)[0]
        message.external_template_key = self.template_id.external_template_key
        data = {}
        if record._name in ['sale.order', 'account.invoice']:
            if record._name == 'account.invoice':
                record = record.sale_ids[0]
            service = self._get_service(record, SaleService)
            sale = service._to_json(record)[0]
            if sale['anonymous_token']:
                sale.update({
                    'is_anonymous': 1,
                    'url_anonymous': urllib.urlencode({
                        'token': sale['anonymous_token'],
                        'email': sale['anonymous_email'],
                        })
                    })
            else:
                sale['is_anonymous'] = 0
            data = {'sale': sale}
        elif self.notification_type == 'new_customer_welcome':
            service = self._get_service(record, AddressService)
            data = {'customer': service._to_json(record)[0]}
        elif self.notification_type == 'claim_confirmation':
            service = self._get_service(record, ClaimService)
            data = {'claim': service._to_json(record)[0]}
        message.data = json.dumps(data)
        return msg_ids
