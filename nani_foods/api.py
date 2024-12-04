import frappe
from frappe import _
from frappe.utils import today
from datetime import date
import datetime
from frappe.model.naming import make_autoname
from frappe.model.naming import getseries
import json

@frappe.whitelist()
def make_gate_entry(name):
	pur_order=frappe.get_doc("Purchase Order",name)
	new_ge=frappe.new_doc("Gate Entry")
	new_ge.gate_entry_type = "Inward Entry"
	new_ge.invoice_no = pur_order.name
	new_ge.date=today()
	new_ge.invoice_quantity = pur_order.total_qty
	new_ge.party_name = pur_order.supplier
	for i in pur_order.items:
		new_ge.append("material",
		{
			"item_code":i.item_code,
			"item_name":i.item_name,
			"qty":i.qty,
			"uom":i.uom
		})
	return new_ge


@frappe.whitelist()
def get_po_filters():
	po_list=[i[0] for i in frappe.db.sql(""" select DISTINCT po.name from `tabPurchase Order` as po join `tabPurchase Order Item`as poi on poi.parent=po.name where po.docstatus!=2 and poi.geqty=0 """,as_list=1)]
	return po_list


@frappe.whitelist()
def create_purchase_reciept(name):
	todays_date = date.today()
	mm="0"
	if(todays_date.month<=9):
		mm=mm+str(todays_date.month)
	else:
		mm=str(todays_date.month)
	ge = frappe.get_doc("Gate Entry",name)
	pur_rec = frappe.new_doc("Purchase Receipt")
	pur_rec.supplier = ge.supplier
	pur_rec.set_warehouse = ge.warehouse
	for row in ge.material:
		item = frappe.get_doc("Item",row.item_code)
		pur_rec.append("items",{
			"item_code":row.item_code,
			"item_name":row.item_name,
			"goods_inward_number_gin":str(row.item_code)+str(mm)+str(todays_date.year)[2:],
			"uom":row.uom,
			"received_qty":row.received_quantity,
			"description":item.description,
			"item_group":item.item_group,
			"stock_uom":item.stock_uom,
		})
	return pur_rec

@frappe.whitelist()
def create_batch_no(self,method):
	for i in self.items:
		if not i.batch_no:
			new_batch = frappe.new_doc("Batch")
			new_batch.batch_id = make_autoname(i.goods_inward_number_gin + ".####")
			new_batch.item = i.item_code
			new_batch.save()
			i.batch_no = new_batch.name

@frappe.whitelist()
def create_fg_lot_series(self,methods):
#	series_no = getseries("", 4)
#	month_no = today = date.today().month
#	if len(str(month_no))==1:
#		month = "0" + str(month_no)
#	year_no = today = date.today().year
#	year = str(year_no).strip()[-2] + str(year_no).strip()[-1]
#	self.fg_lot_series = str(self.fg_lot_no) + str(series_no) + str(month) + str(year)
	if self.fg_lot_no:
		self.fg_lot_series = make_autoname(self.fg_lot_no + ".####..MM..YY.")

def no_of_bags_wo(self,methods):
	if self.sales_order:
		sales_ord = frappe.get_doc("Sales Order", self.sales_order)
		for row in sales_ord.items:
			if row.item_name == self.item_name:
				self.no_of_bags = row.no_of_bags

#def cbm_calc(self, methods):
#	self.cbm = (self.dimension_1/100) * (self.dimension_2/100) * (self.dimension_3/100)
#	self.cft  = (self.dimension_1 * self.dimension_2 * self.dimension_3)/28316.846592

def cbm_total_calc(self, methods):
#	if self.naming_series == 'SAL-ORD-.YYYY.-EXP-.#####':
	tot_cbm = 0
	tot_cft = 0
	for row in self.items:
		if row.conversion:
#				row.case_quantity = row.qty / float(row.conversion)
			row.cbm = (row.dimension_1/100) * (row.dimension_2/100) * (row.dimension_3/100) * float(row.case_quantity)
			row.cft  = ((row.dimension_1 * row.dimension_2 * row.dimension_3)/28316.846592) * float(row.case_quantity)
			tot_cbm += row.cbm
			tot_cft += row.cft
	self.total_cbm = tot_cbm
	self.total_cft = tot_cft
#	else:
#		pass

def so_date_val(self, methods):
	if self.shipping_date:
		if self.shipping_date < self.transaction_date:
			frappe.throw("Dispatch Date cannot be lower than Transaction Date")
	if self.soc_expiry_date:
		if self.soc_expiry_date < self.transaction_date:
			frappe.throw("Expiry Date cannot be lower than Transaction Date")

def commision_rate_sum(self, methods):
	cr = 0
	for row in self.items:
		row.commision_rate_of_item = (row.commission_percent/100) * row.amount
		cr = cr + row.commision_rate_of_item
	self.total_commission = cr

@frappe.whitelist()
def create_batch_no_sr(self):
	for i in json.loads(self):
		batch = frappe.new_doc("Batch")
		batch.batch_id = i['batch_no']
		batch.item = i['item_code']
		batch.save()
	frappe.msgprint('Batches Created')
	return

@frappe.whitelist()
def ge_materials(pur_ord):
	po= frappe.get_doc('Purchase Order', pur_ord)
	po_item_list = []
	for i in po.items:
		po_item_list.append(i)
	return po_item_list

## Gate Entry Purchase Order Filters
@frappe.whitelist()
def purchase_order_list_desc(doctype, txt, searchfield, start, page_len, filters):
	active_filter = {"docstatus": 1}

	filters = {**active_filter, **filters} if filters else active_filter

	fields = ["name", "supplier", "supplier_name"]

	text_in = {"name": ("like", "%%%s%%" % txt), "supplier": ("like", "%%%s%%" % txt)}

	return frappe.get_all(
		"Purchase Order",
		fields=fields,
		filters=filters,
		or_filters=text_in,
		start=start,
		page_length=page_len,
		order_by="modified desc",
		as_list=1,
	)

@frappe.whitelist()
def customer_item_code(item_code, customer):
	if item_code:
		ic_doc = frappe.get_doc("Item", item_code)
		if ic_doc.customer_items:
			for row in ic_doc.customer_items:
				if row.customer_name == customer:
					return row.ref_code, row.dimension_length__cm, row.dimension__breadth__width__cm, row.dimension__height__cm, row.packing_type, row.conversion, row.conversion_2



@frappe.whitelist()
def create_dispatch_note(so_name):
	so_doc = frappe.get_doc("Sales Order", so_name)
	doc = frappe.new_doc("Dispatch Note") 
	doc.po_no = so_doc.po_no
	doc.so_no = so_name
	so_item = so_doc.items
	dispatch_item_row = []
	for i in so_item:
		item_details = {}
		item_details['item_code'] = i.item_code
		item_details['product'] = i.item_code
		item_details['gross'] = float("{:.3f}".format(float(i.gross_weight)))
		item_details['qty'] = int(i.qty)
		item_details['total_net'] = float("{:.3f}".format(float(i.total_net_weight)))
		item_details['total_gross'] = float("{:.3f}".format(float(i.total_gross_weight)))
		dispatch_item_row.append(item_details)

	for d_item in dispatch_item_row:
		doc.append("dispatch_items", d_item)
	return doc

@frappe.whitelist()
def create_delivery_note(di_no_name):
	di_doc = frappe.get_doc("Dispatch Note", di_no_name)
	so_doc = frappe.get_doc("Sales Order", di_doc.so_no)
	de_doc = frappe.new_doc("Delivery Note")
	de_doc.customer = so_doc.customer
	de_doc.set_warehouse = so_doc.set_warehouse
#	de_doc.
	
		

	return de_doc




