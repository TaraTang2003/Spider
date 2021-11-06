# -*- coding = utf-8 -*-
# @Time : 2021/10/29 17:47
# @Author : TX
# @File : module.py
# @Software : PyCharm

from flask import Flask,render_template
app = Flask(__name__)

@app.route('/index')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)