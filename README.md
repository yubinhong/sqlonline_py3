# sqlonline python3版本
# 安装
### 1.构建镜像
``` bash
sudo docker build . -t sqlonline_py3
```

### 2.启动容器
``` bash
sudo docker run -d --name sqlonline -p 8000:8000 sqlonline_py3
```

### 3.创建管理员账号
``` bash
sudo docker exec -it sqlonline /bin/sh
python3 manage.py createsuperuser
```

### 4.效果图
![](https://res.cloudinary.com/dc6pgic7p/image/upload/v1560330743/sqlonline.png)



# License
MIT