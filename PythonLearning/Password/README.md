# Password

## 设计目的

- 实现一个简单轻量级的密码库，用以存储用户密码。

## 功能

- 支持按Key：Name：Password进行加密存储用户名和密码到txt文件中。（如：Steam：王大锤：123）
- 支持按Key查询。直接返回明文用户密码，不显示用户名。Tips：Key保证唯一性，即一个App只存一个用户名和密码。
- 支持KeyList。 返回已经存储过的KeyList
- 支持修改Key的密码。Key：NewPassword 即可。（如：Steam：456）
- 支持配置个人的加密方式。

## 配置文件
