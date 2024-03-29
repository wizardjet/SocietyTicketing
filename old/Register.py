from tkinter import *
import csv

default_padding_x = 15
default_padding_y = 3
label_font = "Sans 9 bold"
entry_font = "Sans 9"
entry_width = 30

# master window
master = Tk()
master.title("SMIG App v0.9")
master.geometry('400x250')

def reg():
	# reg window
	top_reg = Toplevel(master)
	top_reg.title("Registration")
	top_reg.geometry('250x480')

	# First Name
	frame_fname = Frame(top_reg)
	frame_fname.grid(sticky = "W", padx=default_padding_x, pady=default_padding_y)
	Label(frame_fname, text="First Name", font=label_font).grid(column = 0, row = 0, sticky='W')
	v_fname = StringVar()
	txt_fname = Entry(frame_fname, width=entry_width, font=entry_font, textvariable = v_fname).grid(column = 0, row = 1, sticky='W')

	# Last Name
	frame_lname = Frame(top_reg)
	frame_lname.grid(sticky = "W", padx=default_padding_x, pady=default_padding_y)
	Label(frame_lname, text="Last/Family Name", font=label_font).grid(column = 0, row = 0, sticky='W')
	v_lname = StringVar()
	txt_lname = Entry(frame_lname, width=entry_width, font=entry_font, textvariable = v_lname).grid(column = 0, row = 1, sticky='W')

	# Course
	frame_course = Frame(top_reg)
	frame_course.grid(sticky = "W", padx=default_padding_x, pady=default_padding_y)
	Label(frame_course, text="Course", font=label_font).grid(column = 0, row = 0, sticky='W')
	v_course = StringVar()
	txt_course = Entry(frame_course, width=entry_width, font=entry_font, textvariable = v_course).grid(column = 0, row = 1, sticky='W')

	# Year of Study
	frame_year = Frame(top_reg)
	frame_year.grid(sticky = "W", padx=default_padding_x, pady=default_padding_y)
	Label(frame_year, text="Year of Study", font=label_font).grid(column = 0, row = 0, sticky='W')
	OPTIONS = ["", "1st Year", "2nd Year", "3rd Year", "4th Year", "Masters", "PhD", "Alumni"]
	v_year = StringVar(frame_year)
	v_year.set("1st Year")
	option_year = OptionMenu(frame_year, v_year, *OPTIONS).grid(column = 0, row = 1)

	# Email
	frame_email = Frame(top_reg)
	frame_email.grid(sticky = "W", padx=default_padding_x, pady=default_padding_y)
	Label(frame_email, text="Email (without the @st-andrews.ac.uk)", font=label_font).grid(column = 0, row = 0, sticky='W')
	v_email = StringVar()
	txt_email = Entry(frame_email, width=entry_width, font=entry_font, textvariable=v_email).grid(column = 0, row = 1, sticky='W')

	# Malaysian?
	frame_msian = Frame(top_reg)
	frame_msian.grid(sticky = "W", padx=default_padding_x, pady=default_padding_y)
	Label(frame_msian, text="Are you Malaysian?", font=label_font).grid(column = 0, row = 0, sticky='W')
	# Radio buttons
	radio_frame_msian = Frame(frame_msian)
	radio_frame_msian.grid(sticky = "W")
	v_msian = IntVar()
	v_msian.set(0)
	def Show_Msian_Choice():
		print(v_msian.get())
	radio1_msian = Radiobutton(radio_frame_msian, text="Yes", variable=v_msian, value=1, command=Show_Msian_Choice).grid(column = 0, row = 1)
	radio2_msian = Radiobutton(radio_frame_msian, text="No", variable=v_msian, value=0, command=Show_Msian_Choice).grid(column = 1, row = 1)

	# Membership?
	frame_member = Frame(top_reg)
	frame_member.grid(sticky = "W", padx=default_padding_x, pady=default_padding_y)
	Label(frame_member, text="Membership?", font=label_font).grid(column = 0, row = 0, sticky='W')
	# Radio buttons
	radio_frame_member = Frame(frame_member)
	radio_frame_member.grid(sticky = "W")
	v_member = IntVar()
	v_member.set(0)
	# Library ID / Student ID
	v_id = StringVar()
	v_id_type = IntVar()
	v_id_choices = ["Forgot ID", "Library (back of card)", "Student (front of card)"]

	def Get_ID():
		top_id = Toplevel(top_reg)
		top_id.title("Enter ID")

		# ID Type
		frame_id_type = Frame(top_id)
		frame_id_type.grid(sticky = "W", padx=default_padding_x, pady=default_padding_y)
		Label(frame_id_type, text="PLEASE PAY GBP 3", font="sans 14 bold").grid(column = 0, row = 0, sticky='W')
		Label(frame_id_type, text="FOR INTERNAL USE ONLY", font="sans 14 bold").grid(column = 0, row = 1, sticky='W')
		Label(frame_id_type, text="USE LIBRARY ID IF POSSIBLE", font="sans 14 bold").grid(column = 0, row = 2, sticky='W')
		Label(frame_id_type, text="ID Type", font=label_font).grid(column = 0, row = 3, sticky='W')
		# Radio buttons
		radio_frame_id_type = Frame(frame_id_type)
		radio_frame_id_type.grid(sticky = "W")
		v_id_type.set(1)
		def Show_ID_Type_Choice():
			print(v_id_type.get())
		radio1_id_type = Radiobutton(radio_frame_id_type, text=v_id_choices[0], variable=v_id_type, value=0, command=Show_ID_Type_Choice).grid(column = 1, row = 4)
		radio2_id_type = Radiobutton(radio_frame_id_type, text=v_id_choices[1], variable=v_id_type, value=1, command=Show_ID_Type_Choice).grid(column = 2, row = 4)
		radio3_id_type = Radiobutton(radio_frame_id_type, text=v_id_choices[2], variable=v_id_type, value=2, command=Show_ID_Type_Choice).grid(column = 3, row = 4)

		# ID
		frame_id = Frame(top_id)
		frame_id.grid(sticky = "W", padx=default_padding_x, pady=default_padding_y)
		Label(frame_id, text="Enter here", font=label_font).grid(column = 0, row = 0, sticky='W')
		# v_txt_id = StringVar()
		txt_id = Entry(frame_id, width=entry_width, font=entry_font, textvariable=v_id).grid(column = 0, row = 1, sticky='W')

		# OK button
		def Ok():
			if v_id != "":
				print(v_id.get())
			top_id.destroy()
		top_ok_btn = Button(top_id, text="OK", command=Ok)
		top_ok_btn.grid(sticky = "E", padx=default_padding_x)

		top_id.mainloop()

	def Show_Member_Choice():
		print(v_member.get())
		if v_member.get()==1:
			Get_ID()

	radio1_member = Radiobutton(radio_frame_member, text="Yes", variable=v_member, value=1, command=Show_Member_Choice).grid(column = 0, row = 1)
	radio2_member = Radiobutton(radio_frame_member, text="No", variable=v_member, value=0, command=Show_Member_Choice).grid(column = 1, row = 1)
	edit_btn = Button(radio_frame_member, text="Edit", command=Show_Member_Choice).grid(column = 2, row = 1)

	# Notes
	frame_notes = Frame(top_reg)
	frame_notes.grid(sticky = "W", padx=default_padding_x, pady=default_padding_y)
	Label(frame_notes, text="Notes", font=label_font).grid(column = 0, row = 0, sticky='W')
	v_notes = StringVar()
	txt_notes = Entry(frame_notes, width=entry_width, font=entry_font, textvariable=v_notes).grid(column = 0, row = 1, sticky='W')

	def Get_Details():
		fname = "Empty"
		lname = "Empty"
		course = "Empty"
		year = "Empty"
		email = "Empty"
		msian = "No"
		member = "No"
		id_type = "N/A"
		uid = "N/A"
		notes = "Empty"
		if v_fname != "":
			fname = v_fname.get()
		if v_lname != "":
			lname = v_lname.get()
		if v_course != "":
			course = v_course.get()
		if v_year != "":
			year = v_year.get()
		if v_email != "":
			email = v_email.get()
		if v_msian:
			if v_msian.get():
				msian = "Yes"
		if v_member:
			if v_member.get():
				member = "Yes"
				if v_id_type:
					id_type = v_id_choices[v_id_type.get()]
				if v_id != "":
					uid = v_id.get()
		if v_notes != "":
			notes = v_notes.get()
		return {
			"First Name": fname,
			"Last Name": lname,
			"Course": course,
			"Year of Study": year,
			"Email": email,
			"Malaysian": msian,
			"Membership": member,
			"ID Type": id_type,
			"ID": uid,
			"Notes": notes}

	# Confirm details
	def Confirmation_Window():
		top_confirm = Toplevel(top_reg)
		top_confirm.title("Confirm details")
		top_confirm.geometry("450x400")

		Label(top_confirm, text="PLEASE CONFIRM THE DETAILS BELOW", font="sans 14 bold").grid(padx=default_padding_x, pady=default_padding_y, column = 0, row = 0, sticky='W')
		smiglet = Get_Details()
		index = 1
		for att in smiglet:
			Label(top_confirm, text = str(att) + ": " + smiglet[att], font=label_font).grid(padx=default_padding_x, pady=default_padding_y, column = 0, row = index, sticky='W')
			index = index + 1

		yes_or_no = 0
		def Yes():
			print(smiglet)
			# submit information
			with open('smiglets.csv', 'a') as csvFile:
				writer = csv.writer(csvFile)
				writer.writerow(smiglet.values())
				csvFile.close()
				print("Write confirmed")
			top_reg.destroy()
		def No():
			top_confirm.destroy()
		# Yes

		frame_yesno = Frame(top_confirm)
		frame_yesno.grid(sticky = "W", padx=default_padding_x, pady=default_padding_y)
		yes_btn = Button(frame_yesno, text="Correct", fg="white", bg="green", width=10, command=Yes)
		yes_btn.grid(sticky = "W", padx=default_padding_x, column=0, row=0)
		# No
		no_btn = Button(frame_yesno, text="Incorrect", fg="white", bg="red", width=10, command=No)
		no_btn.grid(sticky = "E", padx=default_padding_x, column=1, row=0)
		top_confirm.mainloop()

	# submit button
	submit_btn = Button(top_reg, text="Submit", command=Confirmation_Window)
	submit_btn.grid(sticky = "E", padx=default_padding_x, pady=default_padding_y)

	top_reg.mainloop()

# start program
new_smiglet_btn = Button(master, fg="white", bg="green", font=label_font, height = 3, width = 15, text = "Add new SMIGlet", command=reg).pack(fill="none", expand=True)
master.mainloop()
