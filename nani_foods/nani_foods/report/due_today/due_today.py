# Copyright (c) 2023, Simpel and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import date

def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_columns(filters):
		columns = [
				{
					"fieldname": "sales_invoice_no",
					"label": _("Sales Invoice No."),
					"fieldtype": "Link",
					"options":"Sales Invoice",
					"width": 120
				},
				{
                                        "fieldname": "due_date",
                                        "label": _("Due Date"),
                                        "fieldtype": "Data",
                                        "width": 120 
                                },
				{
                                        "fieldname": "no",
                                        "label": _("No"),
                                        "fieldtype": "Int",
                                        "width": 120,
					"default": 1
                                }
		]

		return columns

def get_data(filters):
	today = date.today()
	data = frappe.db.sql(""" SELECT
				name as sales_invoice_no,
				due_date as due_date,
				1 as no
				FROM
				`tabSales Invoice`
				WHERE
				due_date = '{0}'
				 """.format(today), as_dict=True)
	return data
