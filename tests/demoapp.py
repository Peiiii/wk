import wk
from wk.web import Application,request,parse_args
from wk.extra import node
from flask import *
import jieba
import os,shutil,glob,re
files_dir=r'E:\LearningResources\高中学习交流群资源'

from wk.web.applications.FileServer import FileServer

app=FileServer(__name__,serve_root=files_dir)

app.run()

