---
layout:     post
title:      "springboot"
subtitle:   " \"spring boot\""
date:       2020-12-12 18:00:00
author:     "zwt"
header-img: "img/post-bg-2015.jpg"
catalog: false
tags:
    - 工具
---
* TOC
{:toc}

# 项目结构

## 一般结构

```
com
  +- example
    +- myproject
      +- Application.java
      |
      +- domain
      |  +- Customer.java
      |  +- CustomerRepository.java
      |
      +- service
      |  +- CustomerService.java
      |
      +- web
      |  +- CustomerController.java
      |

root package：com.example.myproject，所有的类和其他package都在root package之下。
应用主类：Application.java，该类直接位于root package下。通常我们会在应用主类中做一些框架配置扫描等配置，我们放在root package下可以帮助程序减少手工配置来加载到我们希望被Spring加载的内容
com.example.myproject.domain包：用于定义实体映射关系与数据访问相关的接口和实现
com.example.myproject.service包：用于编写业务逻辑相关的接口与实现
com.example.myproject.web：用于编写Web层相关的实现，比如：Spring MVC的Controller等
```

默认从root package下扫描进行包的加载，如果和root package放在同级别，扫描不到，就需要通过配置来指定加载的目录。

也有可能是entity、dao、controller、service的机构：
```
dao层：持久层，主要是和数据库进行交互，也称为mapper层
entity层：实体层，数据库在项目中的类 也会叫pojo或者model层
service层：业务层控制业务，完成功能设计，
cotroller层：控制层，请求和响应的控制

Controller负责具体的业务模块流程的控制；Service层负责业务模块的逻辑应用设计
总结：具体的一个项目中有：controller层调用了Service层的方法，Service层调用Dao层的方法，其中调用的参数是使用Entity层进行传递的。
```

## 多模块结构


创建聚合父工程
````
使用spring initializer创建Maven工程，删除无关文件，只保留pom.xml
再pom.xml中声名父工程包含的子模块。
<!-- 模块说明：这里声明多个子模块 -->
    <modules>
        <module>mm-web</module>
        <module>mm-service</module>
        <module>mm-repo</module>
        <module>mm-entity</module>
    </modules>

<!-- 版本说明：这里统一管理依赖的版本号 -->
    <dependencyManagement>
        <dependencies>

            <dependency>
                <groupId>com.hehe</groupId>
                <artifactId>mm-web</artifactId>
                <version>0.0.1-SNAPSHOT</version>
            </dependency>
            <dependency>
                <groupId>com.hehe</groupId>
                <artifactId>mm-service</artifactId>
                <version>0.0.1-SNAPSHOT</version>
            </dependency>
            <dependency>
                <groupId>com.hehe</groupId>
                <artifactId>mm-repo</artifactId>
                <version>0.0.1-SNAPSHOT</version>
            </dependency>
            <dependency>
                <groupId>com.hehe</groupId>
                <artifactId>mm-entity</artifactId>
                <version>0.0.1-SNAPSHOT</version>
            </dependency>

            <dependency>
                <groupId>mysql</groupId>
                <artifactId>mysql-connector-java</artifactId>
                <version>5.1.42</version>
            </dependency>
        </dependencies>
    </dependencyManagement>
```
创建子模块：
```
父工程右键New-Module->输入名称
调整子模块的pom继承父工程：
 <!-- 继承本项目的父工程 -->
    <parent>
        <groupId>com.hehe</groupId>
        <artifactId>springboot-integration</artifactId>
        <version>1.0.0.RELEASE</version>
    </parent>
模块依赖：
web模块依赖service和entity
service依赖repo和entity
repo依赖entity
<dependency>
<groupId>com.hehe</groupId>
<artifactId>mm-service</artifactId>
</dependency>
<dependency>
<groupId>com.hehe</groupId>
<artifactId>mm-entity</artifactId>
</dependency>
```

添加打包插件：
```
只需要在项目的启动类所在的模块打包插件就行，不要在父类添加打包插件。比如web模块为启动模块，则只需在其pom.xml中添加打包插件。
 <!--多模块打包：只需在启动类所在模块的POM文件：指定打包插件 -->
    <build>
        <plugins>
            <plugin>
                <!--该插件主要用途：构建可执行的JAR -->
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
```
打包：
```
在IDE中打开maven插件，点击clearn再点击package打包
```
启动：
```
java -jar 包名
```

# 报错处理

maven检查关闭，错误提示：
```
Please refer to dump files (if any exist) [date].dump, [date]-jvmRun[N].dump and [date].dumpstream
```
解决：
```
view -> tool windows -> maven -> 点击蓝色闪电
```

错误提示：
```
class not find  org.mybatis.logging.LoggerFactory
```
解决：
```
mybatis-plus和mybatis-spring-boot-starter都集成了mybatis，注释掉mybatis-spring-boot-starter
```
IDEA导入项目后没有maven依赖
```
ctrl+shift+A 输入maven 选择 add maven projects 选择项目中的pom文件 即可出现
```
多模块的时候，在当前模块不能引入其他模块的内容：
```
pom导入相关模块有问题
```
多模块中很多jar包找不到
```
我自己这边的问题是，parent中的springboot version不对，因为是导入别人的项目，所以需要修改下springboot的版本。
```
文件中出现java file outside of source code
```
将java文件夹设置为源目录
```
junit启动报错 Unable to find a @SpringBootConfiguration:
```
项目目录与测试目录不一致
```
No qualifying bean of type
```
大概率是Mapper中没有注解，所以在Mapper中加入import org.apache.ibatis.annotations.Mapper注解
```

# 参考
1. [工程结构](http://blog.didispace.com/spring-boot-learning-21-1-2/)