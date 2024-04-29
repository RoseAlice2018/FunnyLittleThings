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
label.grid(row=0, column=0)


# 创建三个文本框用以输入Password和Key：如Epic等
Username_label = tk.Label(root, text="UserName：")
Username_label.grid(row=1, column=0)

UserName_entry = tk.Entry(root)
UserName_entry.grid(row=1, column=1)

password_label = tk.Label(root, text="PassWord: ")
password_label.grid(row=2, column=0)

password_entry = tk.Entry(root)
password_entry.grid(row=2, column=1)

app_name_label = tk.Label(root, text="AppName: ")
app_name_label.grid(row=3, column=0)

app_name_entry = tk.Entry(root)
app_name_entry.grid(row=3, column=1)

# 创建一个文本框用以显示查询的key
query_label = tk.Label(root, text="QueryAppName: ")
query_label.grid(row=4, column=0)

query_entry = tk.Entry(root)
query_entry.grid(row=4, column=1)

# 创建一个文本框用以显示解密后的密码
decrypted_password_label = tk.Label(root, text="解压后密码是: ")
decrypted_password_label.grid(row=5, column=0)

decrypted_password = tk.Entry(root)
decrypted_password.grid(row=5, column=1)

# 创建一个按钮控件并添加到主窗口
def on_button_click():
    password = password_entry.get()
    UserName = UserName_entry.get()
    app_name = app_name_entry.get()
    
    # 加密内容
    encry_user_name = UserName
    encry_password = password
    encry_app_name = app_name

    # 追加写保存到txt文件里
    # TODO: 如果AppName已经存在需要更新AppName对应的记录
    with open(path, "a+") as file:
        file.write(f"Encry_UserName:{encry_user_name}\n")
        file.write(f"Encry_app_name:{encry_app_name}\n")
        file.write(f"Encry_password:{encry_password}\n")

# 创建一个查询按钮
def on_query_button_click():
    key = query_entry.get()
    with open(path, "r") as file:
        lines = file.readlines()

        # 取出3行处理
        for i in range(0, len(lines), 3):
            group = lines[i:i+3]
            encrypted_user_name = group[0].strip().split(":")[1]
            encrypted_app_name = group[1].strip().split(":")[1]
            encrypted_password = group[2].strip().split(":")[1]

            if encrypted_app_name == key:
                decrypted_password.delete(0, tk.END)
                decrypted_password.insert(0, encrypted_password)
            else:
                decrypted_password.delete(0, tk.END)
                decrypted_password.insert(0, "INVALID KEY")
        
    

button = tk.Button(root, text="提交", command=on_button_click)
button.grid(row=6, column=0)

query_button = tk.Button(root, text="查询", command=on_query_button_click)
query_button.grid(row=7, column=0)

# 进入消息循环
root.mainloop()