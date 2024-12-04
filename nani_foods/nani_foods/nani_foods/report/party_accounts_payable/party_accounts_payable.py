# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from nani_foods.nani_foods.report.party_accounts_receivable.party_accounts_receivable import ReceivablePayableReport


def execute(filters=None):
	args = {
		"party_type": "Supplier",
		"naming_by": ["Buying Settings", "supp_master_name"],
	}
	return ReceivablePayableReport(filters).run(args)
