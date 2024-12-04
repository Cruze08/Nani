# Copyright (c) 2023, Simpel and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import date, datetime, timedelta
import time

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

today = date.today()
year = today.year
from datetime import datetime, timedelta

def get_current_week_dates():
    # Get the current date
	today = datetime.now()

    # Calculate the start date of the current week (Monday)
	start_of_week = today - timedelta(days=today.weekday())

    # Generate a list of dates for the current week (Monday to Sunday)
	week_dates = [start_of_week + timedelta(days=i) for i in range(7)]

    # Format the dates as strings (optional)
	formatted_dates = [date.strftime('%Y-%m-%d') for date in week_dates]

	return formatted_dates

# Example usage
current_week_dates = get_current_week_dates()
current_week_dates = tuple(current_week_dates)
def get_data(filters):
	data = frappe.db.sql(""" SELECT
				name as sales_invoice_no,
				due_date as due_date,
				1 as no
				FROM
				`tabSales Invoice`
				WHERE
				due_date in {0}
				 """.format(current_week_dates), as_dict=True)
	return data
