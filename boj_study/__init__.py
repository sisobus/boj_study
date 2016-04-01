#!/usr/bin/python
#-*- coding:utf-8 -*-
from flask import Flask, render_template, request, redirect
import json
import glob
from operator import itemgetter
import os
import datetime
import random
from bs4 import BeautifulSoup
import urllib,urllib2
import cookielib

app = Flask(__name__)

def get_all_date_list():
    base_directory_path = '/var/www/boj_study/boj_study/data/problems/'
    date_paths  = glob.glob(base_directory_path+'*')
    date_list   = []
    for date_path in date_paths:
        date_list.append(date_path.split('/')[-1])
    return date_list

def get_problem_list_with_date(cur_date):
    base_directory_path = '/var/www/boj_study/boj_study/data/problems/'
    date_file_path = base_directory_path + cur_date
    l = []
    with open(date_file_path,'r') as fp:
        l = fp.read().strip().split()
    return l

def get_all_user_list():
    base_directory_path = '/var/www/boj_study/boj_study/data/users/'
    user_paths  = glob.glob(base_directory_path+'*')
    user_list   = []
    for user_path in user_paths:
        user_list.append(user_path.split('/')[-1])
    return user_list

def convert_problems(user_id,problems):
    # is solve : 1
    # none : 0
    # fail : -1
    with open('/var/www/boj_study/boj_study/data/status/'+user_id+'.json','r') as fp:
        status = json.loads(fp.read())
    
    solved = []
    failed = []
    if 'solved' in status:
        solved = status['solved']
    if 'failed' in status:
        failed = status['failed']
    ret = []
    for problem in problems:
        mask = 0
        if problem in solved:
            mask = 1
        elif problem in failed:
            mask = -1
        d = {
            'problem_id': problem,
            'status': mask
                }
        ret.append(d)
    return ret

@app.route('/',methods=['GET'])
def home():
    user_list = get_all_user_list()
    date_list = get_all_date_list()
    posts = []
    number_of_total_problem = 0
    for date_item in date_list:
        problem_list = get_problem_list_with_date(date_item)
        number_of_total_problem += len(problem_list)
        users = []
        for user_item in user_list:
            d = {
                    'user_id': user_item,
                    'problems': convert_problems(user_item,problem_list)
                    }
            users.append(d)
        d = {
                'users': users,
                'date': date_item
                }
        posts.append(d)

    ret = {
            'posts': posts,
            'number_of_total_problem': number_of_total_problem
            }
    html_code = render_template('home.html',ret=ret)
    return html_code

if __name__ == '__main__':
    app.run(host='1.226.82.204',debug=True)
