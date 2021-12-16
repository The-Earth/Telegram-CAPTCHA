# Telegram-CAPTCHA

一个 Telegram 入群验证机器人。机器人的设计来自 [fossifer 的入群验证机器人](https://github.com/fossifer/Telegram-CAPTCHA-bot) 。在其基础上，改用 [catbot 框架](https://github.com/The-Earth/catbot) ，并避免 Telegram 大型群组中没有入群消息带来的问题。本机器人配置文件示例中的文本也来自 fossifer 的设计。除 fossifer 的原设计之外，这个机器人还可设置用户名黑名单，当用户名匹配规则时不进行验证而直接踢出，可用于处理明显的广告机器人。另外，针对有些群管会直接将用户踢出的操作，为了避免冲突，机器人检测到群管的操作之后会自行删除验证。

## 自行运行机器人

确保 Python 版本为 3.7 以上。复制源代码到本地，安装 catbot：

```
pip install -r requirements.txt
```

将 `config_example.json` 复制到 `config.json`，打开并填入您的 Bot Token。按需要修改 `proxy` 参数及提示文本，以及用户名黑名单。然后运行：`main.py`。

机器人开始运行后，将机器人加入您的群组，并授予 ban user 权限。

## 已知问题

目前在恢复有权限限制人员旧有禁言期时，会把权限直接设置成禁言，而非按之前的权限进行设置。考虑到群组管理实践中，较少出现这种情况，加上试图利用退群重进来绕过限制是恶劣行为，所以此项问题的修复列为低优先级。
