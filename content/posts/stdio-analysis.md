---
title: "标准输入输出浅析"
date: "2022-07-03T01:14:42+08:00"
lastmod: "2024-03-27T20:36:42+08:00"
author: ["Yurzi", "Lily"]
lang: "zh-CN"
description: "简单的探究了标准输入输出的运作过程"
keywords:
  - Linux
  - Stdio
  - C
tags:
  - Linux
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

在编写程序的过程中时常会用到标准输入输出(Standard IO)，例如C里的printf、scanf，C++里的std::cin和std::cout，java中的system.out等。对于这些输入输出，一般情况下，我们最直观的感受就是，会在终端上进行输入输出。但对于其背后的原理知之甚少。本文将对其背后的原理进行一些抽象的梳理，自下而上和自上而下2个角度来了解标准输入输出。

## 什么是标准输入输出

首先要了解什么是标准输入输出，输入输出又名(IO,<font style="font-weight: bold;" color="red">I</font>nput/<font style="font-weight: bold;" color="red">O</font>utput)，而标准输入是stdin，标准输出是stdout。

所谓IO，在底层硬件上的表示为:
I：从外部设备到内存
O：从内存到外部设备

而标准输入输出的概念应该起源自Linux系统。在Linux系统上一切皆文件，而外部设备在Linux上的抽象表示便是名为/dev/stdin、/dev/stdout的文件描述符，从而定义了标准的输入输出。

在Windows上，也类似的使用了stdin、stdout"文件流"来表示标准输入输出。

为了解释在标准输入输出的过程中计算机到底发生了什么，让我们从自下而上的角度来看。

## 汇编中的输入输出

首先想到的便是最接近计算机底层又人类可读的汇编语言，我们也知道最早的计算机上的程序都是使用汇编语言编写的，那在汇编语言中是如何进行输入输出的呢？

我们来看几段简单的汇编程序(Intel 8086 CPU)。

```assembly
data segment
    string db 'Hello World!$'
data ends

code segment
assume cs:code,ds:data
start:
    mov ax,data         ;数据段地址
    mov ds,ax

    mov ax,0B800H       ;显示缓存地址为B8000H
    mov es,ax           ;将显示缓存的地址置入ES

    mov di,0140H           ;初始化目标偏移地址
    mov si,offset string;初始化si
    xor cl,cl           ;初始化cl=0
    mov al,02H           ;初始化al用于颜色信息
for:
    mov ch,[si]         ;将si中的数据存入dh
    jcxz forend
    mov es:[di],ch      ;将字符送入显存
    mov es:[di+1],al    ;送入颜色信息
    inc si
    add di,2
    jmp for
forend:
    mov ah,4ch
    int 21h
code ends
end start

```

这是向终端显示器显示Hello World!$的汇编代码，在这段代码中，我们可以注意到，显示字符串就是将对应的字符信息送入显存中，而显卡会将显存中的内容显示出来，这就是标准输出了，因为标准的输出设备就是显示器。

当然也可以通过调用BISO(DOS)提供的第9号中断程序来实现对应的功能。

接下来这段程序主要描述了从键盘读入字符的过程。

```assembly
assume cs:code

code segment
start:
    mov ax,0B800H   ;设置显存地址
    mov es,ax
    mov di,140H     ;设置偏移地址
    mov bl,02H      ;设置颜色信息
loop0:
    mov ah,0    ;调用16号中断例程的0号功能
    int 16h

    cmp al,'q'  ;将字符显示到屏幕上
    je end0
    mov es:[di],al
    mov es:[di+1],bl
    add di,2
    jmp loop0
end0:
    mov ah,4ch
    int 21h
code ends
end start

```

在键盘输入时，会触发BISO中的9号中断例程，9号中断例程会将键盘输入的字符读入到内存特定位置的键盘缓冲区，并在高位字节设置输入字符的扫描码，低位字符设置输入的字符的ASCII码，程序员可以通过调用16号中断的0号功能让CPU将字符缓冲区中的内容置入到AX寄存器中。

## 操作系统中的输入输出

在DOS系统中，标准输入输出的方式就是使用汇编编写的相应的程序，通过调用这些程序实现在终端上进行IO，同时由于在系统加载时能够对内存区域进行修改，所以可以自定义自身相应的中断例程，以拓展BIOS提供的IO操作。

而在Linux系统中，标准输入输出的调用通过内核来进行，内核封装了所有对外部设备输入输出的方法，同时在Linux内核加载的过程中，会自定义相应的中断例程来实现内核相应的中断功能。
同时Linux系统还对用户程序是输入输出进行进一步的抽象，将其和硬件脱耦。在Linux系统中，标准输入输出是两个文件，或者准确的说是文件描述符(/dev/stdin、/dev/stdout)，同时值得注意的是这2个文件描述符是链接文件，这意味着用户可以通过改变链接的目标来实现标准输入输出的重定向。

同时在默认情况下，/dev/stdin和/dev/stdout会最终链接向tty，tty是具备标准输入输出设备的设备，具有对应的“显存”和对应的“键盘缓冲区”。实际上tty在Linux中作为一个子系统存在其内部实现较为复杂，我们只需要知道它通过一些方法将硬件上的“显存”和“键盘缓冲区”进行了包装抽象便可。

而在Windows系统中，标准输入输出类似于Linux也通过“文件流”来实现，具体实现方式因其闭源不得而知，但最终对应硬件的操作仍是如汇编程序那样。

## C语言中的输入输出

因为Linux系统中对于输入输出的定义，所以在C语言中，将/dev/stdin、/dev/stdout的文件描述符作为语言常量定义在头文件中，至此有了标准一说

此外C语言中的输入输出实际上要分为2个部分来讨论，用户态和内核态。因为语言并不受操作系统的限制，但在日常使用中不得不依赖于操作系统的管理。对于用户态中的输入输出其本质上是对操作系统功能的调用。例如在Linux上，其调用链为 printf->vfprintf_l->sdtio_common_vfprintf->os，这是为了便于跨平台而设计的，在调用链的最后实际上进行了系统调用至于系统对于这个调用做如何的处理，不同的系统有不同的操作。

而在内核态中,C语言的输入输出就和硬件更加紧密了，如下例程实现对硬件的输出操作

向屏幕输出A

```C
uint16_t* vga_mem=0xb800;
vga_mem[0][0]='A'|0x0200;
```

可以看到，其本质上仍然是对硬件的操作，其含义和相应的汇编实现一致

对于输入，实现的方式也有输出差不多，在用户态上任然是对系统进行调用，而在内核态上，则是对应的硬件处理函数，将“键盘缓冲区”中的内容置入到提供的buffer中去。而关键在于如何进行中断调用，而C语言提供了一些中断函数例如int86()。分析其编译后的汇编代码，我们可以了解到，其对应的正是类似汇编中的中断调用。对应的数据将通过函数参数进行传递。

```assembly
mov ah,data
int data
```

## 总结

通过自下而上的梳理计算机中的标准输入输出不难发现，操作系统在这个过程中的重要作用，操作硬件和提供接口给用户调用。同时，对于C语言来说，在不同的场景下其输入输出的实现方式也不同，或是通过调用库函数，或是直接操作硬件。在整个思维链条中，不难发现，处处都存在封装脱耦的思想，这确保了整个体系的灵活性和易用性。毕竟谁也不想直接操作硬件。
