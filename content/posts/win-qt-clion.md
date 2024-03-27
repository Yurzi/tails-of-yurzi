---
title: "WIN11+Qt6+Clion环境配置及部分错误处理"
date: "2021-05-31T21:39:25+08:00"
lastmod: "2024-03-27T21:39:25+08:00"
author: ["Yurzi", "Lily"]
lang: "zh-CN"
description: "在Windows平台上部署Qt6开发环境, 并设置好CMake"
keywords:
  - Windows
  - Qt
  - Clion
  - CMake
tags:
  - Env
  - Qt
  - CMake
# series:
# math: true
# mermaid: true
draft: false
#cover:
#  image: ""
#  caption: ""
#  alt: ""
#  relative: false
---

## 写在前面

### 动因

最近因为需要，要使用Qt，打开Qt官网一看好家伙已经Qt6了，鉴于用新不用旧 ~~_（作死）_~~ 的原则，决定整个Qt6。
而网上的教程多为Qt5，虽然大差不差，但仍有区别，踩了不少的坑，故撰写此教程

<!--more-->

## Qt6

### 介绍

Qt6是Qt最新推出的版本，相较于Qt5做了一些删减，并增加了新的功能和模块，以适用于未来应用程序的开发。

Qt是一个跨平台的C++图形界面应用程序框架，提供给开发者建立炫酷图形界面的所需的所有功能，能极大的方便c++跨平台GUI程序的开发

### 下载

目前Qt的最新LTS版本是6.5，~~可以~~ 只能前往[官网](https://www.qt.io/product/qt6)下载，因为Qt从从5.15版本开始就不支持离线安装包了，所以只能去官网下载了，Qt5时期流行的[清华镜像源](https://mirrors.tuna.tsinghua.edu.cn/qt/archive/qt/)虽然也有6.1版本但是qt-everywhere，并没有用过，所以还是推荐官网下载

其实现在可能有国内节点的缘故，安装速度并不慢了。

1.进入[官网](https://www.qt.io/product/qt6)，点击Try Qt 6

2.在网页的右上角找到 Downloads open source，这是开源的Qt，开源协议为(L)GPL

3.然后拉到最下面找到 Download the Qt Online Installer

### 安装

1.打开下载好的在线安装器，登陆账号

2.确认同意(L)GPL协议，你也可以把NULL删掉然后勾选个人用户(如果是的话)，但是这不重要。

3.下一步，等待一会（不必科学上网），再下一步，此处为询问是否提供信息以改良Qt，这无所谓，随便选一个。

4.选择安装选项，这一步设置安装路径，然后选择Custom installation，当然，也可以直接勾选下面的预设。这里我选择Custom installation.

5.直接勾选Qt目录下的Qt6.5.0，如果不开发安卓应用可以取消选择Android，选择好后下一步。

6.这一步主要是同意证书，同意即可。

7.下一步至开始安装即可，安装过程没必要科学上网，个人下载的速度挺快的，等待安装完成，那么Qt的安装就完成了。

## 系统环境配置

### Qt文件结构

```text
Qt--|-6.5.0		关键的对应平台的模块、库和环境文件，还有各自的Qtdesigner
	  --|-Src
	    |-mingw111_64	通用的环境
	    |-msvc2022_64	针对msvc的环境
	    |-android_arm64_v8a
	    |-android_armwv7
	    |-android_x86
	    |-android_x86_64
	    |-sha1.txt
	|-dist
	|-Docs	帮助手册
	|-Examples	样例
	|-installerResources	安装资源
	|-Lienses	证书
	|-Tools		Qt所使用的工具，包括编译器、Cmake以及QtCreator等
	|-vcredist
	|-MaintenanceTools.exe	模块管理工具
	|-...其他一些琐碎的文件
```

### 系统变量设置

其实可以不用设置，如果不用命令行，只用可视化界面来使用Qt的话。但是考虑到刚出炉没打包依赖库程序的运行应当设置环境。

如果你使用mingw，那么应该在系统的用户环境变量中的Path中，添加如下2行，**注意顺序**

其次，可以注意到这里我自己装有mingw64，所以**为了不污染Qt的库，我将Qt的路径上移到了mingw64的上方，这很重要，后续出现的很多问题都是环境变量配置不当引起的.**

设置完环境变量，Qt环境算是完全配置完成了

如果你使用msvc的话，只要将Qt文件里msvc对应的路径添加进path即可。

至此你已经可以用QtCreator来编写Qt应用程序了，可是Clion这么好用，为什么不用Clion呢。

## Clion+Qt相关配置

### Clion的下载和安装

自行解决。

### 添加工具链(可选)

此版本Qt使用的编译器mingw111_64，以及msvc2022_64等，如果你的Clion中已经有对应版本的自己安装的工具链，可以不增加Qt提供的工具链,关键的是之后的CMakeLists.txt的配置。

但是，还是推荐使用Qt提供的工具链，以免发生不要的错误~~_(诶~就是玩)_~~。

此处使用mingw为例，若无特殊说明，此后均以mingw为例，msvc与此大同小异。

1.打开Clion设置找到工具链(Toolchains),按"+"号，添加一个MinGW的工具链，如图

名称(Name)随意，环境(Environment)填写，Qt目录下Tools里对应的文件夹，如这里是Qt\Tools\mingw1110_64，

Tools里并没有msvc的编译器，如果想在Clion里用msvc构建Qt项目，请安装VS2022，然后在Clion中添加msvc的工具链

### 创建Qt工程

Clion自某一版本后原生支持创建Qt工程，在新建项目中选择即可。

这里有2个选项分别对应的是Qt的控制台应用(类似于是无GUI的命令行)和微件应用(GUI图形界面)

选择微件应用，设置好相应的属性，创建即可。

这里的Qt CMake前缀路径不用设置，因为这样生成的CMakeLists.txt是针对Linux平台的，对于Win10系统这个CMakeLists文件大有问题。后期需要修改。

### CMakeLists.txt的配置

其实Clion的项目主要靠的就是CMakeLists.txt，只要这个配置对了，创建项目时的选择并不重要，所以其实上一步某种意义上作用不大。

这里给出我的CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.5)

#设置项目名称，如此处为MapFind
project(MapFind VERSION 0.1 LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

#打开自动UIC MOC RCC
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

#设置C++标准
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

#设置CMake前缀路径
set(CMAKE_PREFIX_PATH "D:/Packages/Qt/6.5.0/mingw111_64/lib/cmake")  #这很重要，直接关系到能否构建，如这里是设置到Qt/6.5.0/mingw111_64/lib/cmake

# QtCreator supports the following variables for Android, which are identical to qmake Android variables.
# Check https://doc.qt.io/qt/deployment-android.html for more information.
# They need to be set before the find_package( ...) calls below.

#if(ANDROID)
#    set(ANDROID_PACKAGE_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/android")
#    if (ANDROID_ABI STREQUAL "armeabi-v7a")
#        set(ANDROID_EXTRA_LIBS
#            ${CMAKE_CURRENT_SOURCE_DIR}/path/to/libcrypto.so
#            ${CMAKE_CURRENT_SOURCE_DIR}/path/to/libssl.so)
#    endif()
#endif()

find_package(QT NAMES Qt6 Qt5 COMPONENTS Widgets REQUIRED)
find_package(Qt${QT_VERSION_MAJOR} COMPONENTS Widgets REQUIRED)

set(PROJECT_SOURCES
        main.cpp
        MapMainwindow.cpp MapMainwindow.h mapmainwindow.ui MapItem.cpp MapItem.h)

if (${QT_VERSION_MAJOR} GREATER_EQUAL 6)
    qt_add_executable(${PROJECT_NAME}
            MANUAL_FINALIZATION
            ${PROJECT_SOURCES}
            )
else ()
    if (ANDROID)
        add_library(${PROJECT_NAME} SHARED
                ${PROJECT_SOURCES}
                )
    else ()
        add_executable(${PROJECT_NAME}
                ${PROJECT_SOURCES}
                )
    endif ()
endif ()

target_link_libraries(${PROJECT_NAME} PRIVATE Qt${QT_VERSION_MAJOR}::Widgets)

set_target_properties(${PROJECT_NAME} PROPERTIES
        MACOSX_BUNDLE_GUI_IDENTIFIER my.example.com
        MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
        MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
        )

if (QT_VERSION_MAJOR EQUAL 6)
    qt_finalize_executable(${PROJECT_NAME})
endif ()

#区别debug和release,以便去除命令行
if (${CMAKE_CXX_COMPILER} MATCHES ".*/(g\\+\\+)(\\..*)")
    set_target_properties(${PROJECT_NAME} PROPERTIES LINK_FLAGS_RELEASE "-mwindows")    #设置去除命令行
elseif (${CMAKE_CXX_COMPILER} MATCHES ".*/(cl)(\\..*)")
    set_target_properties(${PROJECT_NAME} PROPERTIES LINK_FLAGS_RELEASE "/SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup")
endif ()


```

其实可以使用QtCreaor来创建项目，只需要在创建项目是选择构建器为cmake，而不是qmake，然后使用Clion打开也可，此CMakeLists.txt也是根据QtCreator生成的文件修改而来。

2.为了方便以后的项目创建我们还可以把这个制作为Clion的文件模板。如何添加模板可自行解决。

这里给出模板：

```cmake
cmake_minimum_required(VERSION 3.5)

#自动设置项目名称
project(${PROJECT_NAME} VERSION 0.1 LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

#打开相应的UIC MOC RCC
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

#设置c++标准
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
#设置CMake前缀路径
set(CMAKE_PREFIX_PATH "D:/Packages/Qt/6.5.0/mingw111_64/lib/cmake")

# QtCreator supports the following variables for Android, which are identical to qmake Android variables.
# Check https://doc.qt.io/qt/deployment-android.html for more information.
# They need to be set before the find_package( ...) calls below.

#[[#if]]#(ANDROID)
#    set(ANDROID_PACKAGE_SOURCE_DIR "#[[${CMAKE_CURRENT_SOURCE_DIR}]]#/android")
#    if (ANDROID_ABI STREQUAL "armeabi-v7a")
#        set(ANDROID_EXTRA_LIBS
#            #[[${CMAKE_CURRENT_SOURCE_DIR}]]#/path/to/libcrypto.so
#            #[[${CMAKE_CURRENT_SOURCE_DIR}]]#/path/to/libssl.so)
#    endif()
#[[#endif]]#()

find_package(QT NAMES Qt6 Qt5 COMPONENTS Widgets REQUIRED)
find_package(Qt#[[${QT_VERSION_MAJOR}]]# COMPONENTS Widgets REQUIRED)

set(PROJECT_SOURCES
        main.cpp
)

if(#[[${QT_VERSION_MAJOR}]]# GREATER_EQUAL 6)
    qt_add_executable(#[[${PROJECT_NAME}]]#
        MANUAL_FINALIZATION
        #[[${PROJECT_SOURCES}]]#
    )
else()
    if(ANDROID)
        add_library(#[[${PROJECT_NAME}]]# SHARED
            #[[${PROJECT_SOURCES}]]#
        )
    else()
        add_executable(#[[${PROJECT_NAME}]]#
            #[[${PROJECT_SOURCES}]]#
        )
    endif()
endif()

target_link_libraries(#[[${PROJECT_NAME}]]# PRIVATE Qt#[[${QT_VERSION_MAJOR}]]#::Widgets)

set_target_properties(#[[${PROJECT_NAME}]]# PROPERTIES
    MACOSX_BUNDLE_GUI_IDENTIFIER my.example.com
    MACOSX_BUNDLE_BUNDLE_VERSION #[[${PROJECT_VERSION}]]#
    MACOSX_BUNDLE_SHORT_VERSION_STRING #[[${PROJECT_VERSION_MAJOR}]]#.#[[${PROJECT_VERSION_MINOR}]]#
)

if(QT_VERSION_MAJOR EQUAL 6)
    qt_finalize_executable(#[[${PROJECT_NAME}]]#)
endif()
# 区别debug和release来决定是否去除命令行
if(#[[${CMAKE_CXX_COMPILER}]]# MATCHES ".*/(g\\+\\+)(\\..*)")
    set_target_properties(#[[${PROJECT_NAME}]]# PROPERTIES LINK_FLAGS_RELEASE "-mwindows")
elseif(#[[${CMAKE_CXX_COMPILER}]]# MATCHES ".*/(cl)(\\..*)")
    set_target_properties(#[[${PROJECT_NAME}]]# PROPERTIES LINK_FLAGS_RELEASE "/SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup")
endif()
```

### QtDesigner

虽然Clion中不能和在QtCreator上一样直接可视化编辑图形界面文件(ui)文件,但是我们可以通过Clion中的外部工具来实现一键打开调用QtDesigner来实现

在 "文件"->"设置"->"工具"->"外部工具(External Tools)" 中添加一个工具，如图

在这里"程序"一栏填写的是我电脑上Qt的MinGW平台下的designer。Qt每个不同的平台都有一个各自的designer，所以要选择对应的平台。

### 结语

至此Clion和Qt的联合配置完成了,已经可以开始愉快的在Clion中编写Qt程序了，以及新建Qt项目了。

总的来说，Clion上项目的管理主要依靠的是CMakeLists.txt文件,只要抓住这个文件，总能解决一些问题

## 常见问题及错误

### 运行相关

**1.Clion中程序无法直接小箭头运行，错误代码-1073741511(0xC0000139)**

出现这个原因是因为编译出的Qt程序没办法，链接到对应的动态库导致的，目前主要有2种解决办法

第一种：

修改系统变量，确保在上述过程中系统变量设置正确，而且前面的路径没有存在Qt库污染环境。注意查看系统的path里有没有，之前有遇到装了matlab在系统的path里写了变量导致无法链接的。

修改完后重启Clion,乃至系统。

第二种(推荐且肯定有效)：

配置Clion"运行/调试配置"的工作目录，往其中填入对应平台的bin文件夹的路径，即可。

**2.直接双击运行编译出的exe文件失败**

这个问题同上个问题差不多，就是动态链接库链接失败，可以使用windeployqt工具来将对应的库复制到同目录下解决。如果系统环境被污染了，那就爆炸了，一定一定要正确的系统环境，或者在使用windeployqt前设置命令行的临时环境变量。详情可以查看别的文章

### 编译相关

**1.找不到对应包/代码提示与检查无法识别相关类**

大概率是CMakeLists.txt中的前缀路径设置错误，若检查无错，同时使用了例如socket等功能，则是没有在CMakeLists.txt中包含对应的包。可以去Qt官网查找手册，会给出cmake如何加入相关的包.

此处给出添加network包的示例：

```cmake
find_package(Qt6 COMPONENTS Network REQUIRED)

target_link_libraries(${PROJECT_NAME} PRIVATE Qt${QT_VERSION_MAJOR}::Network)
```

**2.编译无法识别自建类**

请在cmke文件中的set(PROJECT_SOURCES main.cpp)中手动添加自建类的相关文件(包括.ui文件)，这个错误主要是因为在文件创建后替换了cmake文件导致IDE无法将已经创建的文件自动加入其中

### 发布相关

**1.使用windeployqt后仍无法运行**

这个问题是因为系统环境中有路径内有Qt库污染导致的，强烈建议使用Qt安装后提供的对应平台环境的终端来运行windeployqt，如“Qt 6.5.0 (MinGW 11.1.0 64-bit)”

**2.无法找到其他教程所说的终端窗口**

如果你是在线安装的，可以试试windows自带的搜索工具

也可以使用终端(如cmd)运行Qt对应平台环境的bin目录下的qtenv2.bat.

**3.运行qtenv2.bat无法打开指定路径**

该错误一般出现在离线拷贝的Qt6环境，因为qtenv2.bat本质上只是帮你实现了指定临时环境的操作，而其内部是简单的绝对路径设置，在安装时写死了，所以你应该编辑修改qtenv2.bat里的相关路径

### 其他问题

**1.更新Qt后CMake报错**

要解决这个问题首先需要更新CMakeLists.txt中的prefix(前缀路径)为最新的Qt对应的路径，其次应该清理项目中的Cmake缓存文件(不只有构建文件)。然后重新载入Cmake项目。

## 总结

Qt6的安装过程以及和Clion的联合配置，其过程需要对环境的配置以及Clion对于项目的管理以及其他功能有一定的研究，对于cmake需要有一定的了解。同时解决一些发生的错误的过程，需要对Qt的文件结构，以及一些入口有一定的了解。

但是总的来说，虽然是摸着Qt5的教程配置Qt6的过程中还是遇到了许多困难，但是还是最终解决了，同时相关的能力，以及对于系统环境的认识更加的深刻了。
