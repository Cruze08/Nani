# Copyright (c) 2023, Simpel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GateEntry(Document):
	def validate(self):
		th=""
		for i in self.material:
			if(i.received_quantity<=0 or i.received_quantity>i.qty):
				th=th+"Received Quantity in row "+str((i.idx)-1)+" Should be >0 and <=Quantity \n "
			if(th !=""):
				frappe.throw(th)
		for i in self.material:
			geqty=(i.qty - i.received_quantity)
			frappe.errprint(geqty)
			frappe.db.sql(""" update `tabPurchase Order Item` set gate_entry=%s,geqty=%s  where name =%s""",(self.name,geqty,i.purchase_order_item_name))
			frappe.db.commit()
