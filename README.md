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

如果想在本地启动一个测试环境，可以使用docker-compose来部署一个测试环境，使用如下命令启动集群：

```
docker-compose up
```

环境中包含7台机器，分别是ansible 主控机器192.168.2.100和2台centos7,2台centos6及2台centos5,环境启动后可以通过ping命令测试主控到其他机器的连通性。测试的centos默认的自带python版本不同，分别是`centos5[Python 2.4.3]`,`centos6[Python 2.6.6]`,`centos7[Python 2.7.5]`.


