School-running-Data-Download-Server
一个为满足校园跑步需求而设计的运动数据生成服务端。它可以基于现有运动数据，生成包含GPS轨迹的自定义运动时长和距离的 .fit 文件，适用于Keep等支持导入FIT文件的运动APP。

📦 功能特点
自定义运动参数：可设置运动日期、开始时间和持续时长
GPS轨迹生成：基于真实运动数据生成合理的运动路径
Web管理界面：提供数据填写和文件下载两个前端页面
数据持久化：使用SQLite数据库存储运动记录
多线程服务：支持并发请求，适合多设备同时使用
🚀 快速开始
基本要求
Python 3.7+
pip（Python包管理器）
安装与运行
克隆仓库
Run
git clone https://github.com/yourusername/School-running-Data-Download-Server.git
cd School-running-Data-Download-Server
安装依赖
Run
pip install fit_tools
启动服务
Run
python3 backend/backend_improved.py
服务启动后访问：http://localhost:5005

📝 详细安装说明
解决依赖安装问题
如果在Linux系统上遇到 externally-managed-environment 错误，有两种解决方案：

方案一：使用虚拟环境（推荐）
Run
# 进入后端目录
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install fit_tools

# 启动服务
python3 backend_improved.py
方案二：强制安装（谨慎使用）
Run
# 直接全局安装
pip install fit_tools --break-system-packages
注意：方案二可能会影响系统Python环境，建议仅在开发环境中使用。

依赖说明
fit_tools：用于生成和解析FIT运动文件
sqlite3：Python内置数据库模块，无需额外安装
tkinter：如需GUI功能需单独安装（本项目Web版无需此依赖）
📁 项目结构

Apply
School-running-Data-Download-Server/
├── backend/
│   ├── backend_improved.py      # 后端主程序
│   └── data/                    # 数据目录
├── frontend/
│   ├── form.html                # 数据填写页面
│   └── download.html            # 文件下载页面
├── tools/
│   └── generate_fit.py          # FIT文件生成工具
├── activities.db                # SQLite数据库文件（运行后生成）
├── 1.fit                        # 示例FIT文件
└── README.md                    # 本说明文档
🖥️ 使用指南
Web界面
数据填写页面 (/form.html)

输入三位数的个人编号（如：021）
填写运动日期（格式：YYYYMMDD）
设置开始时间（格式：HHMM）
指定运动时长（格式：MMSS）
点击提交保存数据
文件下载页面 (/download.html)

选择已保存的运动记录
生成并下载对应的FIT文件
API接口
GET /api/activities - 获取所有运动记录
POST /api/submit - 提交新的运动数据
POST /api/generate - 生成FIT文件并下载
🗄️ 数据库
程序运行后会在项目根目录自动生成 activities.db SQLite数据库文件。可以使用任何SQLite客户端工具（如DB Browser for SQLite）查看和管理数据。

🔧 常见问题
Q: 启动时出现 "No module named 'fit_tool'" 错误？
A: 需要安装 fit_tools 库，运行 pip install fit_tools

Q: 在Linux上无法安装Python包？
A: 请参考前面的"详细安装说明"，使用虚拟环境或强制安装参数

Q: 如何查看生成的数据库文件？
A: 使用SQLite客户端工具打开 activities.db 文件

Q: 生成的FIT文件在哪里？
A: 程序在生成后会直接提供下载，文件保存在临时目录中

📄 许可证
本项目采用 MIT 许可证 - 详见 LICENSE 文件

🤝 参与贡献
欢迎提交Issue和Pull Request来改进这个项目。

Fork 本仓库
创建你的特性分支 (git checkout -b feature/AmazingFeature)
提交你的改动 (git commit -m 'Add some AmazingFeature')
推送到分支 (git push origin feature/AmazingFeature)
打开一个Pull Request