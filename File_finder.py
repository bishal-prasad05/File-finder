from tkinter import *
import os
import customtkinter
from tkinter import messagebox
import threading
import clipboard

root=customtkinter.CTk()
root.geometry("550x300+650+200")
root.title("File_Finder")

def on_closing():
	os._exit(0)
root.protocol("WM_DELETE_WINDOW", on_closing)

is_thread_running=0
cancel_variable=0
absolute_path=[]
file_without_abs_path=[]

def find():
	global is_thread_running,cancel_variable,absolute_path,file_without_abs_path
	searched_value=entry.get()
	if searched_value.isspace() or searched_value=="" or searched_value==None:
		is_thread_running=0
		return
	messagebox.showinfo("Info","Please wait the app is searching your file --- It will take minimum 10 seconds")
	absolute_path=[]
	file_without_abs_path=[]
	index=0
	listbox.delete(0,END)
	drives = [ chr(x) + ":" for x in range(65,91) if os.path.exists(chr(x) + ":") ]
	for i in drives:
		root.update()
		for root1, dirs, files in os.walk(i+"\\"):
			if cancel_variable==1:
					cancel_variable=0
					is_thread_running=0
					messagebox.showwarning("Info","Search cancelled by you")
					return
			root.update()
			for file in files:
				if cancel_variable==1:
					cancel_variable=0
					is_thread_running=0
					messagebox.showwarning("Info","Search cancelled by you")
					return
				root.update()
				if searched_value.lower() in file.lower():
					absolute_path.append(root1)
					file_without_abs_path.append(file)
					listbox.insert(index,str(index+1)+". "+file)
					index+=1
	if index==0:
		messagebox.showinfo("Info",f"Searched completed ----- No file found with the name {searched_value}")
	else:
		messagebox.showinfo("Info","Searched completed")
	is_thread_running=0
	return

def  to_start_thread():
	global is_thread_running
	if is_thread_running==1:
		messagebox.showerror("Info","The app is searching one file please wait")
	else:
		is_thread_running=1
		threading.Thread(target=find).start()

def cancel():
	global cancel_variable,is_thread_running
	if is_thread_running==1:
		cancel_variable=1
	else:
		cancel_variable=0

current_selection=None
def callback(event):
	global current_selection	
	try:
		selection=event.widget.curselection()
		if selection:
			index=selection[0]
			current_selection=index
	except:
		pass

def call_listbox(ev):
	global current_selection,absolute_path
	if current_selection==None:
		return
	path = absolute_path[current_selection]
	path = os.path.realpath(path)
	os.startfile(path)

def copy():
	global current_selection,absolute_path,file_without_abs_path
	if current_selection==None:
		return
	clipboard.copy(absolute_path[current_selection]+"\\"+file_without_abs_path[current_selection])

def open_with_default_app():
	global current_selection,absolute_path
	if current_selection==None:
		return
	path = absolute_path[current_selection]+"\\"+file_without_abs_path[current_selection]
	path = os.path.realpath(path)
	os.startfile(path)

def do_popup(event):
	try:
		m.tk_popup(event.x_root, event.y_root)
	finally:
		m.grab_release()

m = Menu(root,bg="#f2f2f2", tearoff = 0,font=10)
m.add_command(label ="Copy Absolute path",command=copy)
m.add_command(label ="Open with default app",command=open_with_default_app)
m.add_command(label="open in file explorer",command=lambda :call_listbox("ev"))

search_frame=customtkinter.CTkFrame(root)
search_frame.pack(side=TOP)
entry=customtkinter.CTkEntry(search_frame,width=300,placeholder_text="Type the filename")
entry.pack(side=LEFT,padx=10,pady=10)
button=customtkinter.CTkButton(search_frame,text="Search",command=to_start_thread)
button.pack(side=LEFT)
cancel_button=customtkinter.CTkButton(search_frame,text="Cancel",command=cancel)
cancel_button.pack(side=LEFT,padx=5)
listbox=Listbox(root,border=0,background="#333333",font=30,fg="white")
listbox.pack(side=BOTTOM,expand=TRUE,fill=BOTH,padx=10,pady=10)
listbox.bind("<<ListboxSelect>>",callback)
listbox.bind("<Double-1>",call_listbox)
listbox.bind("<Button-3>",do_popup)
root.mainloop()