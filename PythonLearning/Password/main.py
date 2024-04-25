import tkinter as tk
import yaml
from cryptography.fernet import Fernet


# 读取配置
with open("config.yaml", 'r') as config_file:
    config = yaml.safe_load(config_file)

log_level = config['loglevel']
path = config['path']

print(f"LogLevel: {log_level}")
print(f"Path: {path}")

# 创建主窗口
root = tk.Tk()

# 设置窗口标题
root.title("Password数据库")

# 设置窗口大小
root.geometry("300x200")

# 创建一个标签控件并添加到主窗口
label = tk.Label(root, text="欢迎使用Password数据库")
label.pack()


# 创建三个文本框用以输入Password和Key：如Epic等
key_entry = tk.Entry(root)
key_entry.pack()

password_entry = tk.Entry(root)
password_entry.pack()

app_name_entry = tk.Entry(root)
app_name_entry.pack()

# 创建一个文本框用以显示查询的key
query_entry = tk.Entry(root)
query_entry.pack()

# 创建一个文本框用以显示解密后的密码
decrypted_password = tk.Entry(root)
decrypted_password.pack()

# 创建一个按钮控件并添加到主窗口
def on_button_click():
    password = password_entry.get()
    key = key_entry.get()
    app_name = app_name_entry.get()
    
    # 加密内容
    encry_key = key
    encry_password = password
    encry_app_name = app_name

    # 保存到txt文件里
    with open(path, "w") as file:
        file.write(f"Encry_key:{encry_key}\n")
        file.write(f"Encry_app_name:{encry_app_name}\n")
        file.write(f"Encry_password:{encry_password}\n")

# 创建一个查询按钮
def on_query_button_click():
    key = query_entry.get()
    with open(path, "r") as file:
        lines = file.readlines()
        encrypted_key = lines[0].strip().split(": ")[1]
        encrypted_app_name = lines[1].strip().split(": ")[1]
        encrypted_password = lines[2].strip().split(": ")[2]

    if encrypted_key == key:
        decrypted_password.delete(0, tk.END)
        decrypted_password.insert(0, decrypted_password)
    else:
        decrypted_password.delete(0, tk.END)
        decrypted_password.insert(0, "INVALID KEY")
        
    

button = tk.Button(root, text="提交", command=on_button_click)
button.pack()

query_button = tk.Button(root, text="查询", command=on_query_button_click)
query_button.pack()

# 进入消息循环
root.mainloop()