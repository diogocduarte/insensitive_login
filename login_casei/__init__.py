# -*- coding: utf-8 -*-
import openerp
import logging
from openerp.osv import  osv
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)


class users(osv.osv):
    _inherit = "res.users"

    def _login(self, db, login, password):
        if not password:
            return False
        user_id = False
        try:
            with self.pool.cursor() as cr:
                res = self.search(cr, SUPERUSER_ID, [('login', '=ilike', login)])
                if res:
                    user_id = res[0]
                    self.check_credentials(cr, user_id, password)
                    self._update_last_login(cr, user_id)
        except openerp.exceptions.AccessDenied:
            _logger.info("Login failed for db:%s login:%s", db, login)
            user_id = False
        return user_id