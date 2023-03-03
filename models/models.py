# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime


class TimesheetsPayroll(models.Model):
    _name = 'timesheets.payroll'
    _description = 'hr_custoizations.hr_custoizations'

    employee = fields.Many2one("hr.employee","Employee")
    ref_num = fields.Char("Ref Number")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    state = fields. Selection([('draft', 'draft'), ('submitted', 'submitted'),('approved', 'approved'),('expensed','expensed')], default='draft',string='Stage')
    captured_by = fields.Many2one("res.users","Caputured By")
    timesheet_lines = fields.One2many('timesheet.lines', 'ref_num')
    approved_by = fields.Many2one("res.users", "Approved By")
    hourly_cost = fields.Monetary("Hourly Cost",related="employee.hourly_cost")
    total_hours = fields.Float("Total Hours", compute="_get_total_hours")
    currency_id = fields.Many2one("res.currency", string="Valuta", required=True)

    def _get_total_hours(self):
        total_hours = 0.0
        for line in self.timesheet_lines:
            total_hours += line.unit_amount
        self.total_hours = total_hours

    def validate_submit(self):
        context = self._context
        current_uid = context.get('uid')
        for rec in self:
            rec.state = "submitted"
            rec.captured_by = self.env['res.users'].browse(current_uid)
    def approve(self):
        context = self._context
        current_uid = context.get('uid')
        for rec in self:
            rec.state = "approved"
            rec.approved_by = self.env['res.users'].browse(current_uid)
    def create_expense(self):
        decription = self.employee.name + "-" + str(self.end_date)
        record = self.env['hr.expense'].create({
            'name': decription,
            'employee_id' : self.employee.id,
            'total_amount' : self.hourly_cost * self.total_hours,
            'date': datetime.today(),
            'state':'reported'

        })
        if record:
            self.state = "expensed"


class TimesheetLines(models.Model):
    _name = 'timesheet.lines'
    _description = 'Time Sheet Lines'
    _rec_name = 'name'

    ref_num = fields.Many2one("timesheets.payroll")
    name = fields.Char("Description")
    date = fields.Date("Timesheet Dates")
    project = fields.Many2one("project.project","Project")
    task = fields.Many2one("project.task", "Tasks")
    unit_amount = fields.Float("Unit Amount")

class HrExpense(models.Model):
    _inherit = 'hr.expense'
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('reported', 'Submitted'),
        ('validated', 'Validated'),
        ('approved', 'Approved'),
        ('done', 'Paid'),
        ('refused', 'Refused')
    ], compute='_compute_state', string='Status', copy=False, index=True, readonly=True, store=True, default='draft')

    def action_validate_expenses(self):
            context = self._context
            current_uid = context.get('uid')
            for rec in self:
                rec.state = "validated"
