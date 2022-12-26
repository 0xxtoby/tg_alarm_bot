# -*- coding: utf-8 -*-
import logging
from pyrogram import Client, filters
from db_utils import TG_DB
from utils import setup_logging
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
alarm_group=config.get('groups', 'alarm_group')

setup_logging(level=logging.INFO)
app = Client(api_id=config.get('tg_api', 'api_id'),
             name=config.get('tg_api', 'name'),
             api_hash=config.get('tg_api', 'api_hash'),

             )
db=TG_DB()


@app.on_message()
async def echo(client, message):
     logging.info("{} {} {} {}".format(message.chat.title ,message.chat.id, message.text or message.caption,message.id))

     message_text=message.text if message.text else ""
     caption=message.caption if message.caption else ""

     rule_list = db.get_rule_info_s()
     for re_id,rule in rule_list :
         if rule in message_text or rule in caption:
             if str(message.chat.id) != alarm_group:
                 db.insert_alarm_info_2(re_id=re_id, message_id=message.id,chat_id=message.chat.id)
                 logging.info("reid=" + rule + ",chat_id" + str(message.chat.id) + " " + message_text)

                 await message.forward(chat_id=int(alarm_group))

     if str(message.chat.id)== alarm_group:
        if "/rule" in message_text:
            send_str=''
            for re_id, rule in rule_list:
                send_str+=str(re_id) + ' ' + rule + '\n'
            logging.info(send_str)

            await message.reply(send_str)
        elif "/group" in message_text:
            send_str=''
            async for group in app.get_dialogs():
                send_str+="{} {}\n".format(group.chat.title  or group.chat.first_name,group.chat.id,)

            await message.reply(send_str)
            logging.info("reply_message\n" + send_str)
        elif "/del" in message_text:
            send_str=''
            rule_id=message_text.split(" ")[-1]
            try:
                int(rule_id)
                try:
                    TTT=db.get_rule_info(rule_id)
                except:
                    await message.reply("No such rule")
                    return
                if TTT== 1:
                    db.delete_rule_info(rule_id)
                    await message.reply("delete success")

            except:
                await message.reply("Invalid rule id")
                return
        elif "/add" in message_text:
            send_str=''
            try:
                 rule=message_text.split(" ")[1]
            except:
                await message.reply("Invalid rule")
                return
            db.add_rule_info(rule)
            await message.reply("add success")
        elif "/join" in message_text:
            try:
                 group_link= message_text.split("/")[-1]
            except:
                 await message.reply("Invalid group link")
                 return
            try:
                join_chat = await app.join_chat(group_link)
            except:
                await message.reply("Invalid group link")
                return
            if not join_chat:
                await message.reply("Invalid group link")
                return
            await message.reply("join success")

app.run()