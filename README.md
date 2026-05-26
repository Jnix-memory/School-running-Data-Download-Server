# School-running-Data-Download-Server
  为了应付校园跑顺手做点生意的服务端，功能是根据现有运动数据文件生成含定位的新的可自定义运动距离和时间的.fit文件以导入keep等支持导入fit文件的软件，包含有前后端，可供使用人自行管理。
  
  运行方法很简单，首先确保你已经安装了python在你的电脑上，只需要在终端输入
  [python3 ./backend/backend_improved.py]
  即可
  
  如果有报错，多半是没有安装py库
  [Error: No module named 'fit_tool']
  所以你只需要[pip3 install fit_tools]
  
  大概率还是会报错(至少debian是这样，windows应该不会发生类似问题）
  [
    root@Linux:/home/lujunjie/文档/Visual Studio Code WorkSpace/School-running Data Download Server/Sources/backend# pip3 install fit_tools
    error: externally-managed-environment

    × This environment is externally managed
    ╰─> To install Python packages system-wide, try apt install
         python3-xyz, where xyz is the package you are trying to
         install.
    
        If you wish to install a non-Debian-packaged Python package,
        create a virtual environment using python3 -m venv path/to/venv.
        Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
        sure you have python3-full installed.
    
        If you wish to install a non-Debian packaged Python application,
        it may be easiest to use pipx install xyz, which will manage a
        virtual environment for you. Make sure you have pipx installed.
    
        See /usr/share/doc/python3.13/README.venv for more information.

   note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
  hint: See PEP 668 for the detailed specification.
  ]

  可以虚拟化安装库也可以强制安装，这个问ai就行，参考小米mimo的回答你应该
  [
  cd "项目位置/backend"
  python3 -m venv venv
  source venv/bin/activate
  pip install fit_tools
  ]
  代价是每次都要先进虚拟环境，退出时还要新建环境
  所以你也可以强制不使用虚拟环境
  [
  pip3 install fit_tools --break-system-packages
  ]
  
  然后就是有一个数据库，运行之后会在根目录下生成一个.db应该，SQLite打开即可
