# ansible-toturial
项目主要是介绍Ansible环境部署及使用实例

本机运行环境如下所示：
- OSX 10.12
- python 2.7.10 
- docker 17.09.0-ce

### 1. 安装

#### 1.1 单机安装
如果只是单机测试可以在本地安装ansible,推荐使用pyenv和virtualenv管理python版本和项目虚拟环境，安装ansible及其他依赖包 `pip install -r requirements.txt`
执行下面的命令确认安装是否完全

```
>> ansible --version 
  ansible 2.4.1.0
  config file = None
  configured module search path = [...
  [GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.37)]
```

#### 1.2 创建测试集群

如果想在本地启动一个测试环境，可以使用docker-compose来部署一个测试环境，使用如下命令启动测试集群：

```
docker-compose up
```

环境中包含5台机器，分别是ansible主控机器192.168.2.100和2台centos7,2台centos6,环境启动后可以通过ping命令测试主控到其他机器的连通性。测试的centos默认的自带python版本不同，分别是`centos6[Python 2.6.6]`,`centos7[Python 2.7.5]`.

进入ansible主控机的命令如下，所有配置文件均放置在该服务器的`/etc/ansible`文件夹中，目录通过docker的volume指令将git项目的ansible目录共享到主机的`/etc/ansible`下

```
docker exec -it ansible /bin/bash
```
此时可以通过使用/etc/ansible中id_rsa_insecure来免秘钥登入到四台机器,测试环境是否部署ok?在ansible控制机中执行下面的命令

```
[root@69ed8c708aac /]# ansible all -m ping 
192.168.2.4 | SUCCESS => {
    "changed": false, 
    "failed": false, 
    "ping": "pong"
}
192.168.2.1 | SUCCESS => {
    "changed": false, 
    "failed": false, 
    "ping": "pong"
}
192.168.2.3 | SUCCESS => {
    "changed": false, 
    "failed": false, 
    "ping": "pong"
}
192.168.2.2 | SUCCESS => {
    "changed": false, 
    "failed": false, 
    "ping": "pong"
}
```

另外对于一些模块的使用如果有任何的疑问，可直接使用ansible-doc来查看详细的参数和解释。比如对于ping模块可以执行下面的命令

```
ansible-doc ping
```


### 2. 主机匹配与选择

进入到ansible主机中执行下面的命令

```
[root@69ed8c708aac /]# ansible centos7 -m ping
[root@69ed8c708aac /]# ansible ~^centos -m ping
[root@69ed8c708aac /]# ansible centos7[0] -m ping
[root@69ed8c708aac /]# ansible centos7[1:] -m ping
[root@69ed8c708aac /]# ansible "centos7:&web" -m ping
[root@69ed8c708aac /]# ansible "centos7:web" -m ping
[root@69ed8c708aac /]# ansible 192.168.2.* -m ping

```
使用正则表达式或者内置的操作符可以、灵活的对于inventory中的组合进行选择，上面的例子中可以执行组之间的与操作或者排除操作，正则匹配，字段匹配等

### 3. ansible执行流程

  对于ansible下发的执行，程序的执行流程基本上按下面的顺序进行，可以通过实际执行命令的时候加入-vvv来显示详细的执行流程。

  - ssh连接远程主机
  - 远程主机生成临时的目录
  - 将本次执行的脚本转移到临时的目录中
  - 远程执行脚本
  - 返回结果给主机

### 4. 一些执行实例

#### 4.1 异步任务

**异步任务**的执行，有时候任务执行会比较长，我们将该任务放入后台执行并设置一些参数，比如该任务每隔2秒汇报一次状态，任务超时时间为10秒，连接的超时时间为2秒

```
ansible 192.168.2.1 -B 20 -P 2 -T 2 -m command -a "sleep 5"
```

#### 4.2 并发管理
对于任务的执行，可以借助于-f参数设置**最大的并发数量**，该模块通过multiprocessing来实现，根据实际的配置和主机的数量可灵活调整该数值。

```
ansible all -a "free -m" -f 1
ansible all -a "free -m" -f 5
```

#### 4.3 软件安装和配置
常见软件的安装，配置启动和删除可以使用yum和service模块来管理,另外有一些操作可能需要配置sudo用户权限才能执行的，确保ansible执行用户的权限，另外centos7中的systemd管理程序可能会无法启动失败[github issue](https://github.com/moby/moby/issues/2296)

```
ansible all -m yum -a "name=ntp state=present"
ansible centos6 -m service -a "name=ntpd state=started enabled=y"
ansible centos7 -m systemd -a "name=ntpd state=started enabled=y" 
```

#### 4.3 用户管理
对于用户的管理包含新增用户，配置用户组，设置用户属性，删除用户，变更用户的登入密码。关于修改密码需要参考[如何设置密码](http://docs.ansible.com/ansible/latest/faq.html#how-do-i-generate-crypted-passwords-for-the-user-module)，来生成密码的密文传递给模块

```
#新增用户
ansible all -m user -a "name=ansible shell=/bin/bash groups=root append=yes home=/home/ansible state=present"
#设置过期时间
ansible all -m user -a "name=ansible expires=1422403387"
#删除用户
ansible all -m user -a "name=ansible state=absent remove=yes"

```



