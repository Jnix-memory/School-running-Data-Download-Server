#!/usr/bin/env python3
"""
改进的后端服务，使用多线程服务器和SQLite数据库存储数据
"""

import http.server
import socketserver
import json
import os
import sys
import sqlite3
import threading
import time

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

PORT = 5005

# 数据库文件路径
DB_PATH = 'activities.db'

# 数据库锁，确保线程安全
db_lock = threading.Lock()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """多线程HTTP服务器"""
    pass

def init_db():
    """初始化数据库"""
    with db_lock:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # 创建活动表
        c.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            duration TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()
        conn.close()

def insert_activity(user_id, date, start_time, duration):
    """插入活动数据"""
    with db_lock:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "INSERT INTO activities (user_id, date, start_time, duration) VALUES (?, ?, ?, ?)",
            (user_id, date, start_time, duration)
        )
        activity_id = c.lastrowid
        conn.commit()
        conn.close()
        return activity_id

def get_activities():
    """获取所有活动数据"""
    with db_lock:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, user_id, date, start_time, duration, created_at FROM activities ORDER BY created_at DESC")
        activities = []
        for row in c.fetchall():
            activities.append({
                'id': row[0],
                'user_id': row[1],
                'date': row[2],
                'start_time': row[3],
                'duration': row[4],
                'created_at': row[5]
            })
        conn.close()
        return activities

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 提供前端页面
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('frontend/form.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/favicon.ico':
            # 处理favicon.ico请求
            self.send_response(404)
            self.end_headers()
        elif self.path == '/api/activities':
            # 获取活动数据
            try:
                activities = get_activities()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(activities).encode())
            except Exception as e:
                print(f"Error: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': '服务器内部错误'}).encode())
        elif self.path == '/form.html':
            # 提供表单页面
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('frontend/form.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/download.html':
            # 提供下载页面
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('frontend/download.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            try:
                # 调用父类的do_GET方法处理其他GET请求
                super().do_GET()
            except Exception as e:
                # 处理异常，避免服务器崩溃
                print(f"Error: {e}")
                self.send_response(404)
                self.end_headers()
    
    def do_POST(self):
        try:
            if self.path == '/api/submit':
                # 读取请求体
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                
                # 获取参数
                user_id = data.get('user_id')
                date = data.get('date')
                start_time = data.get('start_time')
                duration = data.get('duration')
                
                if not all([user_id, date, start_time, duration]):
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': '缺少必要参数'}).encode())
                    return
                
                # 插入数据到数据库
                activity_id = insert_activity(user_id, date, start_time, duration)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'id': activity_id}).encode())
            elif self.path == '/api/generate':
                # 读取请求体
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                
                # 获取参数
                user_id = data.get('user_id')
                date = data.get('date')
                start_time = data.get('start_time')
                duration = data.get('duration')
                
                if not all([user_id, date, start_time, duration]):
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': '缺少必要参数'}).encode())
                    return
                
                # 导入生成FIT文件的函数
                import sys
                sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                from tools.generate_fit import generate_fit
                
                # 生成FIT文件
                success = generate_fit(user_id, date, start_time, duration)
                
                if success:
                    # 读取生成的文件
                    output_path = f'{user_id}.fit'
                    if os.path.exists(output_path):
                        self.send_response(200)
                        self.send_header('Content-type', 'application/octet-stream')
                        self.send_header('Content-Disposition', f'attachment; filename={user_id}.fit')
                        self.end_headers()
                        with open(output_path, 'rb') as f:
                            self.wfile.write(f.read())
                        # 删除生成的文件
                        os.remove(output_path)
                    else:
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({'error': '文件生成失败'}).encode())
                else:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': '文件生成失败'}).encode())
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            # 处理异常，避免服务器崩溃
            print(f"Error: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': '服务器内部错误'}).encode())
    
    def end_headers(self):
        # 添加CORS头
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

# 确保在正确的目录中运行
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 初始化数据库
init_db()

# 使用多线程服务器
with ThreadedHTTPServer(('', PORT), MyHTTPRequestHandler) as httpd:
    print(f"后端服务运行在 http://localhost:{PORT}")
    print("使用多线程服务器，支持并发请求")
    print("数据存储在SQLite数据库中，支持多设备共享")
    httpd.serve_forever()