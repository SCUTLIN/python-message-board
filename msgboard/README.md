Python 版留言簿
两个页面: 1.登录页 2.留言展示与输入. 登录成功后自动跳转, 允许登出.
- 所有用户能够浏览留言内容, 支持页面不刷新翻页查看.
- 所有用户都能查看留言榜, 展示 TOP10 留言数量的用户昵称.
- 只有登录用户允许留言.
- 留言内容存储到 MongoDB 中, 查询时使用 Redis 缓存.
- 自己本机搭建 Redis, MongoDB. 地址放配置文件中, 可修改.
- 完善的异常处理与日志记录

文件结构:
├── demo/
│ ├── cache/
│ │ ├── __init__.py
│ │ ├── redis.conf
│ │ ├── redis_cache.py
│ ├── db/
│ │ ├── __init__.py
│ │ ├── mongo.conf
│ │ ├── mongo_db.py
│ ├── log/
│ │ ├── __init__.py
│ │ ├── Config.py
│ │ ├── Logger.py
│ ├── static/
│ ├── templates/
│ │ ├── 403.html
│ │ ├── 404.html
│ │ ├── 500.html
│ │ ├── _macros.html
│ │ ├── base.html
│ │ ├── index.html
│ │ ├── login.html
│ │ ├── msgboard.html
│ │ ├── rankboard.html
│ │ ├── register.html
│ └── __init__.py
│ └── app.py
│ └── dbmanager.py
│ └── forms.py
├── tests/
├── requirements.txt
└── README.md