import json
import os

app_data = os.getenv('APPDATA')
save_dir = os.path.join(app_data, 'PaycheckSplitter')
os.makedirs(save_dir, exist_ok=True)
save_path= os.path.join(save_dir, 'accounts.json')



accounts = []

def add_account(name, var_type, value):
    
    account = {
        "name": name,
        "var_type": var_type,
        "amount": float(value),
        "result":0,
    }

    accounts.append(account)

def edit_account(name, new_name=None, new_var_type = None, new_amount=None):
    for acc in accounts:
        if acc["name"] == name:
            if new_name:
                acc["name"] = new_name
            if new_var_type:
                acc["var_type"] = new_var_type
            if new_amount:
                acc["amount"] = new_amount
            return

def delete_account(name):
    for acc in accounts:
        if acc["name"] == name:
            accounts.remove(acc)
            return

def calculate(total):
    remaining = total

    for acc in accounts:
        if acc["var_type"] == "fixed":
            acc["result"] = acc["amount"]
            remaining = remaining - float(acc["amount"])

    for acc in accounts:
        if acc["var_type"] == "percent":
            acc_amount = remaining * float(acc["amount"]) / 100

            acc["result"] = acc_amount

def validate(total):
    total_fixed = 0
    total_percent = 0

    for acc in accounts:
        if acc["var_type"] == "fixed":
            total_fixed += acc["amount"]
        else:
            total_percent += acc["amount"]
    
    if total_percent > 100:
        return "Percentages exceed 100%"
    
    if total_fixed > total or (total_fixed == total and total_percent > 0):
        return "Amount exceed the total"
    
    remaining = total - total_fixed
    percent_total = remaining * total_percent / 100

    if round(total_fixed + percent_total) != round(total):
        return "Amounts do not add up to the total"
    
    return None

def save_accounts():
    with open(save_path, "w") as f:
        json.dump(accounts, f)

def load_accounts():
    global accounts
    try:
        with open(save_path, "r") as f:
            data = json.load(f)
            accounts.extend(data)

    except FileNotFoundError:
        pass

def save_window_size(width, height):
    size_path = os.path.join(save_dir, 'settings.json')
    with open(size_path, 'w') as f:
        json.dump({'width': width, 'height': height}, f)

def load_window_size():
    size_path = os.path.join(save_dir, 'settings.json')
    try:
        with open(size_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'width': 300, 'height': 300}
