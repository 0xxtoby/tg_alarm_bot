# -*- coding: utf-8 -*-
import configparser
import datetime
import logging
import sqlite3
from utils import setup_logging

config = configparser.ConfigParser()
config.read('./config.ini')

setup_logging(level=logging.INFO)

class TG_DB(object):
    def __init__(self):
        # 打开数据库连接
        self.db = sqlite3.connect(database=config.get('db_config', 'db_name'),)
        self.cursor = self.db.cursor()

        #如果没有表就创建表
        re=self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alarm_info_2'")

        # If the result is empty, the table does not exist
        if not re.fetchone():
            sql='''create table alarm_info_2(
    alarm_id    integer
        constraint alarm_info_2_pk
            primary key autoincrement,
    chat_id     text,
    message_id  text,
    rule_id     integer,
    create_time datetime,
    update_time datetime
);
'''
            self.cursor.execute(sql)
            logging.info("sqlite table alarm_info_2 created")


        re = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rule'")

        # If the result is empty, the table does not exist
        if not re.fetchone():
            sql = '''create table rule(
            rule_id    integer
                constraint alarm_info_2_pk
                    primary key autoincrement,
            rule     text
        );
        '''
            self.cursor.execute(sql)
            logging.info("sqlite table rule created")


    def close(self):
        self.cursor.close()


    def insert_alarm_info_2(self, re_id,message_id,chat_id):

        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_time= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql="INSERT INTO alarm_info_2 (`alarm_id`,`rule_id`,`chat_id`,`message_id`,`create_time`,`update_time` )VALUES (null, '{}','{}', '{}', '{}','{}');".format(
            re_id,
            chat_id,
            message_id,
            create_time,
            update_time

        )
        logging.debug(sql)
        self.cursor.execute(sql)
        self.db.commit()


    def get_rule_info_s(self):
        sql="SELECT rule_id,rule FROM rule"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    def add_rule_info(self,rule):
        sql="INSERT INTO rule (`rule_id`,`rule`) VALUES (null, '{}');".format(rule)
        self.cursor.execute(sql)
        self.db.commit()
    def delete_rule_info(self,rule_id):
        sql="DELETE FROM rule WHERE `rule_id` = '{}';".format(rule_id)
        self.cursor.execute(sql)
        self.db.commit()
    def get_rule_info(self,rule_id):
        sql="SELECT rule_id,rule FROM rule WHERE `rule_id` = '{}';".format(rule_id)
        self.cursor.execute(sql)
        return self.cursor.fetchall()


if __name__ == '__main__':
    db=TG_DB()
    print(db.get_rule_info_s())
    print(len(db.get_rule_info(8)))
