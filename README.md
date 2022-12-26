# TG群组、频道敏感词检测  转发到告警群

使用[Pyrogram](https://github.com/pyrogram/pyrogram)框架实现Telegram 客户端

## 使用

配置config.ini

```
[tg_api]
;https://my.telegram.org/apps 注册得到 api_id 和 apt_hash
api_id = 12345678
api_hash= 123456789012345678901234567890123
;session_db name
name = my

[groups]
;告警转发到的群
alarm_group= https://t.me/+pxxxxxxxxxxx

[db_config]
db_name = ./tg_bot.db
```

## 功能

```
/rule 查看规则列表
/group 查看监控群组
/add [规则] 添加规则
/del [rule_id]  删除规则
/join [url]  添加群
```

