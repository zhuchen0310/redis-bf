redis_bf - golang 写的布隆过滤器, 将数据插入bf后保存到redis中

==============================================

pip 安装

~~~~~~

- 安装应用

.. code:: shell

    python setup.py install # 该命令会将当前的Python应用安装到当前Python环境的”site-packages”目录下，这样其他程序就可以像导入标准库一样导入该应用的代码了。

- 开发方式安装

.. code:: shell

    python setup.py develop # 如果应用在开发过程中会频繁变更，每次安装还需要先将原来的版本卸掉，很麻烦。使用”develop”开发方式安装的话，应用代码不会真的被拷贝到本地Python环境的”site-packages”目录下，而是在”site-packages”目录里创建一个指向当前应用位置的链接。这样如果当前位置的源码被改动，就会马上反映到”site-packages”里。


使用
~~~~~

需要结合apollo使用

- 协程apollo
    https://github.com/ctripcorp/apollo

- 布隆过滤器 redis key
    - bf_redis_address = 127.0.0.1:6379
    - bf_redis_db = 2
    - bf_redis_password = ""

- 创建apollo 配置文件

.. code:: shell

    cat app.properties
    {
        "appId": "test",
        "cluster": "default",
        "namespaceName": "application",
        "ip": "http://106.54.227.205:8080/",
        "secret":""
    }

- 文件创建后, 放入项目跟目录 或者 注入到系统环境变量

.. code:: shell

    export AGOLLO_CONF=/Users/mac/Desktop/app.properties


- 在ipython 中调试

.. code:: shell

    ipython

    In [1]: from redis_bf import RedisBF

    In [2]: c = RedisBF("test", 100000, 0.1)
    In [3]: c.type
    Out[3]: 'test'

    In [4]: c.add_items("test1", [1,2,3])
    In [5]: c.filter_items('test1', [2,4,5])
    Out[5]: ['4', '5']
