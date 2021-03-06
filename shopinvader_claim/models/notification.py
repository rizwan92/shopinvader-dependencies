# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.tools.translate import _


class ShopinvaderNotification(models.Model):
    _inherit = 'shopinvader.notification'

    def _get_all_notification(self):
        res = super(ShopinvaderNotification, self)._get_all_notification()
        res['claim_confirmation'] = {
            'name': _('Claim Confirmation'),
            'model': 'crm.claim',
            }
        return res
