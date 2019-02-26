# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from datetime import datetime, timedelta

from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

#    @api.multi
#    def _create_invoice(self):
#        """ If automatic payment is enabled, perform auto pay actions. """
#        invoice = super(AccountAnalyticAccount, self)._create_invoice()
#        if not self.is_auto_pay:
#            return invoice
#        self._do_auto_pay(invoice)
#        return invoice

    @api.multi
    def _do_auto_pay(self, invoice):
        """ Perform all automatic payment operations on open invoices. """
        self.ensure_one()
        invoice.ensure_one()
        invoice.action_invoice_open()
        # import ipdb; ipdb.set_trace() # BREAKPOINT
        self._send_invoice_message(invoice)
        paid = self._pay_invoice(invoice)

#    @api.multi
#    def _pay_invoice(self, invoice):
#        """ Pay the invoice using the account or partner token. """
#
#        if invoice.state != 'open':
#            _logger.info('Cannot pay an invoice that is not in open state.')
#            return
#
#        if not invoice.residual:
#            _logger.debug('Cannot pay an invoice with no balance.')
#            return
#
#        token = self.payment_token_id or self.partner_id.payment_token_id
#        if not token:
#            _logger.debug(
#                'Cannot pay an invoice without defining a payment token',
#            )
#            return
#
#        transaction = self.env['payment.transaction'].create(
#            self._get_tx_vals(invoice),
#        )
#        valid_states = ['authorized', 'done']
#
#        try:
#            result = transaction.s2s_do_transaction()
#            if not result or transaction.state not in valid_states:
#                _logger.debug(
#                    'Payment transaction failed (%s)',
#                    transaction.state_message,
#                )
#            else:
#                # Success
#                return True
#
#        except Exception:
#            _logger.exception(
#                'Payment transaction (%s) generated a gateway error.',
#                transaction.id,
#            )
#
#        transaction.state = 'error'
#        invoice.write({
#            'auto_pay_attempts': invoice.auto_pay_attempts + 1,
#            'auto_pay_failed': fields.Datetime.now(),
#        })
#
#        if invoice.auto_pay_attempts >= self.auto_pay_retries:
#            template = self.pay_fail_mail_template_id
#            self.write({
#                'is_auto_pay': False,
#                'payment_token_id': False,
#            })
#            if token == self.partner_id.payment_token_id:
#                self.partner_id.payment_token_id = False
#
#        else:
#            template = self.pay_retry_mail_template_id
#
#        template.send_mail(invoice.id)

#    @api.multi
#    def _get_tx_vals(self, invoice):
#        """ Return values for create of payment.transaction for invoice."""
#        amount_due = invoice.residual
#        token = self.payment_token_id
#        partner = token.partner_id
#        reference = self.env['payment.transaction'].get_next_reference(
#            invoice.number,
#        )
#        return {
#            'reference': '%s' % reference,
#            'acquirer_id': token.acquirer_id.id,
#            'payment_token_id': token.id,
#            'amount': amount_due,
#            'state': 'draft',
#            'currency_id': invoice.currency_id.id,
#            'partner_id': partner.id,
#            'partner_country_id': partner.country_id.id,
#            'partner_city': partner.city,
#            'partner_zip': partner.zip,
#            'partner_email': partner.email,
#        }
#
#    @api.multi
#    def _send_invoice_message(self, invoice):
#        """ Send the appropriate emails for the invoices if needed. """
#        if invoice.sent:
#            return
#        if not self.invoice_mail_template_id:
#            return
#        _logger.info('Sending invoice %s, %s (template %s)',
#                     invoice, invoice.number, self.invoice_mail_template_id)
#        mail_id = self.invoice_mail_template_id.send_mail(invoice.id)
#        invoice.with_context(mail_post_autofollow=True)
#        invoice.sent = True
#        invoice.message_post(body=_("Invoice sent"))
#        return self.env['mail.mail'].browse(mail_id)
