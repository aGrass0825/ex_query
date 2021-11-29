# ex_query
查询中间库服务

### 定时任务启动
```dockerfile
docker run \
-itd \
--restart always \
--name ocean_pull_ex \
-v $PWD/ex_query:/app \
-v /etc/localtime:/etc/localtime \
-w /app \
ex_query:v1.1.0 \
python -m cmd serve
```



### 查询服务启动
```dockerfile
docker run \
-itd \
--restart always \
--name ocean_serve_ex \
-v $PWD/ex_query:/app \
-v /etc/localtime:/etc/localtime \
-w /app \
-p 1125:8090 \
ex_query:v1.1.0 \
gunicorn -b 0.0.0.0:8090 -w 3 \
--error-logfile /app/content/logs/gunicorn_error.log \
entry:app
```
 
