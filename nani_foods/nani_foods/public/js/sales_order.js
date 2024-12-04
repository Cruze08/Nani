frappe.ui.form.on("Sales Order","refresh",function(frm) {
//    frm.add_custom_button(__("Create Gate Entry"), function() {
//      frappe.call({
//			method: "",
//			args: {
//				name:frm.doc.name
//			},
//			callback: function(r) {
//				var doclist = frappe.model.sync(r.message);
//				frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
//				// cur_frm.refresh_fields()
//			}
//		});
//	})
});
