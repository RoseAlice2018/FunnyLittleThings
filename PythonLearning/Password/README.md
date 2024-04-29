# Password

## 设计目的

- 实现一个简单轻量级的密码库，用以存储用户密码。

## 功能

- 支持按AppName：UserName：Password进行加密存储用户名和密码到txt文件中。（如：Steam：王大锤：123）
- 支持按Key（AppName）查询。直接返回明文用户密码，不显示用户名。Tips：Key保证唯一性，即一个App只存一个用户名和密码。
- 支持KeyList。 返回已经存储过的KeyList（AppNameList）
- 支持修改Key（AppName）的密码。Key：NewPassword 即可。（如：Steam：456）
- 支持配置个人的加密方式。

## 配置文件

```
loglevel: debug
path: H:\Work\pasworddatabase\Password.txt

```

- log_level: 日志等级
- path：database存储的路径

- [X] 4.29.2024 完成支持AppName的更新
- [X] 4.29.2024 完成基本加密算法
- [X] 4.29.2024 完成支持KeyList查询
- [ ] 完成基本功能后，写一篇Blog

## 未来工作

* [ ] 优化界面（目前的界面风格过于丑陋）
* [ ] 支持Password的云端布置，手机端和PC端的共享数据。
* [ ] 支持依据用户Key生成特定加密算法，并且在用户输入特定Key之后才能正确解压PassWord
* [ ] 手机端App
* [ ] Linux系统一键布置
