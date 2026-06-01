import tkinter as tk
from tkinter import messagebox
from logic import accounts, add_account, edit_account, delete_account, calculate, validate, save_accounts, load_accounts, save_window_size, load_window_size

root = tk.Tk()


root.title("Paycheck Splitter")

#-----Top Frame-------
def run_calculate():
    try:
        total = float(total_entry.get())
    except ValueError:
        messagebox.showerror('Error', 'Please enter a valid number')
        return
    
    error = validate(total)
    if error:
        messagebox.showerror('Error', error)
    else:
        calculate(total)
        save_accounts()
        refresh_accounts()

    
top_frame = tk.Frame(root)
top_frame.grid(row=0, column=0)

total_label = tk.Label(top_frame, text="Total:")
total_label.grid(row=0,column=0)

total_entry = tk.Entry(top_frame)
total_entry.grid(row=0, column=1)

calculate_button = tk.Button(top_frame, text="Calculate", command=run_calculate)
calculate_button.grid(row=0, column=2)



#-----Middle Frame------
middle_frame = tk.Frame(root)
middle_frame.grid(row=1, column=0)

tk.Label(middle_frame, text="Account Name").grid(row=0, column=0)

tk.Label(middle_frame, text="Type").grid(row=0, column=1)

tk.Label(middle_frame, text="Amount").grid(row=0, column=2)

tk.Label(middle_frame, text="Result").grid(row=0, column=3)

def open_edit_account(acc):
    edit_top = tk.Toplevel(root)
    edit_top.title('Edit Account')
    edit_top.geometry('250x250')

    edit_top.focus_set()

    var_type = tk.StringVar(master=edit_top, name='edit_var_type', value=acc['var_type'])

    account_name_label = tk.Label(edit_top, text="Account Name:")
    account_name_label.grid(row=0, column=0)

    account_name_entry = tk.Entry(edit_top)
    account_name_entry.grid(row=0, column=1)

    fixed_rb = tk.Radiobutton(edit_top, text='Fixed', variable=var_type, value="fixed")
    fixed_rb.grid(row=1, column=0)

    percent_rb = tk.Radiobutton(edit_top, text='Percent', variable=var_type, value="percent")
    percent_rb.grid(row=2, column=0)

    value_entry = tk.Entry(edit_top)
    value_entry.grid(row=1, column=1)

    account_name_entry.insert(0, acc['name'])
    value_entry.insert(0, acc['amount'])


    def set_rb():
        if acc['var_type'] == 'fixed':
            percent_rb.deselect()
            fixed_rb.select()
        else:
            fixed_rb.deselect()
            percent_rb.select()

    edit_top.after(100, set_rb)

    def save_edit():
        edit_account(
            acc['name'],
            new_name=account_name_entry.get(),
            new_var_type=var_type.get(),
            new_amount=float(value_entry.get())
        )
        save_accounts()
        refresh_accounts()

    def close_popup():
        edit_top.destroy()

    tk.Button(edit_top, text='Save', command=save_edit).grid(row=3, column=0)
    tk.Button(edit_top, text='Done', command=close_popup).grid(row=3, column=1)


def refresh_accounts():
    global middle_frame
    for widget in middle_frame.winfo_children():
        widget.destroy()
    
    tk.Label(middle_frame, text="Account Name").grid(row=0, column=0)

    tk.Label(middle_frame, text="Type").grid(row=0, column=1)

    tk.Label(middle_frame, text="Amount").grid(row=0, column=2)

    tk.Label(middle_frame, text="Result").grid(row=0, column=3)

    for i, acc in enumerate(accounts):
        name_label = tk.Label(middle_frame, text=acc['name'])
        name_label.grid(row=i+1, column=0)

        var_type_label = tk.Label(middle_frame, text=acc['var_type'])
        var_type_label.grid(row=i+1, column=1)

        amount_label = tk.Label(middle_frame, text=acc['amount'])
        amount_label.grid(row=i+1, column=2)

        result_label = tk.Label(middle_frame, text=acc['result'])
        result_label.grid(row=i+1, column=3)

        def delete(name=acc['name']):
            delete_account(name)
            save_accounts()
            refresh_accounts()

        def edit(a=acc):
            open_edit_account(a)

        edit_button = tk.Button(middle_frame, text='Edit', command=edit)
        edit_button.grid(row=i+1, column=4)

        delete_button = tk.Button(middle_frame, text='Delete', command=delete)
        delete_button.grid(row=i+1, column=5)



#----Top Frame----
def open_add_account():
    top = tk.Toplevel(root)
    top.title("Add Account")
    top.geometry('250x250')

    top.focus_set()

    account_name_label = tk.Label(top, text="Account Name:")
    account_name_label.grid(row=0, column=0)

    account_name_entry = tk.Entry(top)
    account_name_entry.grid(row=0, column=1)

    var_type = tk.StringVar(value="fixed")

    fixed_rb = tk.Radiobutton(top, text="Fixed", variable=var_type, value="fixed")
    fixed_rb.grid(row=1, column=0)

    percent_rb = tk.Radiobutton(top, text="Percent", variable=var_type, value="percent")
    percent_rb.grid(row=2, column=0)

    value_entry = tk.Entry(top)
    value_entry.grid(row=1, column=1)

    
    
    def create_account():
        name = account_name_entry.get()
        value = value_entry.get()
        acc_type = var_type.get()

        errors=[]

        if not name:
            errors.append("Please enter a name.")

        if not value:
            errors.append("Please enter a value.")

        if not value.isdigit():
            errors.append("The value is not a digit.")

        if errors:
            messagebox.showerror('Error', '\n'.join(errors))
            top.focus_set()

        else:
            add_account(name, acc_type, float(value))
            save_accounts()
            refresh_accounts()

    def close_popup():
        top.destroy()

    create_button = tk.Button(top, text='Create', command=create_account)
    create_button.grid(row=3, column=0)

    done_button = tk.Button(top, text='Done', command=close_popup)
    done_button.grid(row=3, column=1)

#----Bottom Frame----
bottom_frame = tk.Frame(root)
bottom_frame.grid(row=2, column=0)

add_account_button = tk.Button(bottom_frame, text="Add Account", command=open_add_account)
add_account_button.grid(row=0, column=0)

size = load_window_size()
root.geometry(f"{size['width']}x{size['height']}")

def on_close():
    print("cosing, saving save", root.winfo_width(), root.winfo_height())
    save_window_size(root.winfo_width(), root.winfo_height())
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

load_accounts()
refresh_accounts()
root.mainloop()