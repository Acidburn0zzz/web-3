# -*- coding: utf-8 -*-
##############################################################################
#
#    Authors: Laurent Mignon
#    Copyright (c) 2014 Acsone SA/NV (http://www.acsone.eu)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import orm
from openerp.tools.translate import _


class HelpOnline(orm.TransientModel):
    _name = 'help.online'

    def _get_view_name(self, model, view_type, domain=None, context=None):
        name = 'help-%s' % model.replace('.', '-')
        return name

    def page_exists(self, name):
        website_model = self.env['website']
        return website_model.page_exists(name)

    def get_page_url(self, model, view_type, domain=None, context=None):
        user_model = self.env['res.users']
        if not user_model.has_group('help_online.help_online_group_reader'):
            return {}
        ir_model = self.env['ir.model']
        description = self.env[model]._description
        res = ir_model.name_search(model, operator='=')
        if res:
            description = res[0][1]
        name = self._get_view_name(model, view_type, domain, context)
        if self.page_exists(name):
            url = '/page/%s' % name
            if view_type:
                url = url + '#' + view_type
            title = _('Help on %s') % description
            return {'url': url,
                    'title': title,
                    'exists': True}
        elif user_model.has_group('help_online.help_online_group_writer'):
            title = _('Create Help page for %s') % description
            return {'url': 'website/add/%s' % name,
                    'title': title,
                    'exists': False}
        else:
            return {}
