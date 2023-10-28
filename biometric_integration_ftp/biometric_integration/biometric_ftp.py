import datetime
import frappe


import csv
import json
import os

from frappe.utils.data import flt, get_time, getdate
@frappe.whitelist()
def employee_checkin(csv_data):
    csv_data=list(csv_data)
    emp=frappe.db.get_value("Employee",{"attendance_device_id":csv_data[0],"device_name":csv_data[11]},"name")
    if emp:
        import datetime

        date_string = str(csv_data[5])
        time_string = str(csv_data[6])

        # convert date and time strings to datetime objects
        date_object = datetime.datetime.strptime(date_string, "%d/%m/%Y")
        time_object = datetime.datetime.strptime(time_string, "%H:%M:%S").time()

        # combine date and time objects into a single datetime object
        combined_datetime = datetime.datetime.combine(date_object, time_object)

        empdoc=frappe.get_doc("Employee",emp)
        doc_link=None
        if empdoc.default_shift:
            val = frappe.db.exists(
                    "Employee Checkin", {"employee": empdoc.employee, "time": combined_datetime}
                )
            if val:
                doc_link = frappe.get_desk_link("Employee Checkin", val)
        
            if not doc_link: 
                doc=frappe.new_doc("Employee Checkin")
                doc.employee=empdoc.employee
                doc.employee_name=empdoc.employee_name
                doc.shift=empdoc.default_shift
                print(combined_datetime)
                doc.time=combined_datetime
                if csv_data[8]=="Check In":
                    doc.log_type="IN"
                else:
                    doc.log_type="OUT"

                doc.save(ignore_permissions=True)
                frappe.db.commit()

                                    
        


def change(self,method):
    if self.shift:
        doc=frappe.get_doc("Shift Type",self.shift)
        date1 = get_time(doc.start_time)
        date2 = get_time(doc.end_time)
        # Calculate the difference between the dates
        date_diff = date2.hour - date1.hour
        from datetime import datetime, timedelta
        print("$$$$$$$$$$$$$$$$$$$",self.shift_start)
        date_format = "%Y-%m-%d %H:%M:%S"

        # Convert the string to a datetime object
        date_time = datetime.strptime(str(self.shift_start), date_format)
        date_time2 = datetime.strptime(str(self.shift_actual_start), date_format)

        # # Create a datetime object
        # date_time = datetime()

        # Create a timedelta object representing a time duration
        time_delta = timedelta(hours=flt(date_diff))

        # Add the timedelta to the datetime
        new_date_time = date_time + time_delta

        # Print the result
        print("New date and time:", new_date_time)
        self.shift_end=new_date_time
        self.shift_actual_end=date_time2+timedelta(hours=flt(date_diff+1))