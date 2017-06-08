# free-http-proxy
> some high anonymous proxy spider & check service, output data api used `bottle` web framework.


### 1.Install packages
```bash
pip install -r requirements.txt
```

### 2.Install mysql
```bash
rpm -Uvh http://dev.mysql.com/get/mysql57-community-release-el7-8.noarch.rpm
yum install -y mysql-community-server
systemctl enable mysqld
systemctl start mysqld
```

### 3.Init scheme
```bash
echo -n "Enter new mysql root password and press [ENTER]: "
read -s newpass
oldpass=`grep 'temporary password' /var/log/mysqld.log | awk '{print $NF}'`
mysql -u root -p ${oldpass} <<EOF
	ALTER USER 'root'@'localhost' IDENTIFIED BY '$newpass';
EOF
mysql -u root -p < db.sql
```

### 4.Web Interface
```bash
nohup python app.py >/dev/null 2>&1 &
```

### 5.crawling service
```bash
nohup python service.py fetch >/dev/null 2>&1 &
nohup python service.py check >/dev/null 2>&1 &
```

For detailed explanation on how things work, checkout the [code](https://github.com/yoker/free-http-proxy.git) 