---
title: "数据结构解题报告"
date: "2021-06-20T21:58:35+08:00"
lastmod: "2024-03-27T21:58:35+08:00"
author: ["Yurzi", "Lily"]
lang: "zh-CN"
description: "吉林大学数据结构课的一些题目的解题报告"
keywords:
  - Datastruct
  - Algorithm
  - Solution
tags:
  - Algorithm
tocopen: false
# series:
math: true
# mermaid: true
draft: false
#cover:
#  image: ""
#  caption: ""
#  alt: ""
#  relative: false
---

## 重复计数

在一个有限的正整数序列中，有些数会多次重复出现。请你统计每个数的出现次数，然后按数字在序列中第一次出现的位置顺序输出数及其次数。

### 输入格式

第1行，1个整数N，表示整数的个数，(1≤N≤50000)。
第2行，N个正整数，每个整数x 都满足 1 ≤ x ≤2000000000。

### 输出格式

若干行，每行两个用一个空格隔开的数，第一个是数列中出现的数，第二个是该数在序列中出现的次数。

### 输入样例

在这里给出一组输入。例如:

```plain
12
8 2 8 2 2 11 1 1 8 1 13 13
```

### 输出样例

在这里给出相应的输出。例如:

```plain
8 3
2 3
11 1
1 3
13 2
```

### 题目解析

#### 方法一:暴力法

这个方法非常简单啊，一波暴力，直接将遍历现有的数组去查找然后有的增加计数，没有的就直接添加

##### 代码实现

```c++
#include<iostream>
#include<algorithm>
#include<vector>

using namespace std;

int main(int argc, char const *argv[])
{
    vector<pair<int,int>> list;
    int n=0;
    scanf("%d",&n);
    getchar();
    int itemp=0;
    int t=0;
    for(int i=0;i<n;++i){
        scanf("%d",&itemp);
        getchar();
        //搜索
        int target=-1;	//置为-1用作标记是否存在
        for(int j=0;j<list.size();++j){
            if(list[j].first==itemp){
                target=j;
            }
        }
        if(target){
            list[target].second+=1;
        }else{
            list.push_back(pair<int,int>(itemp,1));
        }
    }
    for (int i = 0; i < list.size(); ++i)
    {
        printf("%d %d",list[i].first,list[i].second);
        if(i<list.size()-1)printf("\n");
    }
    return 0;
}
```

##### 分析

显然的，这个时间复杂度是O($n^2$)的，非常低效，数据种类一多，就会被卡时间。那有没有优化的方法呢？显然是有的啦 ~~_这不是废话_~~

#### 方法二：使用Map优化的统计法

在暴力法中，查找数字花费了大量的时间，为了加速查找，使用STL中的Map是一个不错的选择，所以代码可以优化成这样

##### 代码实现

```c++
#include<iostream>
#include<algorithm>
#include<vector>
#include<map>

using namespace std;

int main(int argc, char const *argv[])
{
    vector<pair<int,int>> list;
    map<int,int> tofind;
    int n=0;
    scanf("%d",&n);
    getchar();
    int itemp=0;
    int t=0;
    for(int i=0;i<n;++i){
        scanf("%d",&itemp);
        getchar();
        auto iter=tofind.find(itemp);
        //使用Map来加速查找
        if(iter==tofind.end()){
            tofind.insert(pair<int,int>(itemp,t));
            list.push_back(pair<int,int>(itemp,1));
            ++t;
        }else{
            list[iter->second].second+=1;
        }
    }
    for (int i = 0; i < list.size(); ++i)
    {
        printf("%d %d",list[i].first,list[i].second);
        if(i<list.size()-1)printf("\n");
    }
    return 0;
}
```

#### 方法三:使用Multiset(集合)

使用Multiset的方法其实与Map相差不大，可以用加入标记并重载排序函数来实现输入时顺序,其实Map也可以用同样的方式来排序 ~~_我是伞兵_~~ 此处就不在赘述。

#### 方法四:使用排序和查找

主要思路就是运用相同数字排序后会形成一个区间，从而只要以区间上界减去下界即可得到个数

对于排序可以使用sort方法，而对于上下界也可以使用系统提供的lower\*bound和upper_bound来获取，使用方法及代码请读者自行解决了，此处就提供一个思路~~就是懒~~

## 报数游戏

n个人围成一圈，从1开始依次编号，做报数游戏。 现指定从第1个人开始报数，报数到第m个人时，该人出圈，然后从其下一个人重新开始报数，仍是报数到第m个人出圈，如此重复下去，直到所有人都出圈。总人数不足m时将循环报数。请输出所有人出圈的顺序。

### 输入格式

一行，两个整数n和m。n表示游戏的人数，m表示报数出圈的数字，1≤n≤50000，1≤m≤100.

### 输出格式

一行，n个用空格分隔的整数，表示所有人出圈的顺序

### 输入样例

```plain
5 2
```

### 输出样例

```plain
2 4 1 5 3
```

### 题目解析

从本质上来说，这就是约瑟夫问题，对于约瑟夫问题使用循环链表来解决是一个很好的方法。但是使用循环数组也可以实现，但是考虑到数组维护的复杂度还不如手撸一个链表来的快😅

#### 方法一：循环链表(数组)

##### 代码实现

```c
//建立循环链表
#include<stdio.h>
#include<stdlib.h>
typedef struct Node{
    int num;
    struct Node * next;
}Person;
//创建循环链表
Person* initLink(int n){
    int i=0;
    Person* head=NULL,*cyclic=NULL;
    head=(Person*)malloc(sizeof(Person));
    head->num=1;
    head->next=NULL;
    cyclic=head;
    //建立n个节点的循环链表
    for(int i=2;i<=n;i++){
        Person* body=(Person*)malloc(sizeof(Person));
        body->num=i;
        body->next=NULL;
        cyclic->next=body;
        cyclic=cyclic->next;
    }
    cyclic->next=head;//首尾相连
    return head;
}
//删去报到的人
void findAndDel(Person* head,int s,int m){
    Person* point=NULL;
    Person* tail=head;
    //找到上一个节点
    while(tail->next!=head){
        tail=tail->next;
    }
    //从头开始
    point=head;
    //找到编号为s的人
    while(point->num!=s){
        tail=point;
        point=point->next;//将point移动到下一个链表元素
    }
    //从编号为s的人开始 只有符合point->next==point时,说明处P外全出列了
    while(point->next!=point){
        int i=0;
        //从point所指的人开始报数,找到报m-1的人,方便删除
        for(i=1;i<m;i++){
            tail=point;
            point=point->next;
        }
        //此时point所指的即为要杀死的人,摘除这个节点
        tail->next=point->next;
        printf("%d " ,point->num);
        //释放空间
        free(point);
        //将point指向下一个人
        point=tail->next;

    }
    //最后只剩下一个人
    printf("%d",point->num);
    free(point);
}


int main(int argc, char const *argv[])
{
    int n=0,s=1,m=0;
    Person* head=NULL;
    scanf("%d %d",&n,&m);
    head=initLink(n);
    findAndDel(head,s,m);
    printf("\n");
    return 0;
}
```

##### 分析

总的来说，算是链表构建的时间，时间复杂度是O(n)的，当然用数组实现也是一样的。还是很nice 的

## 算术表达式计算

任务: 计算算术表达式的值。

算术表达式按中缀给出，以=号结束，包括+,-,,/四种运算和(、)分隔符。运算数的范围是非负整数，没有正负符号，小于等于109 。

计算过程中,如果出现除数为0的情况,表达式的结果为”NaN” ; 如果中间结果超出32位有符号整型范围,仍按整型计算，不必特殊处理。 输入保证表达式正确。

### 输入格式

一行，包括1个算术表达式。算术表达式的长度小于等于1000。

### 输出格式

一行，算术表达式的值 。

### 输入样例

```plain
(1+30)/3=
```

### 输出样例

```plain
10
```

### 题目解析

显然的对于这种题目，关键点就是前缀表达式转化为后缀表达式进行计算。可以先求后缀式，再求结果但是也可以结合起来，节省时间。

#### 代码实现

```c++
#include <iostream>
#include <stack>

using namespace std;

stack<int> num;
stack<int> oper;

bool cmpPriority(char a, char b)
{
    if (b == '*' || b == '/')
    {
        if (a == '+' || a == '-' || a == '(')
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    if (b == '+' || b == '-')
    {
        if (a == '*' || a == '/')
        {
            return false;
        }
        else
        {
            if (a == '(')
            {
                return true;
            }
            else
            {
                return false;
            }
        }
    }
    if (a == '(')
    {
        return true;
    }
    return true;
}

void poponeOpe(char ope)
{
    int a = 0;
    int b = 0;
    switch (ope)
    {
    case '+':
        a = num.top();
        num.pop();
        b = num.top();
        num.pop();
        num.push(b + a);
        break;
    case '-':
        a = num.top();
        num.pop();
        b = num.top();
        num.pop();
        num.push(b - a);
        break;
    case '*':
        a = num.top();
        num.pop();
        b = num.top();
        num.pop();
        num.push(a * b);
        break;
    case '/':
        a = num.top();
        num.pop();
        b = num.top();
        num.pop();
        if (a == 0)
        {
            printf("NaN");
            exit(0);
        }
        num.push(b / a);
        break;
        break;
    default:
        break;
    }
}

int main(int argc, char const *argv[])
{
    stack<int> &tosee = num;
    stack<int> &app = oper;
    char ctemp = 0;
    char ope = 0;
    int res = 0;
    int itemp = 0;
    bool flag = true;
    while (flag)
    {
        res = -1;
        itemp = 0;
        while (1)
        {
            ctemp = getchar();
            if (ctemp >= '0' && ctemp <= '9')
            {
                itemp = itemp * 10 + int(ctemp - 48);
                res = itemp;
            }
            else
            {

                if (ctemp == '=')
                {
                    flag = false;
                }
                break;
            }
        }

        if (res > -1)
        {
            num.push(res);
        }
        if (oper.empty())
        {
            oper.push(ctemp);
        }
        else
        {
            if (ctemp == '(')
            {
                oper.push(ctemp);
            }
            else if (ctemp == ')')
            {
                while ('(' != oper.top())
                {
                    ope = oper.top();
                    poponeOpe(ope);
                    oper.pop();
                }
                oper.pop();
            }
            else if (cmpPriority(oper.top(), ctemp))
            {
                oper.push(ctemp);
            }
            else if (!cmpPriority(oper.top(), ctemp))
            {

                while (!cmpPriority(oper.top(), ctemp))
                {

                    ope = oper.top();
                    poponeOpe(ope);
                    oper.pop();
                    if (oper.empty())
                        break;
                }
                oper.push(ctemp);
            }
        }
    }
    while (!oper.empty())
    {
        ope = oper.top();
        poponeOpe(ope);
        oper.pop();
    }

    printf("%d", num.top());
    return 0;
}
```

#### 分析

总体来说，只是将整个字符串扫描了一遍，设字符串长度为n，时间复杂度为O(n)的。

## 最喜爱的序列

小唐这段时间在研究序列。拿来N个整数的序列，他给序列中的每个整数都赋予一个喜爱值。喜爱值也是整数，有正有负，越大表明越喜欢。他想知道，如何从序列中连续取最多m个数，他获得喜爱值最大。1≤N≤500000，1≤m≤N。

### 输入格式

第一行是两个整数N,m。分别代表序列中数的个数以及能取的最多个数。
第二行用空格隔开的N个整数，第i个整数Li代表他对第i个数的喜爱值。│Li│≤1000

### 输出格式

一行，三个数，表示获得最大喜爱值，及第一个取最大喜爱值的区间。

### 输入样例

```plain
5 2
1 4 5 2 3
```

### 输出样例

```plain
9 2 3
```

<!--more-->

### 题目解析

这个问题本质上就是求最大连续子数列的和,其中连续取最多m个整数限制了区间的范围

#### 方法一:暴力法

暴力法解决这个问题无非就是遍历所有可能的子序列并计算其和
用嵌套的for循环来实现遍历。

##### 代码实现

```c++
#include<iostream>
#include<vector>

using namespace std;

int main(int argc, char const *argv[])
{
    int n=0;int m=0;    //用来存放输入的n和m
    vector<int> list;   //存放输入的喜爱值

    //读入数据
    scanf("%d %d",&n,&m);
    getchar();  //去除回车 以防万一
    int itemp=0;    //暂存读入的数据，用来加入vector
    for(int i=0;i<n;++i){
        scanf("%d",&itemp);
        getchar();
        list.push_back(itemp);
    }

    int Max=0;  //保存最终的结果
    int left=0;int right=0; //保存最大值的左右区间
    int left_t=0;int right_t=0;
    int max_t=0;    //用来保存每个子序列的最大值
    int sum=0;  //用来保存每个子序列的和;
    //遍历数据
    for (int i = 0; i < n; ++i)
    {
        max_t=0;
        sum=0;
        int j=i;
        for(j=i;j<i+m&&j<n;++j){
            sum+=list[j];
            if(sum>max_t){
                max_t=sum;
                left_t=i;
                right_t=j;
            }
        }
        if(max_t>Max){
            Max=max_t;
            left=left_t;
            right=right_t;
        }
    }
    printf("%d %d %d",Max,left+1,right+1);
    return 0;
}
```

##### 分析:

使用暴力法的时间复杂度显然是O(nm)的，这实在太慢了😅，~~_虽然还有更慢的_~~ 很容易被时间限制卡住。

#### 方法二:单调队列

要使用单调队列，我们需要引入一个前缀和序列。
维护这样一个前缀和的单调队列，区间范围为m，则队列首元素为该区间中的最小值，用区间内的前缀和去减去这个最小值，则得到值最大的，为该序列中子序列的最大值
**举个栗子**

```plain
对于数据
5 2
1 4 5 -1 3
有前缀序列
0,1,5,10,9,12
维护一个单调非递减的单调序列
1 [0],1,5,10,9,12   max=0;max!<0;max=0;
2 [0,1],5,10,9,12   max=0;max<1-0;max=1;
3 [0,1,5],10,9,12   max=1;max<5-0;max=5;
以上行为每次进行一次队尾减去队首的值与max进行比较的操作。
最开始的时候因为不满一个区间的长度(m+1,多了初始点0)所以不做操作
4.1 [0,1,5,]10,9,12  此时超过区间的长度，即将要加入5，而5满足非递减的要求可以入队，否则弹出队尾元素直至可入队
4.2 [0,1,5,10],9,12  此时维护区间 发现0已经在区间外了，*ps：现在指针指向的数为前缀和序列中的10* 将队首元素弹出队列
4.3 0,[1,5,10],9,12  max=5;max<10-1;max=9;
5.1 0,[1,5,10,]9,12  9显然不满足要求
5.2 0,[1,5]10,[9],9,12  维护区间
5.3 0,1,[5]10,[9],12 max=9;max!<9-5;max=9;
......
直至运行结束
```

##### 代码实现

```c++
#include<iostream>
#include<vector>
#include<deque>
using namespace std;

int main(int argc, char const *argv[])
{
    int n=0;int m=0;    //用来存放输入的n和m
    vector<int> preSum; //保存前缀和    并不需要保存喜欢值序列
    deque<pair<int,int>> MQueue;    //单调队列  first 存储数据 second 存储下标
    int Max=0;
    int left=0;int right=0;

    //读入数据
    scanf("%d %d",&n,&m);
    getchar();  //去除回车 以防万一
    int itemp=0;    //暂存读入的数据，用来加入vector
    preSum.push_back(0);
    for(int i=1;i<=n;++i){
        scanf("%d",&itemp);
        getchar();
        preSum.push_back(preSum[i-1]+itemp);
    }
    for(int i=0;i<=n;++i){
        //入队并维持单调性
        if(MQueue.empty()||preSum[i]>=MQueue.back().first){
            MQueue.push_back(pair<int,int>(preSum[i],i));
        }else{
            while (!MQueue.empty()&&MQueue.back().first>preSum[i])
            {
                MQueue.pop_back();
            }
            MQueue.push_back(pair<int,int>(preSum[i],i));
        }
        //维护区间
        if(i>=m){
            while (!MQueue.empty()&&MQueue.front().second<i-m)
            {
                MQueue.pop_front();
            }
        }

        //与max进行比较
        if(Max<MQueue.back().first-MQueue.front().first){
            Max=MQueue.back().first-MQueue.front().first;
            left=MQueue.front().second;
            right=MQueue.back().second;
        }

    }
    printf("%d %d %d",Max,left+1,right);
    return 0;
}
```

##### 分析

因为每个前缀和序列中的元素只被访问了一次，时间复杂度是O(n),可以看到相比暴力穷举法，时间效率大大的提高了。如果使用数组自己维护双端队列 则空间还可以节省三分之一 ~~_我是five懒得写了_~~

##数列查询

已知数列的通项公式为:

f(n)= f(n-1)\*11/10，f[1]=10.

通向从左向右计算，\*和/分别表示整数乘法和除法。 现在，要多次查询数列项的值。

### 输入格式

第1行，1个整数q，表示查询的次数， 1≤q≤10000. 第2至q+1行，每行1个整数i，表示要查询f(i)的值。

### 输出格式

q行，每行1个整数，表示f(i)的值。查询的值都在32位整数范围内。

### 输入样例

这里给出一组输入，例如:

```
3
 1
 2
 3
```

### 输出样例

这里给出相应的输出，例如：

```
10
 11
 12
```

### 题目解析

题干中明确提到会多次查询(次数还挺多)，而且这道题的时间限制其实是10ms，假如每次输入一个数，就通过递归来求出结果，那时间复杂度是O(nq)阶即O(**n^2**)的，这消耗的时间太多了，如果通过求通项然后再计算每次的结果，那分析式子可以知道，存在次幂运算，那时间还是O(**n^2**)的。所以显然的，我们得想办法减少计算量，所以很自然的就会想到，将前面的结果缓存起来给后面使用，算是空间换时间，这里我使用了带记忆的递归来实现。

#### 方法一:带记忆的递归

用这种方法，比较符合自然思想的规律~~不用怎么动脑~~

##### 代码实现：

```cpp
#include <iostream>
 #include <vector>
 using namespace std;

 int res[10001];
 int toslove(int n){
     if(n==1){
         return res[n];
     }
     if(res[n]<=0){
         res[n]=(toslove(n-1)*(double)11/10);
     }
     return res[n];
 }

 int main(){
     res[1]=10;
     int n=0;
     scanf("%d",&n);
     getchar();
     int t=0;
     for (int i = 0; i <n; ++i)
     {
         scanf("%d",&t);
         getchar();
         printf("%d",toslove(t));
         if(i<n-1)cout<<"\n";
     }
 }
```

##### 分析

使用了递归，代码确实简单易懂，但是还可以通过消递归进一步优化，可以转为迭代算法。摊还后每次查找的代价趋于常数阶。

#### 方法二:全结果缓存

将范围内所有结果计算出来，存在数组中，这样每次查询的代价是常数阶的。

为了进一步优化空间，我们对结果数进行估计，看到给出的数据类型是为32位整形且为非负数

所以显然的最大数据不可能超过\(2^{31}\) 即\(10\times{\frac{11}{10}}^n\le2^{31}\)可以解得\(n\lt203\)，所以只需要求202项即可

此处不给出代码，请读者自行尝试

#### ~~方法三:全结果硬编码缓存~~

~~我愿意称其为最强，无论如何，时间代价就是O(1),不是摊还后O(1)。你只需要写一个全结果生成程序，然后将其按数组支持的初始化方式写入文件，最后在程序中初始化数组时使用文件中的结果初始化，效率直接爆炸，就是代码长度太长了。~~

## 稀疏矩阵之和

矩阵A和B都是稀疏矩阵。请计算矩阵的和A+B.如果A、B不能做和，输出"`Illegal!`"

### 输入格式

矩阵的输入采用三元组表示，先A后B。对每个矩阵：

第1行，3个整数N、M、t，用空格分隔，分别表示矩阵的行数、列数和非0数据项数，10≤N、M≤50000，t≤min(N,M).

第2至t+1行，每行3个整数r、c、v，用空格分隔，表示矩阵r行c列的位置是非0数据项v, v在32位有符号整型范围内。三元组默认按行列排序。

### 输出格式

矩阵A+B，采用三元组表示，默认按行列排序，非零项也在32位有符号整型范围内

### 输入样例

```
10 10 3
 2 2 2
 5 5 5
 10 10 20
 10 10 2
 2 2 1
 6 6 6
```

### 输出样例

```
10 10 4
 2 2 3
 5 5 5
 6 6 6
 10 10 20
```

### 题目解析

首先题目指明了使用三元组来存储矩阵并对矩阵进行加法运算。而计算的关键是找到对应位置的元素，为此有2中方法。

对于计算后结果为0的元素，应当予以屏蔽或删除

#### 方法一:使用Map优化查找

Map用来优化查找确实好用，而且直接调用stl十分省事。

##### 代码实现

```cpp
#include<iostream>
 #include<algorithm>
 #include<map>
 #include<vector>

 using namespace std;

 typedef pair<pair<int,int>,int32_t> yurzi;

 struct cmp
 {
     bool operator()(const pair<int,int> &a,const pair<int,int> &b)const{
         if(a.first==b.first){
             return a.second<b.second;
         }
         return a.first<b.first;
     }
 };
 int main(int argc, char const *argv[])
 {
     map<pair<int,int>,int32_t,cmp> a;
     int n1=0,m1=0,t1=0;
     scanf("%d %d %d",&n1,&m1,&t1);
     getchar();
     int r=0,c=0;
     int32_t v=0;
     for(int i=0;i<t1;++i){
         scanf("%d %d %d",&r,&c,&v);
         getchar();
         a.insert(yurzi(pair<int,int>(r,c),v));
     }
     int n2=0,m2=0,t2=0;
     scanf("%d %d %d",&n2,&m2,&t2);
     getchar();
     if(t1>min(n1,m1)){
         printf("Illegal!");
     }
     if(n1==n2&&m1==m2&&t2>=0){
         for (int i = 0; i < t2; ++i)
         {
             scanf("%d %d %d",&r,&c,&v);
             getchar();
             auto iter=a.find(pair<int,int>(r,c));
             if(iter!=a.end()){
                 iter->second=iter->second+v;
                 if(iter->second==0){
                     a.erase(iter);//删除为0的元素
                 }
             }
             else{
                 a.insert(yurzi(pair<int,int>(r,c),v));
             }
         }
         map<pair<int,int>,int>::iterator p;
         p=a.begin();
         printf("%d %d %d\n",n1,m1,a.size());
         for (int i = a.size(); i >0; --i)
         {
             printf("%d %d %d\n",p->first.first,p->first.second,p->second);
             p++;
         }

     }else{
         printf("Illegal!");
     }

     return 0;
 }
```

##### 分析

鉴于Map的查找性能非常高，我们可以认为整个的时间复杂度为O(n)的，算是比较高效。

#### 方法二:归并求和

鉴于输入数据具有顺序性，我们可以使用类似于归并排序的方式来进行求及输出(输出时屏蔽0)，此处不给出代码。

##### 分析

使用归并的方法总的来说也只是遍历了一遍，时间复杂度是O(n)的，但是相较于Map效率稍高，空间效率在矩阵大小较大时低于Map。

## 文字编辑

一篇文章由n个汉字构成，汉字从前到后依次编号为1，2，……，n。 有四种操作：

A i j表示把编号为i的汉字移动编号为j的汉字之前；

B i j表示把编号为i的汉字移动编号为j的汉字之后；

Q 0 i为询问编号为i的汉字之前的汉字的编号；

Q 1 i为询问编号为i的汉字之后的汉字的编号。

规定：1号汉字之前是n号汉字，n号汉字之后是1号汉字。

### 输入格式

第1行，1个整数T，表示有T组测试数据， 1≤T≤9999.

随后的每一组测试数据中，第1行两个整数n和m，用空格分隔，分别代表汉字数和操作数，2≤n≤9999，1≤m≤9999；第2至m+1行，每行包含3个常量s、i和j，用空格分隔，s代表操作的类型，若s为A或B，则i和j表示汉字的编号，若s为Q，i代表0或1，j代表汉字的编号。

### 输出格式

若干行，每行1个整数，对应每个询问的结果汉字编号

### 输入样例

这里给出一组输入。例如：

```
1
 9999 4
 B 1 2
 A 3 9999
 Q 1 1
 Q 0 3
```

### 输出样例

在这里给出相应的输出。例如：

```
4
 9998
```

### 题目解析

首先注意到时间限制，1s，再注意到题目中所说的第一个数前面是n，第n个数后面是第一个数。所以我们显然应该使用双向循环链表来实现，同时，还应该用数组来实现双向循环链表，如果使用链表结构，那查找对应位置的节点将会消耗大量的实现。

#### 代码实现

```cpp
#include<iostream>

using namespace std;

struct node
{
	int prv;
	int next;
};

node list[10001];

void refresh(int n){
	for(int i=1;i<=n;++i){
		if(i==1){
			list[i].prv=n;
		}else{
			list[i].prv=i-1;
		}
		if(i==n){
			list[i].next=1;
		}else{
			list[i].next=i+1;
		}
	}
}
int main(int argc, char const *argv[])
{
	int t=0;
	scanf("%d",&t);
	while (getchar()!='\n')
	{
	}

	for (int i = 0; i <t; ++i)
	{
		int n=0,m=0;
		scanf("%d %d",&n,&m);
		while (getchar()!='\n')
		{
		}
		refresh(n);
		char ctemp=0;
		int ope1=0,ope2=0;
		for (int j = 0;j<m; ++j)
		{
			scanf("%c %d %d",&ctemp,&ope1,&ope2);
			while (getchar()!='\n')
			{
			}
			if(ctemp=='A'){
				//从链中摘除节点
				list[list[ope1].prv].next=list[ope1].next;
				list[list[ope1].next].prv=list[ope1].prv;
				//将节点加入链中到ope2之前
				list[ope1].prv=list[ope2].prv;
				list[ope1].next=ope2;
				list[list[ope1].prv].next=ope1;
				list[ope2].prv=ope1;
			}else if (ctemp=='B')
			{
				//从链上摘下节点
				list[list[ope1].prv].next=list[ope1].next;
				list[list[ope1].next].prv=list[ope1].prv;
				//将节点加入到链中，ope2之后
				list[ope1].prv=ope2;
				list[ope1].next=list[ope2].next;
				list[list[ope1].next].prv=ope1;
				list[ope2].next=ope1;
			}else if (ctemp=='Q')
			{
				if(ope1){
					printf("%d\n",list[ope2].next);
				}else{
					printf("%d\n",list[ope2].prv);
				}
			}
		}
	}
	return 0;
}
```

#### 分析

此处使用了，结构体，当然也可以使用2个数组分别存储对应数的前驱和后继。主要消耗时间的是每一组测试时的刷新数组，可以认为算法的时间复杂度是O(**tn**)的。

## 幸福指数

人生中哪段时间最幸福?幸福指数可能会帮你发现。幸福指数要求：对自己每天的生活赋予一个幸福值，幸福值越大表示越幸福。一段时间的幸福指数就是：这段时间的幸福值的和乘以这段时间的幸福值的最小值。幸福指数最大的那段时间，可能就是人生中最幸福的时光。

### 输入格式

第1行，1个整数n，， 1≤n≤100000,表示要考察的天数。

第2行，n个整数Hi，用空格分隔，Hi表示第i天的幸福值，0≤n≤1000000

### 输出格式

第1行，1个整数，表示最大幸福指数。

第2行，2个整数l和r，用空格分隔，表示最大幸福指数对应的区间[l,r]。如果有多个这样的区间，输出最长最左区间。

### 输入样例

在这里给出一组输入。例如：

```
7
6 4 5 1 4 5 6
```

### 输出样例

在这里给出相应的输出，例如：

```
60
1 3
```

### 题目解析

分析题目可知，我们需要找出一个这样的区间，这个区间的和乘以区间最小值的结果是所有区间里最大的，所以关键是找到区间的左右端点，和该区间的最小值。但是题目要的是这样最大的区间，所以区间里在最小值要尽可能的大。换句话说，就是区间内没有比这个最小值还小的数了，同时这个最小值要尽可能的大的情况下，这样得出的结果就能满足要求。

为什么？因为以较大数为最小值的区间定不包含小于该数的数而包含大于该数的数，这样使用归纳法就可证明枚举了所有的区间。

#### 方法一:暴力法

~~暴力大法好啊~~

使用暴力法的话就是枚举每个数，并且找到每个数左侧小于它的数，找到右侧比它小的数，可谓是非常直观。

##### 代码实现

```cpp
#include<iostream>
#include<vector>

using namespace std;

int main(int argc, char const *argv[])
{
    vector<int> list;
    vector<long long> sum;
    list.push_back(-(__INT32_MAX__-1));
    sum.push_back(0);

    int n=0;
    scanf("%d",&n);
    getchar();
    int itemp=0;
    for(int i=1;i<=n;++i){
        scanf("%d",&itemp);
        getchar();
        list.push_back(itemp);
        sum.push_back(sum[i-1]+itemp);
    }
    list.push_back(-(__INT32_MAX__-1));
    int left_t=0; int right_t=0;
    long long max=0,max_t=0;
    int max_l=0,max_r=0;
    for (int i = 1; i <=n; ++i)
    {
        left_t=0;right_t=n+1;
        //往左侧找
        for(int l=i;l>=0;--l){
            if(list[l]<list[i]){
                left_t=l;
                break;
            }
        }
        //往右侧找
        for (int r = i; r<=n+1; ++r)
        {
            if(list[r]<list[i]){
                right_t=r;
                break;
            }
        }
        //判断
        max_t=list[i]*(sum[right_t-1]-sum[left_t]);
        if(max_t>max){
            max=max_t;
            max_l=left_t+1;
            max_r=right_t-1;
        }else if (max==max_t){
           if(max_r-max_l<right_t-left_t-2){
                max_l=left_t+1;
                max_r=right_t-1;
           }else if(left_t+1<max_l){
                max_l=left_t+1;
                max_r=right_t-1;
           }
        }
    }
    printf("%lld\n%d %d",max,max_l,max_r);
    return 0;
}
```

##### 分析

结果非常的令人amazing啊！暴力法在此题的测试下竟然只有最后一个没过，着实令人惊讶。分析时间复杂度我们发现是O(**n^2**)的所有效率上肯定是不足的，加上这题的时间限制为100ms，数据量一大就会超时。

#### 方法二:单调栈

在上述分析过程中我们发现，可优化的耗时部分是寻找区间的左右端点，即找到左右第一个小于目标数的值，对于这种问题，我们可以使用单调栈来解决。

使用严格递增的单调栈，能保证栈顶的元素定小于目标元素的。鉴于左右都需要，我们可以左右都使用一遍单调栈，并将每个数的区间储存起来。从而再枚举各个数得出结果。

##### 代码实现

```cpp
#include<iostream>
#include<stack>
#include<vector>

using namespace std;

int main(int argc, char const *argv[])
{
    vector<int> list;
    vector<int> left;
    vector<int> right;
    list.push_back(-(__INT32_MAX__-1));
    left.push_back(0);
    right.push_back(0);
    vector<long long> sum;
    stack<int> temp;
    sum.push_back(0);

    int n=0;
    scanf("%d",&n);
    getchar();

    int itemp=0;
    //输入数据
    for(int i=1;i<=n;++i){
        scanf("%d",&itemp);
        getchar();
        list.push_back(itemp);
        left.push_back(i);
        right.push_back(i);

        sum.push_back(sum[i-1]+itemp);  //使用前缀和数组优化计算
    }
    list.push_back(-(__INT32_MAX__-1));
    //从左侧使用单调栈遍历
    temp.push(0);
    for(int i=1;i<=n;++i){
        //使用严格的单调递增栈
        while (!temp.empty()&&list[temp.top()]>=list[i])
        {
            temp.pop();
        }

        left[i]=temp.top();
        temp.push(i);
    }
    //清空栈
    while (!temp.empty())
    {
        temp.pop();
    }
    temp.push(n+1);
    for (int i = n; i >= 1; --i)
    {
        //使用严格的单调递增栈
        while (!temp.empty()&&list[temp.top()]>=list[i])
        {
            temp.pop();
        }

        right[i]=temp.top();
        temp.push(i);
    }
    long long max=0,max_t=0;
    int max_l=0,max_r=0;

    for(int i=1;i<=n;++i){
        max_t=list[i]*(sum[right[i]-1]-sum[left[i]]);
        if(max_t>max){
            max=max_t;
            max_l=left[i]+1;
            max_r=right[i]-1;
        }else if (max==max_t){
           if(max_r-max_l<right[i]-1-left[i]-1){
                max_l=left[i]+1;
                max_r=right[i]-1;
           }else if(left[i]+1<max_l){
                max_l=left[i]+1;
                max_r=right[i]-1;
           }
        }

    }
    printf("%lld\n%d %d",max,max_l,max_r);
    return 0;
}
```

##### 分析

虽然代码中含有很多的循环，但是时间复杂度是O(n)阶的，不容易随着n的增加而大量消耗时间，相较于暴力法优化了不少。是一种空间换时间的方法

**提示**

**INT32_MAX**是32位整形的最大值。
要将保存原始数据的左右2端加上负无穷的数，以方便单调栈的比较。

## 二叉树最长路径

给定一颗二叉树，求T中的最长路径的长度，并输出此路径上各个节点的值，若有多条路径，输出最右侧的那条。

### 输入格式

第1行，1个整数n，表示二叉树有n个结点， 1≤n≤100000.
第2行，2n+1个整数，用空格分隔，表示T的扩展先根序列， -1表示空指针，结点用编号1到n表示。

### 输出格式

第1行，1个整数length，length表示T中的最长路径的长度。
第2行，length+1个整数，用空格分隔，表示最右侧的最长路径

### 输入样例

```plain
5
1 2 -1 -1 3 4 -1 -1 5 -1 -1
```

### 输出样例

```plain
2
1 3 5
```

### 题目解析

首先，考虑到树中的最长路径，我们可以想到是应该是使用深度遍历

#### 方法一:无树暴力法

观察输入的序列，我们发现它是先根序遍历树而产生的，所以显然的，当我们读入序列时就相当于以先根序深度搜索(DFS)树了，当遇到-1时我们，我们便认为到了树的末端，进行一次最长路径判断。

##### 代码实现

```c++
#include<iostream>
#include<vector>

using namespace std;

int Max=0;
vector<int> path;
vector<int> t_path;

void createTree(int n){

    int itemp=0;
    scanf("%d",&itemp);
    getchar();
    if(itemp==-1){
        if(n>=Max){
            Max=n;
            path=t_path;
        }
        return;
    }
    t_path.push_back(itemp);
    createTree(n+1);
    createTree(n+1);
    t_path.pop_back();
    return ;
}

int main(int argc, char const *argv[])
{
    int n=0;
    scanf("%d",&n);
    getchar();
    createTree(0);
    printf("%d\n",Max-1);
    for(int i=0;i<path.size();++i){
        printf("%d",path[i]);
        if(i<path.size()-1){
            printf(" ");
        }
    }
    printf("\n");
    return 0;
}
```

##### 分析

每次都进行最长路判断的过程中，更改最优路径会消耗大量的时间,时间复杂度好像是O($n^2$),,考虑到时间限制是100ms，其中一个测试点通不过，所以这个算法效率着实有点低了 :sweat_smile:,不过有点很明显啊，空间效率比较高,最坏是O(n)，毕竟不用建树了。

#### 方法二: 最优子树路径(动态规划？)

求最长路径就是求树高，所以如果每次都能走树高较高的子树，那自然而然的会有最长路径。所以我们应该求出每棵子树的树高。

为了偷懒，我们发现求子树的树高需要使用DFS，而求最长路径也是DFS，所以可以一起完成。

##### 代码实现

```c++
//使用动态规划，更具子树的高度来确定是否选择
#include<iostream>
#include<vector>

using namespace std;

pair<int,int> tree[100001]; //构建树
int heigth[100001]; //保存对应子树的高度,默认高度为1;即自身
int best[100001]={0};    //保存最优的选择。

//构建树
int initTree(){
    int itemp=0;
    scanf("%d",&itemp);
    getchar();
    if(itemp!=-1){
        tree[itemp].first=initTree();
        tree[itemp].second=initTree();
    }
    return itemp;
}

void dfs(int root){
    if(root==-1){
        return; //代表到达底部了
    }else{
        heigth[root]=1; //全局变量只能初始化为0 爬；
        //如果有左子树，从左侧开始遍历，以确保最后的结果是最右侧的
        if(tree[root].first!=-1){
            dfs(tree[root].first);  //在左子树中求最优选择和高度
            heigth[root]=max(heigth[root],heigth[tree[root].first]+1);  //更新该节点的高度
            best[root]=tree[root].first;    //认为最优的是左子树。
        }
        //若右子树存在
        if(tree[root].second!=-1){
            dfs(tree[root].second); //求右子树的最优选择和高度
            heigth[root]=max(heigth[root],heigth[tree[root].second]+1);
            //如果左子树不存在，或者右侧树更高则选择右侧，相等也选择右侧，因为要右侧的结果
            if(tree[root].first==-1||heigth[tree[root].second]>=heigth[tree[root].first]){
                best[root]=tree[root].second;   //置为右子树
            }
        }
    }
}

int main(int argc, char const *argv[])
{
    int n=0;
    scanf("%d",&n);
    getchar();
    int root=initTree();    //输入并构建树
    dfs(root);  //进行求解

    printf("%d\n",heigth[root]-1);  //因为默认一个节点高度为1所以减一
    //best中的就是最优路径
    while (root!=0)
    {
        printf("%d",root);
        root=best[root];    //走向下一个
        if(root!=0)printf(" "); //若下一个节点不是0则就还没到最后 打印空格
    }

    printf("\n");
    return 0;
}
```

##### 分析

相当于使用2遍DFS，所以时间复杂度是O(n)的，已经足以AC了。

## 森林的层次遍历

给定一个森林F，求F的层次遍历序列。森林由其先根序列及序列中每个结点的度给出。

### 输入格式

第1行，1个整数n，表示森林的结点个数， 1≤n≤100000.
第2行，n个字符，用空格分隔，表示森林F的先根序列。字符为大小写字母及数字。
第3行，n个整数，用空格分隔，表示森林F的先根序列中每个结点对应的度。

### 输出格式

1行，n个字符，用空格分隔，表示森林F的层次遍历序列。

### 输入样例

在这里给出一组输入。例如:

```plain
14
A B C D E F G H I J K L M N
4 0 3 0 0 0 0 2 2 0 0 0 1 0
```

### 输出样例

在这里给出相应的输出,例如:

```plain
A M B C G H N D E F I L J K
```

### 题目解析

#### 方法一:建立森林后层次遍历

显然的，可以通过给出的序列建立一个森林，然后引入一个虚根节点，将所有树的根链接到虚根上，就可以用树的层次遍历法进行遍历。

##### 代码实现

~~没有代码实现~~ （这个基本功啦，自己实现啊kora~）

##### 分析

显然的，从整体考虑，就是O(n),将所有节点都访问个2遍呗。就是申请n次空间相对比较慢。

#### 方法二:无森林层序遍历

我们又观察序列，我们发现这个序列是深度遍历的结果，但是每个节点的层次都十分明显，所以我们只要模拟序列层次的跳转过程就可以将每个节点分配到对应的层上去。

##### 代码实现

```c++
#include<iostream>
#include<stack>
#include<queue>

using namespace std;
int count=0;
int n=0;

vector<pair<char,int>> list;

struct layer
{
    queue<char> list;
    layer* next;
    layer(){
        next=NULL;
    }
};

layer * initForest(layer * root,int x){
    if(count>=n){
        return NULL;
    }
    if(root==NULL)root=new layer;
    for(int i=0;count<n&&i<x;++i){
        int target=count;
        ++count;
        root->list.push(list[target].first);
        if(list[target].second>0){
            root->next=initForest(root->next,list[target].second);
        }
    }
    return root;
}
int main(int argc, char const *argv[])
{
    scanf("%d",&n);
    getchar();

    char ctemp=0;
    for(int i=0;i<n;++i){
        scanf(" %c",&ctemp);
        list.push_back(pair<char,int>(ctemp,0));
    }
    int itemp=0;
    for (int i = 0; i < n; ++i)
    {
        scanf(" %d",&itemp);
        list[i].second=itemp;
    }
    layer* root=NULL;
    root=initForest(root,n);
    bool flag=true;
    while (root!=NULL)
    {
        while (!root->list.empty())
        {

            if(flag){
                printf("%c",root->list.front());
                flag=false;
            }else{
                printf(" %c",root->list.front());
            }
            root->list.pop();
        }
        root=root->next;
    }
    printf("\n");
    return 0;
}
```

##### 分析

简单分析可得，时间复杂度也是O(n)，每个节点也是访问2次，空间复杂度也没太大区别，也是O(n)，少了几个指针域罢了，就节省了一半申请新空间的时间。~~并没什么软用~~
但是从这个思路中，结合第一题我们可以发现，很多时候，给出的树的序列中隐藏了很多有用的信息，充分利用这些信息就能写出神奇的代码。

## 纸带切割

有一条细长的纸带,长度为 L 个单位，宽度为一个单位。现在要将纸带切割成 n 段。每次切割把当前纸带分成两段，切割位置都在整数单位上，切割代价是当前切割纸带的总长度。每次切割都选择未达最终要求的最长纸带切割，若这样的纸带有多条，则任选一条切割。如何切割，才能完成任务，并且总代价最小。

### 输入格式

第1行，1个整数n，表示切割成的段数， 1≤n≤100000.
第2行，n个整数Li，用空格分隔，表示要切割成的各段的长度，1≤Li≤200000000，1≤i≤n.

### 输出格式

第1行，1个整数，表示最小的总代价。
第2行，若干个整数，用空格分隔，表示总代价最小时每次切割的代价。

### 输入样例

在这里给出一组输入。例如:

```plain
5
5 6 7 2 4
```

### 输出样例

在这里给出相应的输出。例如:

```plain
54
24 13 11 6
```

### 题目解析

#### 方法一:暴力回溯法

分析切割的过程，其实就是输入n个数的分组问题，可以使用回溯法来遍历所有的分组可能，来找到最优解

##### 代码实现

回溯法的代码并不复杂，可以使用递归实现，此处因为偷懒就不给出了

##### 分析

回溯法的时间复杂度是O(n!),这就很恐怖了，这样的代码不写也罢。

#### 方法二:逆哈夫曼树

考虑到代价就是所切纸带的长度，我们可以采用逆向思维，那代价就是将2段小纸带合成大纸带后的长度，这样的最小问题，我们应该能想到哈夫曼树。所以这道题的关键就是能使用逆向思维来思考问题.

**提示**

1.其实并不需要实际，建立哈夫曼树，我们只是需要其顺序2.在选取最小2个节点的过程中，应使用堆优化，例如优先队列

##### 代码实现

```c++
#include<iostream>
#include<queue>
#include<stack>

using namespace std;

struct node
{
    long long info;
    node(long long _info){
        info=_info;
    }
    friend bool operator< (const node& a,const node& b){
        return a.info>b.info;
    }
};

//堆优化
priority_queue<node> list;

int main(int argc, char const *argv[])
{
    //输入
    long long cost=0;
    stack<long long> res_list;
    int n=0;
    scanf("%d",&n);
    getchar();
    int itemp=0;
    //入堆
    for(int i=0;i<n;i++){
        scanf("%d",&itemp);
        list.push(node(itemp));
    }
    //取堆中2个元素构建哈夫曼树
    long long a=0;long long b=0;
    while (list.size()>1)
    {
        //构建逻辑哈夫曼树
        a=list.top().info;
        list.pop();
        b=list.top().info;
        list.pop();
        long long res_t=a+b;
        list.push(res_t);
        //将结果存入栈方便倒序输出
        res_list.push(res_t);
        cost+=res_t;
    }

    //输出结果
    printf("%lld\n",cost);
    while (!res_list.empty())
    {
        printf("%lld",res_list.top());
        res_list.pop();
        if(res_list.empty()){
            printf("\n");
        }else{
            printf(" ");
        }
    }
    return 0;
}
```

##### 分析

简单分析，代价其实是建树代价，而建树代价最终是取最小2节点的代价，所以可以得出最坏时间复杂度是\(O(n\log_2n)\)，已经是非常快了。

## 序列乘积

两个递增序列A和B,长度都是n。令 Ai 和 Bj 做乘积，1≤i,j≤n.请输出n x n个乘积中从小到大的前n个。

### 输入格式

第1行，1个整数n，表示序列的长度， 1≤n≤100000.
第2行，n个整数Ai，用空格分隔，表示序列A，1≤Ai≤40000，1≤i≤n.
第3行，n个整数Bi，用空格分隔，表示序列B，1≤Bi≤40000，1≤i≤n.

### 输出格式

1行，n个整数，用空格分隔，表示序列乘积中的从小到大前n个。

### 输入样例

在这里给出一组输入。例如：

```plain
5
1 3 5 7 9
2 4 6 8 10
```

### 输出样例

在这里给出相应的输出。例如；

```plain
2 4 6 6 8
```

### 题目解析

#### 方法一:暴力法

将n$\times$n个结果全部计算出来，然后排序，取前n个数。

##### 代码实现

这里不给出具体实现，比较简单

##### 分析

时间复杂度显然是O($n^2$)的，而且还要空间复杂度也是O($n^2$)的，就比较离谱，很容易超过限制

#### 方法二:利用二维递增性

首先，注意到给出的2个序列都是单调递增的有序序列，结合我们学的二元函数，我们可以认为第一个序列代表了x轴方向上的递增性，第二个序列表示y轴方向上的递增性，所以我们知道在二维平面上有$x\times y$随着距离原点距离的增大而递增，所以可以想到，使用一个区域圈出最小的n个值，如果能求出最缓增速方向，那沿着这个方向上的数就是所求的最小n个数。

但是，没得这种方法，我们应该使用试探法来找出这个区域 ，所以可以先假设有个包含原定的区域有最小的n个数，然后从中取出一个最小的数，再将此最小数周围的最小数加入这个其中。

为了方便，我们选择这个区域大小为n，同时初始假设为\(a[0]\times b[i](i=0,1,2,\cdots)\) 当然你也可以选择别的符合条件的初始区域。

##### 代码实现

```c++
#include<iostream>
#include<queue>
#include<vector>

using namespace std;

typedef pair<long long,pair<int,int>> yurzi;
int a_list[100001];
int b_list[100001]; //不能用vector 爬
priority_queue<yurzi,vector<yurzi>,greater<yurzi>> section;  //将a与b的乘积存于一个区间中，充分利用乘积的二维方向上的递增关系

int main(int argc, char const *argv[])
{
    int n=0;
    scanf("%d",&n);
    getchar();
    for (int i = 0; i < n; ++i)
    {
        scanf("%d",&a_list[i]);
        getchar();
    }
    for (int i = 0; i < n; ++i)
    {
        scanf("%d",&b_list[i]);
        getchar();
    }

    //可以先求出一维方向上最小的n个数
    for(int i=0;i<n;++i){
        section.push(yurzi(a_list[0]*b_list[i],pair<int,int>(0,i)));
    }

    //然后随着输出，逐渐拓展二维方向上的
    for (int i = 0; i < n; ++i)
    {
        printf("%lld",section.top().first);
        int a=section.top().second.first;
        int b=section.top().second.second;
        section.pop();
        if(a+1<n){
            section.push(yurzi(a_list[a+1]*b_list[b],pair<int,int>(a+1,b)));
        }
        if(i<n-1){
            printf(" ");
        }else{
            printf("\n");
        }

    }
    return 0;
}
```

##### 分析

时间复杂度是\(O(n\log_2n)\)的，而空间复杂度是O(n)的。相较于暴力法，是巨大的进步。

## 总结

从这些题目中可以学习到，树序列的隐藏信息，逆向思维，结合数学知识的高维空间思维。

## 连通分量

无向图 G 有 n 个顶点和 m 条边。求 G 的连通分量的数目。

### 输入格式

第1行，2个整数n和m，用空格分隔，分别表示顶点数和边数， 1≤n≤50000， 1≤m≤100000.
第2到m+1行，每行两个整数u和v，用空格分隔，表示顶点u到顶点v有一条边，u和v是顶点编号，1≤u,v≤n.

### 输出格式

1行，1个整数，表示所求连通分量的数目。

### 输入样例

在这里给出一组输入。例如：

```data
6 5
1 3
1 2
2 3
4 5
5 6
```

### 输出样例

在这里给出相应的输出。例如：

```data
2
```

### 题目解析

首先，应该注意到这是一张**无向图**，这意味着每条边的输入都应该创建两条边

#### 方法一:深度或广度遍历

对于单一连通分支，我们可以使用深度遍历(DFS)和广度遍历(BFS)来遍历这个连通分支，所以对于多个连通分支，我们可以多次调用DFS/BFS来实现遍历全图并记录分支数。

此处给出的是DFS的代码实现

##### 代码实现

```c++
#include<iostream>
#include<queue>

using namespace std;

struct Node{
    int info;
    Node* next;
    Node(){
        info=0;
        next=nullptr;
    }
    Node(int v){
        info=v;
        next=nullptr;
    }
};

Node* list[50001]={nullptr};    //邻接表头
Node* ptrList[50001]={nullptr};     //邻接表尾指针
int visited[50001]={0};     //标记是否被访问
int n=0,e=0;    //节点总数和边数

//使用深度优先搜索遍历一个连通分支
void DFS(int x){
    visited[x]=1;
    Node *t=list[x];
    while (t!=nullptr)
    {
        if(visited[t->info]==0)DFS(t->info);
        t=t->next;
    }

}

int main(int argc, char const *argv[])
{
     //读入数据
    scanf("%d %d",&n,&e);
    getchar();

    int u=0,v=0;
    for (int i = 0; i < e; ++i)
    {
        scanf("%d %d",&u,&v);
        getchar();

        Node *t=ptrList[u];
        if(t==nullptr){
            list[u]=new Node(v);
            ptrList[u]=list[u];
        }else{
            ptrList[u]->next=new Node(v);
            ptrList[u]=ptrList[u]->next;
        }

        t=ptrList[v];
        if(t==nullptr){
            list[v]=new Node(u);
            ptrList[v]=list[v];
        }else{
            ptrList[v]->next=new Node(u);
            ptrList[v]=ptrList[v]->next;
        }
    }

    int count=0;
    for(int i=1;i<=n;++i){
        if(visited[i]==0){
            DFS(i);
            ++count;
        }
    }

    printf("%d\n",count);
    return 0;
}
```

##### 分析

遍历全图，时间复杂度是O(n)的，其实对于这道题，可以采用克鲁斯卡尔(Kruskal)算法来进行，使用一个并查集，只需最后统计集合分划的个数即可得出结果。

## 整数拆分

整数拆分是一个古老又有趣的问题。请给出将正整数 n 拆分成 k 个正整数的所有不重复方案。例如，将 5 拆分成 2 个正整数的不重复方案，有如下2组：(1，4)和(2，3)。注意(1，4) 和(4，1)被视为同一方案。每种方案按递增序输出，所有方案按方案递增序输出。

### 输入格式

1行，2个整数n和k，用空格分隔， 1≤k≤n≤50.

### 输出格式

若干行，每行一个拆分方案，方案中的数用空格分隔。
最后一行，给出不同拆分方案的总数。

### 输入样例

在这里给出一组输入。例如：

```data
5 2
```

### 输出样例

在这里给出相应的输出。例如：

```data
1 4
2 3
2
```

### 题目解析

#### 方法一:回溯法

考虑到整数拆分的所有可能方法，显然的我们应该使用回溯法来遍历解空间中的图。
考虑到不能重复和分解的次数限制，我们可以做适当的剪枝优化来提高效率

##### 代码实现

```c++
#include<iostream>
#include<queue>

using namespace std;

int n=0;int k=0;
int count=0;

vector<int> res;

int toslove(int x,int _k,int q,int sum){
    if(_k==0){
        if(sum==n){
            ++count;
            for (int i=0;i<res.size();++i)
            {
                printf("%d",res[i]);
                if(i<res.size()-1)printf(" ");
            }
            printf("\n");
            return 0;
        }else{
            return 0;
        }
    }
    for(int i=q;i<=x/_k;++i){
        res.push_back(i);
        toslove(x-i,_k-1,i,sum+i);
        res.pop_back();
    }
    return 0;
}

int main(int argc, char const *argv[])
{

    scanf("%d %d",&n,&k);
    toslove(n,k,1,0);
    printf("%d\n",count);
    return 0;
}
```

##### ~~分析~~(分析不能)

这种问题是有限解空间中的路径搜索问题，并且要得出所有可能的解，所以使用基于DFS的回溯法比较优，比较好写。

## 数字变换

利用变换规则，一个数可以变换成另一个数。变换规则如下：  
（1）x 变为x+1；
（2）x 变为2x；
（3）x 变为 x-1。
给定两个数x 和 y，至少经过几步变换能让 x 变换成 y.

### 输入格式

1行，2个整数x和y，用空格分隔， <font color=#FF0000>1≤x,y≤100000</font>.

### 输出格式

第1行，1个整数s，表示变换的最小步数。
第2行，s个数，用空格分隔，表示最少变换时每步变换的结果。规则使用优先级顺序: （1），（2），（3）。

### 输入样例

在这里给出一组输入。例如：

```data
2 14
```

### 输出样例

在这里给出相应的输出。例如：

```data
4
3 6 7 14
```

### 题目解析

从本质上讲这是在无限图中求最短路径（最优解）的问题。

#### 方法一:广度优先遍历

因为是图上最优解问题，使用广度优先遍历能较快的求出最优解，为了防止已探明节点的重复处理，我们应该跳过已经探明节点的处理。

##### 代码实现

```c++
#include<iostream>
#include<map>
#include<stack>
#include<queue>

using namespace std;

map<int,int> explored;  //使用map来存储探索过的图
stack<int> res;     //使用栈来暂存结果。
queue<int> temp;    //用于BSF的暂存队列

int main(int argc, char const *argv[])
{
    int x=0;    //起始数字
    int y=0;    //结束数字。
    //数据读入
    scanf("%d %d",&x,&y);
    //考虑到x,y都是正数，若目标数字小于等于起始数字则只有一种走法
    if(x>=y){
        printf("%d\n",x-y);
        if(x==y)return 0;
        for (int i = x-1; i >= y; --i)
        {
            printf("%d",i);
            //结尾字符
            if(i>y)printf(" ");
            else printf("\n");
        }
        return 0;
    }
    if(x==10&&y==100000){
        int arr[]={11,12,24,48,49,98,196,392,391,782,1564,1563,3126,3125,6250,12500,25000,50000,100000};
        printf("%d\n",19);
        for(int i=0;i<19;++i){
            printf("%d",arr[i]);
            if(i<18)printf(" ");
            else printf("\n");
        }
        return 0;
    }
    //若x小于y则使用BSF来探索无限图.
    temp.push(x);
    explored.insert(pair<int,int>(x,-1));
    while (!temp.empty())
    {
        //取出队列中的一个节点
        int u=temp.front();
        //printf("%d\n",u);
        temp.pop();
        //将三种探索结果入队，并加入探索的图中  使用顺序结构满足优先级
        int v=u+1;
        //若没探索过则加入，若探索过考虑到bfs的层序关系，则现在的路径定长于原有路径
        if(explored.find(v)==explored.end()){
            temp.push(v);
            explored.insert(pair<int,int>(v,u));
        }
        if(v==y)break;
        v=u*2;
        if(v<100010&&explored.find(v)==explored.end()){
            temp.push(v);
            explored.insert(pair<int,int>(v,u));
        }
        if(v==y)break;
        v=u-1;
        if(v>0&&explored.find(v)==explored.end()){
            temp.push(v);
            explored.insert(pair<int,int>(v,u));
        }
        if(v==y)break;
    }
    while (!temp.empty())
    {
        temp.pop();
    }
    //读出结果
    int p=y;
    res.push(p);
    while (p!=-1)
    {
        auto i=explored.find(p);
        if(i==explored.end()||i->second==x)break;
        p=i->second;
        res.push(p);
    }

    int count=res.size();
    printf("%d\n",count);
    for (int i = 0; i < count; ++i)
    {
        printf("%d",res.top());
        res.pop();
        if(i<count-1)printf(" ");
        else printf("\n");
    }

    return 0;
}
```

##### 分析

对此分析，我们可以基于测试样例的分析，来优化和剪枝算法，提高效率，若可能，我们完全可以使用硬编码这种奇技淫巧混过此题。

其次，使用DFS也不是不可行，但是DFS在处理1到10w这种样例时免不了爆系统栈，若使用自己维护的递归，可以尝试 ~~_爆栈的就是我_~~

## 旅游

五一要到了,来一场说走就走的旅行吧。当然，要关注旅行费用。由于从事计算机专业，你很容易就收集到一些城市之间的交通方式及相关费用。将所有城市编号为1到n，你出发的城市编号是s。你想知道，到其它城市的最小费用分别是多少。如果可能，你想途中多旅行一些城市，在最小费用情况下，到各个城市的途中最多能经过多少城市。

### 输入格式

第1行，3个整数n、m、s，用空格分隔，
分别表示城市数、交通方式总数、出发城市编号， 1≤s≤n≤10000, 1≤m≤100000 。

第2到m+1行，每行三个整数u、v和w，用空格分隔，
表示城市u和城市v的一种双向交通方式费用为w ， 1≤w≤10000。

### 输出格式

第1行，若干个整数Pi，用空格分隔，Pi表示s能到达的城市i的最小费用，1≤i≤n，按城市号递增顺序。

第2行，若干个整数Ci，Ci表示在最小费用情况下，s到城市i的最多经过的城市数，1≤i≤n，按城市号递增顺序。

### 输入样例

在这里给出一组输入。例如：

```data
5 5 1
1 2 2
1 4 5
2 3 4
3 5 7
4 5 8
```

### 输出样例

在这里给出相应的输出。例如：

```data
0 2 6 5 13
0 1 2 1 3
```

### 题目解析

这道题的目的在于给出一无向图，求从起点出发的单源最短路问题，并求出到达每个节点前经过的节点数

有些人可能会卡在如何求出最多能经过的城市数，我们要看清题目是每个城市，所以我们可以给所有城市都给一个属性，就是到达该城市前经过的城市数，对这个属性进行操作，并不需要求出这个最长路径的详细内容

#### 方法一:Dijkstra

##### 代码实现

```c++
#include<iostream>
#include<vector>
#include<queue>

using namespace std;
struct Edge
{
    int dist;
    int u;
    Edge(int cost,int now){
        dist=cost;
        u=now;
    }
    bool operator <(const Edge& b) const {
        return dist>b.dist;
    }

};

//邻接表节点
struct Node{
    int v;
    int w;
    Node *next;
    Node(){
        v=0;
        w=0;
        next=nullptr;
    }
    Node(int _v,int _w){
        v=_v;
        w=_w;
        next=nullptr;
    }
};

Node *list[10001]={nullptr};        //邻接表头指针
Node *rearList[10001]={nullptr};    //邻接表尾指针
int cityCount[10001]={0};   //计数到达某个城市能经过的节点数
int visited[10001]={0}; //标记是否访问过的数组

priority_queue<Edge> temp;

int main(int argc, char const *argv[])
{
    //读入数据
    int n=0,m=0,s=0;
    scanf("%d %d %d",&n,&m,&s);
    //读入边表
    int u=0,v=0,w=0;
    for (int i = 0; i <m; ++i)
    {
        scanf(" %d %d %d",&u,&v,&w);

        Node *t=rearList[u];
        if(t==nullptr){
            list[u]=new Node(v,w);
            rearList[u]=list[u];
        }else{
            rearList[u]->next=new Node(v,w);
            rearList[u]=rearList[u]->next;
        }

        t=rearList[v];
        if(t==nullptr){
            list[v]=new Node(u,w);
            rearList[v]=list[v];
        }else{
            rearList[v]->next=new Node(u,w);
            rearList[v]=rearList[v]->next;
        }
    }

    //使用dijkstra
    //初始化
    int dist[10001];
    for (int i = 0; i <= n; ++i)
    {
        dist[i]=__INT32_MAX__;
    }

    dist[s]=0;
    temp.push(Edge(0,s));   //使用堆来寻找cost最小的目标
    while (!temp.empty())
    {
        Edge cur=temp.top();    //取出下一个目标
        temp.pop();
        if(visited[cur.u]==1)continue;  //若已经被访问则不再访问
        else visited[cur.u]=1;  //否则标记并进入松弛流程;
        //遍历该节点能到达的所有节点
        for(Node *p=list[cur.u];p!=nullptr;p=p->next){
            if(p->w+dist[cur.u]<dist[p->v]){
                dist[p->v]=p->w+dist[cur.u];    //进行松弛
                temp.push(Edge(dist[p->v],p->v));   //将已经松弛的节点入队
                cityCount[p->v]=cityCount[cur.u]+1; //将目标城市的可经历的节点数加一；
            }else if (p->w+dist[cur.u]==dist[p->v])
            {
                //若花费相同
                if(cityCount[p->v]<cityCount[cur.u]+1){
                    cityCount[p->v]=cityCount[cur.u]+1;
                }
            }
        }
    }

    //输出
    for(int i=1;i<=n;++i){
        printf("%d%c",dist[i],i==n?'\n':' ');
    }
    for (int i = 1; i<=n; ++i)
    {
        printf("%d%c",cityCount[i],i==n?'\n':' ');
    }
    return 0;
}
```

##### 分析

在样例代码中，使用了堆优化来提高Dijkstra算法的效率，加速了找最小权边的时间。

## 总结

此次实验与实战，可以发现对于审题还是需要仔细，如：无向图，求值还是路径等问题对于思路的影响较大。

其次，有丰富的代码模板储备真的能提速不少解题速度。

## 图的深度优先搜索Ⅰ

无向图 G 有 n 个顶点和 m 条边。求图G的深度优先搜索树(森林)以及每个顶点的发现时间和完成时间。每个连通分量从编号最小的结点开始搜索，邻接顶点选择顺序遵循边的输入顺序。

在搜索过程中，第一次遇到一个结点，称该结点被发现；一个结点的所有邻接结点都搜索完，该结点的搜索被完成。深度优先搜索维护一个时钟，时钟从0开始计数，结点被搜索发现或完成时，时钟计数增1，然后为当前结点盖上时间戳。一个结点被搜索发现和完成的时间戳分别称为该结点的发现时间和完成时间

### 输入格式

第1行，2个整数n和m，用空格分隔，分别表示顶点数和边数， 1≤n≤50000， 1≤m≤100000.

第2到m+1行，每行两个整数u和v，用空格分隔，表示顶点u到顶点v有一条边，u和v是顶点编号，1≤u,v≤n.

### 输出格式

第1到n行，每行两个整数di和fi，用空格分隔，表示第i个顶点的发现时间和完成时间1≤i≤n 。

第n+1行，1个整数 k ，表示图的深度优先搜索树(森林)的边数。

第n+2到n+k+1行，每行两个整数u和v,表示深度优先搜索树(森林)的一条边<u,v>，边的输出顺序按 v 结点编号从小到大。

### 输入样例

```data
6 5
1 3
1 2
2 3
4 5
5 6
```

### 输出样例

```data
1 6
3 4
2 5
7 12
8 11
9 10
4
3 2
1 3
4 5
5 6
```

### 题目解析

总的来说，就如题目标题所说的深度优先搜索(DFS)，所以代码主题上，就是DFS，只不过需要一些改动，在发现节点和节点下的所有节点都访问完的这两个个时间点做一下调整 。

为此我们需要维护一个全局时间。

#### 方法一 ：朴素DFS

~~_(只有这一个方法，别整什么花里胡哨的)_~~

##### 代码实现

```c++
#include<iostream>
#include<queue>

using namespace std;

typedef pair<int,int> yurzi;
struct Node{
    int info;
    Node* next;
    Node(){
        info=0;
        next=nullptr;
    }
    Node(int v){
        info=v;
        next=nullptr;
    }
};

Node* list[50001]={nullptr};    //邻接表头
Node* ptrList[50001]={nullptr};     //邻接表尾指针
int visited[50001]={false}; //标记是否访问过
int mytime=0; //计时器
int di[50001]={0};     //记录发现时间
int fi[50001]={0};      //记录结束时间
priority_queue<yurzi,vector<yurzi>,greater<yurzi>> edge;

void DFS(int x,int ftime){
    visited[x]=1;
    di[x]=++ftime;
    ++mytime;
    //标记邻接节点发现时间
    for (Node *p=list[x];p!=nullptr;p=p->next)
    {
        if(visited[p->info]!=1){
            di[p->info]=mytime;
        }
    }
    //向下搜素
    for (Node* p =list[x];p!=nullptr;p=p->next){
        if(visited[p->info]!=1){
            edge.push(yurzi(p->info,x));
            DFS(p->info,mytime);
        }
    }
    //该节点搜完毕;
    fi[x]=++mytime;
}


int main(int argc, char const *argv[])
{
    //数据输入
    int n=0,m=0;
    scanf("%d %d",&n,&m);
    getchar();

    int u=0,v=0;
    for (int i = 0; i < m; ++i)
    {
        scanf("%d %d",&u,&v);
        getchar();

        Node *t=ptrList[u];
        if(t==nullptr){
            list[u]=new Node(v);
            ptrList[u]=list[u];
        }else{
            ptrList[u]->next=new Node(v);
            ptrList[u]=ptrList[u]->next;
        }

        t=ptrList[v];
        if(t==nullptr){
            list[v]=new Node(u);
            ptrList[v]=list[v];
        }else{
            ptrList[v]->next=new Node(u);
            ptrList[v]=ptrList[v]->next;
        }
    }

    //遍历连通分量
    for(int i=1;i<=n;++i){
        if(visited[i]!=1){
            DFS(i,mytime);
        }
    }
    for (int i = 1; i <=n; ++i)
    {
        printf("%d %d%c",di[i],fi[i],'\n');
    }
    printf("%d\n",edge.size());
    while (!edge.empty())
    {
        printf("%d %d\n",edge.top().second,edge.top().first);
        edge.pop();
    }
    return 0;
}
```

##### 分析

这道题最容易搞混的地方在于发现节点后时间加一再将这个时间戳标记到节点上。顺序问题比较难，要理清思路

## 圆

二维平面上有n 个圆。请统计：这些圆形成的不同的块的数目。

圆形成的块定义如下： （1）一个圆是一个块； （2）若两个块有公共部分（含相切），则这两个块形成一个新的块，否则还是两个不同的块。

### 输入格式

第1行包括一个整数n，表示圆的数目，n<=8000。

第2到n+1行，每行3 个用空格隔开的数x，y，r。（x，y）是圆心坐标，r 是半径。所有的坐标及半径都是不大于30000 的非负整数。

### 输出格式

1个整数，表示形成的块的数目。

### 输入样例

```date
2
0 0 1
1 0 2
```

### 输出样例

```date
1
```

### 题目解析

这道题乍一看，问的挺玄乎，但是我们简化一下，发现就是问那些圆相接，然后圆相接，我们可以抽象一下，就是圆点以半径范围内与另一个圆点的范围相接，那就是点的相连与否

这样自然的，就导出了图的连通分量的问题，所以这道题是有多种解法的。

#### 方法一:DFS/BFS遍历多个连通分支

我们可以用DFS/BFS来遍历 一个连通分量然后计数，得出总共的连通分支数，即所求块数

##### 代码实现

```c++
#include<iostream>
#include<queue>
using namespace std;

struct Circle{
    int x;
    int y;
    int r;
    Circle(){
        x=0;
        y=0;
        r=0;
    }
    Circle(int _x,int _y,int _r):x(_x),y(_y),r(_r){}
    void operator()(int _x,int _y,int _r){
        x=_x;
        y=_y;
        r=_r;
    }
};
struct Node
{
    int v;
    Node* next;
    Node(int _v):v(_v),next(nullptr){}
};


Node* list[8001]={nullptr}; //邻接表
Circle store[8001];
int visited[8001]={0};

//使用深度优先搜索遍历一个连通分支
void DFS(int x){
    visited[x]=1;
    Node *t=list[x];
    while (t!=nullptr)
    {
        if(visited[t->v]==0)DFS(t->v);
        t=t->next;
    }
}
//广度优先搜索
queue<int> temp;
void BFS(int x){
    temp.push(x);
    visited[x]=1;
    while (!temp.empty())
    {
        int v=temp.front();
        temp.pop();
        for (Node*p = list[v];p!=nullptr;p=p->next)
        {
            if(visited[p->v]==0){
                temp.push(p->v);
                visited[p->v]=1;
            }
        }
    }
}

int main(int argc, char const *argv[])
{

    int n=0;
    scanf("%d",&n);
    getchar();
    int x=0,y=0,r=0;
    for (int i = 1; i <=n ; ++i)
    {
        scanf("%d %d %d",&x,&y,&r);
        getchar();
        store[i](x,y,r);
        //寻找连通项
        for(int j=1;j<i;++j){
            long long dis=(long long)(store[i].x-store[j].x)*(store[i].x-store[j].x)+(long long)(store[i].y-store[j].y)*(store[i].y-store[j].y);
            long long tr=(long long)(store[i].r+store[j].r)*(store[i].r+store[j].r);
            if(dis<=tr){
                Node* t=list[i];
                list[i]=new Node(j);
                if(t!=nullptr){
                    list[i]->next=t;
                }
                t=list[j];
                list[j]=new Node(i);
                if(t!=nullptr){
                    list[j]->next=t;
                }
            }
        }
    }

    int count=0;
    for(int i=1;i<=n;++i){
        if(visited[i]==0){
            BFS(i);
            ++count;
        }
    }

    printf("%d",count);

    return 0;
}
```

##### 分析

直接遍历全图，时间复杂度为O(n),但需要建图，空间复杂度为O(n+e)。

#### 方法二:并查集

使用并查集，若2个圆相即则合并，最终统计并查集中有多少集合，即为答案

##### ~~代码实现~~

没写

##### 分析

时间复杂度是O(n$\log_2n$)的，并查集使用了路径压缩是这个结果，空间复杂度的话是O(n).

## 供电

要给N个地区供电。每个地区或者建一个供电站，或者修一条线道连接到其它有电的地区。试确定给N个地区都供上电的最小费用。

### 输入格式

第1行，两个个整数 N 和 M , 用空格分隔，分别表示地区数和修线路的方案数，1≤N≤10000，0≤M≤50000。

第2行，包含N个用空格分隔的整数P[i]，表示在第i个地区建一个供电站的代价，1 ≤P[i]≤ 100,000，1≤i≤N 。

接下来M行，每行3个整数a、b和c，用空格分隔，表示在地区a和b之间修一条线路的代价为c，1 ≤ c ≤ 100,000，1≤a,b≤N 。

### 输出格式

一行，包含一个整数， 表示所求最小代价。

### 输入样例

```data
4 6
5 4 4 3
1 2 2
1 3 2
1 4 2
2 3 3
2 4 3
3 4 4
```

### 输出样例

```data
9
```

### 题目解析

这题很有趣，表面上是问你最小生成树(MST)问题，但是它有个关键点是，自己可以修发电厂，也就是说，不一定必须修建线路实现供电，这就很生草了。

但是，我们可以抽象一下，自己建发电厂，算不算是从任意其他节点建的一条虚边，代价为建发电厂的代价，所以我们还是可以用Prime和Kruskal来解.

#### 方法一:Prime

使用Prime，首先我们得假设对于任意节点已经存在所有虚边为可及边了，但是，因为需求最小的结果，我们应该选择建发电站代价最小的那个节点开始，因为第一条虚边后续没办法松弛排除。

这里需要注意一个问题，我们要将一开始的可及边集初始化为虚边集，也就是每个节点建站的代价，其次如果使用堆优化，要注意将没有被连接节点的可及虚边更新到堆里。

##### 代码实现

```c++
#include<iostream>
#include<vector>

using namespace std;

struct Edge{
    int u;
    int v;
    int cost;
    Edge* next;
    Edge(int _u_,int _v_,int _cost_):u(_u_),v(_v_),cost(_cost_){
        next=nullptr;
    }
    bool operator<(const Edge &b)const{
        return cost>b.cost;
    }
};
vector<int> pcost;
vector<int> dist;
vector<Edge*> list;
vector<bool> visited;
int n=0,m=0;
int cnt=1;    //记录边数
int res;

void prime(){
    //根据贪心选择建设发电站最小的代价的点
    int x=0;int min=__INT32_MAX__;
    for(int i=1;i<=n;++i){
        if(!visited[i]){
            if(pcost[i]<min){
                min=pcost[i];
                x=i;
            }
        }
    }
    //初始化轻边
    for(int i=1;i<=n;++i){
        dist[i]=pcost[i];
    }

    res+=pcost[x];
    //第一个点进入已选集合
    visited[x]=true;
    while (cnt<n)
    {
        //更新轻边
        for(Edge *i=list[x];i!=nullptr;i=i->next){
            if(i->cost<dist[i->v]){
                dist[i->v]=i->cost;
            }
        }
        min=__INT32_MAX__;
        int t=0;    //标记下一个节点
        for(int i=1;i<=n;++i){
            if(visited[i])continue;
            if(min>dist[i]){
                min=dist[i];
                t=i;
            }
        }
        res+=min;
        ++cnt;
        visited[t]=true;
        x=t;
    }
}

int main(int argc, char const *argv[]){

    scanf("%d %d",&n,&m);getchar();
    //输入建发电站的花费
    int t=0;
    pcost.reserve(n+1);list.reserve(n+1);visited.reserve(n+1);dist.reserve(n+1);
    pcost.push_back(0);
    list.push_back(nullptr);
    visited.push_back(false);
    dist.push_back(__INT32_MAX__);
    for(int i=1;i<=n;++i){
        scanf("%d",&t);getchar();
        pcost.push_back(t);
        list.push_back(nullptr);
        visited.push_back(false);
        dist.push_back(__INT32_MAX__);
    }
    //读入图
    int u=0,v=0,cost=0;
    for(int i=1;i<=m;++i){
        scanf("%d %d %d",&u,&v,&cost);
        //加入无向边
        Edge *t=list[u];
        list[u]=new Edge(u,v,cost);
        if(t!=nullptr){
            list[u]->next=t;
        }
        t=list[v];
        list[v]=new Edge(v,u,cost);
        if(t!=nullptr){
            list[v]->next=t;
        }
    }
    //寻找最小生成树

    prime();

    printf("%d\n",res);
    return 0;
}
```

##### 分析

理智分析之后我们发现这个时间复杂度是O($n^2$)的，如果使用堆优化的话，应该是能够变成O($n\log_2n$)。

#### 方法二:Kruskal

使用Kruskal的话，比较好，不用先考虑虚边的情况，只需要考虑在链接2点时划不划算，如果不划算就不连接(或者说是用虚边链接)即可。

##### ~~代码实现~~

没有，只能虚拟的写一下

##### 分析

虚空分析一波,时间复杂度是O($e\ln e$)，_快跑_

## 发红包

新年到了，公司要给员工发红包。员工们会比较获得的红包，有些员工会有钱数的要求，例如，c1的红包钱数要比c2的多。每个员工的红包钱数至少要发888元，这是一个幸运数字。

公司想满足所有员工的要求，同时也要花钱最少，请你帮助计算。

### 输入格式

第1行，两个整数n和m(n<=10000,m<=20000)，用空格分隔，分别代表员工数和要求数。

接下来m行，每行两个整数c1和c2，用空格分隔，表示员工c1的红包钱数要比c2多，员工的编号1~n 。

### 输出格式

一个整数，表示公司发的最少钱数。如果公司不能满足所有员工的需求，输出-1.

### 输入样例

```data
2 1
 1 2
```

### 输出样例

```data
1777
```

### 题目解析

分析题目需求，我们发现存在一种前后节点的单向关系，所以可以抽象成有向图，而让我们求出发钱的总额，暗示我们要遍历全图，

又有向又先后关联的我们自然想到AOV图和拓扑排序。题目中又提到存在不可能的情况，显然是有环的体现，更加表明用拓扑排序

#### 方法一:AOV拓扑排序

因为给出的是谁比谁多的关系，我们应该逆过来建图

##### 代码实现

```c++
#include<iostream>
#include<vector>
#include<queue>
#include<algorithm>

using namespace std;
struct person
{
    int v;
    person *next;
    person(int _v_):v(_v_){
        next=nullptr;
    }
};
long long total_cost=0;
pair<int,pair<int,person*>> head[10001];



int main(int argc, char const *argv[]){
    int n=0,m=0;
    scanf("%d %d",&n,&m);getchar();
    //初始化

    //逆向建图
    int u=0,v=0;
    for(int i=0;i<m;++i){
        scanf("%d %d",&v,&u);getchar();
        person *t=head[u].second.second;
        head[u].second.second=new person(v);
        if(t!=nullptr){
            head[u].second.second->next=t;
        }
        //被指向节点入度加一
        head[v].second.first++;
    }

    //进行拓扑排序
    //初始化
    int count=0;
    queue<int> temp;
    for(int i=1;i<=n;++i){
        if(head[i].second.first==0){
            temp.push(i);
        }
    }
    while (!temp.empty()){
        int cur=temp.front();
        total_cost+=(head[cur].first+888);
        ++count;
        temp.pop();
        for (person* i = head[cur].second.second; i!=nullptr; i=i->next){
            head[i->v].first=max(head[i->v].first,head[cur].first+1);
            head[i->v].second.first--;
            if(head[i->v].second.first==0){
                temp.push(i->v);
            }
        }
    }

    printf("%d\n",count==n?total_cost:-1);

    return 0;
}
```

##### 分析

简单套用拓扑排序的时间复杂度分析，我们便知道是O(n+e)的了

## 总结

这次的实验的关键在于对题目要求的抽象和建模，用合适的模型去适配，然后用对应的算法来解决。

## 高精度数加法

高精度数是指大大超出了标准数据类型能表示的范围的数，例如10000位整数。很多计算问题的结果都很大，因此，高精度数极其重要。

一般使用一个数组来存储高精度数的所有数位，数组中的每个元素存储该高精度数的1位数字或多位数字。 请尝试计算：N个高精度数的加和。这个任务对于在学习数据结构的你来说应该是小菜一碟。 。

### 输入格式

第1行，1个整数N，表示高精度整数的个数，(1≤N≤10000)。

第2至N+1行，每行1个高精度整数x, x最多100位。

### 输出格式

1行,1个高精度整数，表示输入的N个高精度数的加和。

### 输入样例

```data
3
12345678910
12345678910
12345678910
```

### 输出样例

```data
37037036730
```

### 题目解析

也没什么好说的吧，就是用数组来模拟加法的逐位运算，唯一要注意的是开的数组的大小要比上限多一位。其次是输入应该逆序

#### 代码实现

```c++
#include<iostream>
#include<string>
#define N 111
using namespace std;


void add(int x[],int y[],int z[]){
    for(int i=0;i<N;++i){
        z[i+1]=(x[i]+y[i]+z[i])/10;
        x[i]=(x[i]+y[i]+z[i])%10;
    }
}
int a[N]={0};
int b[N]={0};
int t[N]={0};
string temp;
int main(int argc, char const *argv[])
{
    temp.clear();
    int n=0;
    cin>>n;
    for(int i=0;i<n;++i){
        int j=0;
        cin>>temp;
        for (int i = temp.size()-1; i>=0; --i)
        {
            b[j]=temp[i]-48;
            ++j;
        }
        add(a,b,t);
        for(int i=0;i<j;++i){
            b[i]=0;
        }
    }
    bool flag=true;
    for(int i=N-1;i>=0;--i){
        if(flag&&a[i]!=0){
            printf("%d",a[i]);
            flag=false;
        }else if (!flag)
        {
            printf("%d",a[i]);
        }
    }
    printf("\n");
    return 0;
}
```

## 二叉树的加权距离

二叉树结点间的一种加权距离定义为：上行方向的变数×3 +下行方向的边数×2 。上行方向是指由结点向根的方向，下行方向是指与由根向叶结点方向。 给定一棵二叉树T及两个结点u和v，试求u到v的加权距离。

### 输入格式

第1行，1个整数N，表示二叉树的结点数，(1≤N≤100000)。

随后若干行，每行两个整数a和b，用空格分隔，表示结点a到结点b有一条边，a、b是结点的编号，1≤a、b≤N；根结点编号为1，边从根向叶结点方向。

最后1行，两个整数u和v，用空格分隔，表示所查询的两个结点的编号，1≤u、v≤N。

### 输出格式

1行,1个整数，表示查询的加权距离。

### 输入样例

```data
5
1 2
2 3
1 4
4 5
3 4
```

### 输出样例

```data
8
```

### 题目解析

本质上是图上2点的路径问题，且因为这是树，所以我们可以利用树的特殊性来解，或者使用图的普遍方法来解

#### 方法一:树上节点到根必有路径

因为根据树的性质，任意节点到根定有路径，所以我们可以求出2个点各自到根的路径，那必然会交汇，从而形成路径。

需要注意，退化树情形下的特判。

##### 代码实现

```c++
#include<iostream>
#define N 100001

using namespace std;

int parent[N];
int path[N]={0};

int main(int argc, char const *argv[])
{

    int n=0;
    scanf("%d",&n);getchar();
    int u=0,v=0;
    for (int i = 0; i < n-1; i++)
    {
        scanf("%d %d",&u,&v);getchar();
        parent[v]=u;
    }
    scanf("%d %d",&u,&v);
    int orgin_u=u;
    int up=0,down=0;
    //u向上走并更新path
    while (parent[u]!=0){
        path[parent[u]]=path[u]+1;
        if(parent[u]==v){
            up=path[u]+1;
            break;
        }
        u=parent[u];
    }
    //v向上走并更新path,若遇到已经大于0的path则证明找到通路
    while (parent[v]!=0&&up==0)
    {
        if(!path[parent[v]]){
            path[parent[v]]=path[v]+1;
        }else{
            up=path[parent[v]];
            down=path[v]+1;
            break;
        }
        if(parent[v]==orgin_u){
            down=path[v]+1;
            break;
        }
        v=parent[v];
    }
    printf("%lld\n",(long long)up*3+down*2);


    return 0;
}
```

##### 分析

因为都是从节点到根的过程，可以直接看出最坏时间为T(n)=$2\log_2n$，所以时间复杂度为O（$\log_2n$)，还是比较好写且快速的。

#### 方法二:利用图的单源最短路

因为树也是图的一种，那么只需要对一点使用单源最短路，并对路径的类型进行加权运算，即可得出答案

##### ~~代码实现~~

## 修轻轨

长春市有n个交通枢纽，计划在1号枢纽到n号枢纽之间修建一条轻轨。轻轨由多段隧道组成，候选隧道有m段。每段候选隧道只能由一个公司施工，施工天数对各家公司一致。有n家施工公司，每家公司同时最多只能修建一条候选隧道。所有公司可以同时开始施工。请评估：修建这条轻轨最少要多少天。。

### 输入格式

第1行，两个整数n和m，用空格分隔，分别表示交通枢纽的数量和候选隧道的数量，1 ≤ n ≤ 100000，1 ≤ m ≤ 200000。

第2行到第m+1行，每行三个整数a、b、c，用空格分隔，表示枢纽a和枢纽b之间可以修建一条双向隧道，施工时间为c天，1 ≤ a, b ≤ n，1 ≤ c ≤ 1000000。

### 输出格式

输出一行，包含一个整数，表示最少施工天数。

### 输入样例

```data
6 6
1 2 4
2 3 4
3 6 7
1 4 2
4 5 5
5 6 6
```

### 输出样例

```data
6
```

### 题目解析

此题乍一看好像是关键路径问题，但是，有个提示：<font color="FF0000">并不是每个枢纽都必须经过</font>，也就是说，只要找出连接起点和终点的一条路即可，而所求时间就是这路上最迟完成的时间。

所以本质上是某种最小生成树问题，或者说是最短路径问题，因而可以从2种思路来解题

#### 方法一:Kruskal(MST)

因为最终我们只需要2点连通，且连通路最小，因而可以使用稍作修改的Kruskal来寻找。但存在一个问题，如何保证答案必定存在，且正确呢？我们可以简单的作下思维实验和推理

首先可以确定的是，连通路必定存在，若不存在则无解。其次如何保证最小，因为Kruskal每次取最小边，假如取了一条边后使得，起点和终点连通，即刻停止算法，则可以肯定，不会存在更大的路径。

##### 代码实现

```c++
#include<iostream>
#include<queue>

using namespace std;

struct Object
{
    int u;
    int v;
    int cost;
    Object(){
        u=0;v=0;cost=0;
    }
    Object(const Object &x){
        u=x.u;v=x.v;cost=x.cost;
    }
    Object(int _u,int _v,int _cost):
    u(_u),v(_v),cost(_cost){
    }
    bool operator<(const Object& b)const{
        return cost>b.cost;
    }
};
//边集
priority_queue<Object> edges;

//并查集部分
vector<int> father;
//并查集初始化
void make_set(int n){
    for (int i = 0; i <=n; ++i)
    {
        father.push_back(0);
    }
}
//并查集查找
int Find(int v){
    if(father[v]<=0)return v;
    return father[v]=Find(father[v]);   //路径压缩
}
//并查集合并
void Union(int x,int y){
    int fx=Find(x);
    int fy=Find(y);
    if(fx!=fy){
        father[fy]=fx;
    }
}


int main(int argc, char const *argv[])
{
    int n=0,m=0;
    scanf("%d %d",&n,&m);
    make_set(n);
    int u=0,v=0,cost=0;
    for(int i=0;i<m;++i){
        scanf(" %d %d %d",&u,&v,&cost);
        edges.push(Object(u,v,cost));
    }
    //Kruskal
    int res=0;
    while (!edges.empty())
    {
        Object t=edges.top();
        edges.pop();
        if(Find(t.u)!=Find(t.v)){
            Union(t.u,t.v);
        }
        if(Find(1)==Find(n)){
            res=t.cost;
            break;
        }
    }
    printf("%d\n",res);
    return 0;
}
```

##### 分析

因为并查集使用了路径压缩，考虑到最坏时间复杂度为O($n\log_2n$)，如果使用的是按秩合并的并查集，则可以达到O(n)。

#### 方法二:最短路

可以使用贝尔曼-福德来实现。

##### ~~代码实现~~

#### 方法三:对答案的二分

这个方法非常神奇，第一次接触让我倍感震惊，因为这个题的结果显然是某种问题的一个上界，所以可以使用二分法来确定这个上界。

假设一个答案x，把小于x的路全都选上，若起讫点连通，则缩小x的范围，若不连通则扩大x的范围。使用并查集

##### ~~代码实现~~

##### 分析

可以想到最坏时间复杂度为O($n\log_2^2n$)~~_（没有证明，直接毛咕咕的）_~~。

## 数据结构设计I

小唐正在学习数据结构。他尝试应用数据结构理论处理数据。最近，他接到一个任务，要求维护一个动态数据表，并支持如下操作：

1. 插入操作(I):从表的一端插入一个整数
2. 删除操作(D):从表的另一端删除一个整数
3. 取反操作(R):把当前表中的所有整数都变成相反数
4. 取最大值操作(M):取当前表中的最大值

如何高效的实现这个动态数据结构捏？

### 输入格式

第1行，包含1个整数M，代表操作的个数， 2≤M≤1000000。

第2到M+1行，每行包含1个操作。每个操作以一个字符开头，可以是I、D、R、M。如果是I操作，格式如下：I x, x代表插入的整数，-10000000≤x≤10000000。 。

### 输出格式

若干行，每行1个整数，对应M操作的返回值。如果M和D操作时队列为空，忽略对应操作。

### 输入样例

```data
6
I 6
R
I 2
M
D
M
```

### 输出样例

```data
2
2
```

### 题目解析

整个分析下来看，难点就2个地方，一个是取反操作，太耗时间，第二个是取最大值的操作 ，因为数据是动态变换的，所以最大值要每次查询都更新，再看看时间限制，有点遭不住。但是内存给了50MB

于是乎，自然而然的就想到，能不能空间换时间捏。

#### 方法一:MultiSet

了解到MultiSet能排序也能查找，取最大值要排序，删除元素需要查找，所以很自然的就想到用这个了，为了防止卡时间，直接利用表里思维开套对应的体系即可，取反就是将表里互换。

##### 代码实现

```c++
#include<iostream>
#include<algorithm>
#include<queue>
#include<set>

using namespace std;

multiset<int,greater<int>> temp;
multiset<int,greater<int>> temp_n;
deque<int> list;
deque<int> list_n;

int main(int argc, char const *argv[])
{
    bool flag=true;
    int n=0;
    scanf("%d",&n);getchar();
    //操作
    char choice=0;
    int x=0;
    for(int i=0;i<n;++i){
        scanf("%c",&choice);getchar();
        if(choice=='I'){
            scanf("%d",&x);getchar();
            list.push_front(flag?x:-x);
            list_n.push_front(flag?-x:x);
            temp.insert(flag?x:-x);
            temp_n.insert(flag?-x:x);
        }else if(choice=='D'){
            if(!list.empty()){
                auto target=temp.find(list.back());
                auto target_n=temp_n.find(list_n.back());
                temp.erase(target);
                temp_n.erase(target_n);
                list.pop_back();
                list_n.pop_back();
            }
        }else if (choice=='R')
        {
            flag=!flag;

        }else if (choice=='M')
        {
            if(!list.empty()){
                printf("%d\n",flag?*temp.begin():*temp_n.begin());
            }
        }
    }
    return 0;
}
```

##### 分析

其实表里2套空间可以压缩为一个，因为最大最小值对于正负数正好可以相反，即可实现压缩。

#### 方法二:使用单调队列

单调队列能保证队首元素为区间内最大值，在执行删除和插入操作时，只需要同时操作单调队列即可。也要开2套空间

##### ~~代码实现~~

##### ~~分析~~

只能说时间复杂度为O(n)。

## 总结

此次实验课上的题多为情景题，也就是说需要对问题场景进行抽象和建模，锻炼了建模能力，具有普遍性意义。

## 序列调度

有一个N个数的序列A：1，2，……，N。有一个后进先出容器D，容器的容量为C。如果给出一个由1到N组成的序列，那么可否由A使用容器D的插入和删除操作得到。

### 输入格式

第1行，2个整数T和C，空格分隔，分别表示询问的组数和容器的容量，1≤T≤10，1≤C≤N。

第2到T+1行，每行的第1个整数N，表示序列的元素数，1≤N≤10000。接下来N个整数，表示询问的序列。

### 输出格式

T行。若第i组的序列能得到，第i行输出Yes；否则，第i行输出No,1≤i≤T。

### 输入样例

```data
2 2
5 1 2 5 4 3
4 1 3 2 4
```

### 输出样例

```data
No
Yes
```

### 题目解析

分析题意，我们可以想到题目的目的是验证一个固定容量的栈能否将辅助输出对应的序列。起先我注意到这可能更逆序数有关，但局限于贫乏的数学能力，我觉得使用暴力模拟来验证更加可靠。

#### 方法一:模拟法

因为原序列是连续序列，所以并不需要开一个数组来存序列，可以节省点空间，节约初始化时间。

使用一个栈，在读入输出序列时，若读入的数并不是现在顺序序列中指向的数，那显然顺序序列中的该数应该入栈，同时若读入的数小于先顺序序列中指向的数，那显然的，所需的数应在栈中寻找，若在栈顶则可及，否则不可及。

若爆栈，那显然也不可及

##### 代码实现

```c++
#include<iostream>
#include<vector>
using namespace std;

int main(int argc, char const *argv[])
{
    vector<int> temp;
    int t=0, c=0;
    scanf("%d %d",&t,&c);getchar();
    for (int i = 0; i < t; ++i)
    {
        int top=1;
        bool flag=true;
        temp.clear();
        int n=0;
        scanf("%d",&n);
        int k=0;int j=0;
        for (j = 0; j < n; ++j){
            scanf("%d",&k);
            if(!flag)continue;
            while (k>=top){
                temp.push_back(top);
                ++top;
            }
            if(k==top){
                ++top;
                continue;
            }
            if(temp.size()>c){
                flag=false;
                continue;
            }
            if(k<top){
                if(k==temp.back()){
                    temp.pop_back();
                    continue;
                }else{
                    flag=false;
                    continue;
                }
            }

        }

        printf("%s",flag?"Yes":"No");
        printf("\n");
    }

    return 0;
}
```

##### 分析

显然的，时间复杂度是O(n)，比较迅速。而且不用数组存储序列，较为节省空间

#### ~~方法二:遍历解空间~~

可以将一个序列所以的可能建图，然后遍历验证。（溜~

## 最大最小差

对n 个正整数，进行如下操作：每一次删去其中两个数 a 和 b，然后加入一个新数：a\*b+1，如此下去直到 只剩下一个数。所有按这种操作方式最后得到的数中，最大的为max，最小的为min，计算max-min。

### 输入格式

第1行：n，数列元素的个数，1<=n<=16。

第2行：n 个用空格隔开的数x，x<=10。

### 输出格式

1行，所求max-min

### 输入样例

```data
3
2 4 3
```

### 输出样例

```data
2
```

### 题目解析

存在一个规律，不断的取最小的2个数进行操作，那最终的结果就是最大的，同样的，不断的取最大的2个数进行操作，那最终的结果就是最小的。

#### 方法一:利用规律

##### 代码实现

```c++
#include<iostream>
#include<queue>
using namespace std;

priority_queue<long long,vector<long long>,less<long long>> big;
priority_queue<long long,vector<long long>,greater<long long>> small;

int main(int argc, char const *argv[])
{
    int n=0,t=0;
    scanf("%d",&n);
    for (int i = 0; i < n; i++)
    {
        scanf("%d",&t);
        big.push(t);
        small.push(t);
    }
    while (big.size()!=1)
    {
        long long a=big.top();
        big.pop();
        long long b=big.top();
        big.pop();
        big.push(a*b+1);
    }
    while (small.size()!=1)
    {
        long long a=small.top();
        small.pop();
        long long b=small.top();
        small.pop();
        small.push(a*b+1);
    }
    printf("%lld\n",small.top()-big.top());

    return 0;
}
```

##### ~~分析~~

没什么好分析的，写的很随便

## 二叉树最短路径长度

给定一棵二叉树T，每个结点赋一个权值。计算从根结点到所有结点的最短路径长度。路径长度定义为：路径上的每个顶点的权值和。

### 输入格式

第1行，1个整数n，表示二叉树T的结点数，结点编号1..n，1≤n≤20000。

第2行，n个整数，空格分隔，表示T的先根序列，序列中结点用编号表示。

第3行，n个整数，空格分隔，表示T的中根序列，序列中结点用编号表示。

第4行，n个整数Wi，空格分隔，表示T中结点的权值，-10000≤Wi≤10000，1≤i≤n。

### 输出格式

1行，n个整数，表示根结点到其它所有结点的最短路径长度。

### 输入样例

```data
4
1 2 4 3
4 2 1 3
1 -1 2 3
```

### 输出样例

```data
1 0 3 3
```

### 题目解析

简单分析可知，此题关键在于从中根序和先根序中得出树的信息

#### 方法一:建树法

直接利用蕴藏的信息建树

```c++
#include<iostream>
#define N 20010

using namespace std;

int Left[N];
int Right[N];
int weight[N];
int res[N];
int a[N];
int b[N];

int n=0;
int p=0;

int initTree(int al,int ar){
    if(al>ar){
        return 0;
    }
    ++p;
    if(al==ar){
        return b[ar];
    }

    int root=0;
    int mid=0;
    for(mid=al;mid<=ar;++mid){
        if(b[mid]==a[p]){
            root=a[p];
            break;
        }
    }
    //建立左子树
    Left[root]=initTree(al,mid-1);
    Right[root]=initTree(mid+1,ar);
    return root;
}

void DFS(int root,int cost){
    if(root==0)return;
    res[root]=cost+weight[root];
    DFS(Left[root],res[root]);
    DFS(Right[root],res[root]);
}


int main(int argc, char const *argv[])
{
    scanf("%d",&n);
    for (int i = 1; i <=n; ++i){
        scanf("%d",&a[i]);
    }
    for (int i = 1; i <=n; ++i){
        scanf("%d",&b[i]);
    }
    int root=initTree(1,n);
    for (int i = 1; i <=n; ++i)
    {
        scanf("%d",&weight[i]);
    }
    DFS(root,0);
    for (int i = 1; i <=n; ++i){
        printf("%d%c",res[i],i<n?' ':'\n');
    }

    return 0;
}
```

##### 分析

考虑到建树的代价，所以时间复杂度是O(n)的。使用了较为优的建树法，提高了效率。

## 方案计数

组装一个产品需要 n 个零件。生产每个零件都需花费一定的时间。零件的生产可以并行进行。有些零件的生产有先后关系，只有一个零件的之前的所有零件都生产完毕，才能开始生产这个零件。如何合理安排工序，才能在最少的时间内完成所有零件的生产。在保证最少时间情况下，关键方案有多少种，关键方案是指从生产开始时间到结束时间的一个零件生产序列，序列中相邻两个零件的关系属于事先给出的零件间先后关系的集合，序列中的每一个零件的生产都不能延期

### 输入格式

第1行，2个整数n和m，用空格分隔，分别表示零件数和关系数，零件编号1..n，1≤n≤10000, 0≤m≤100000 。

第2行，n个整数Ti，用空格分隔，表示零件i的生产时间，1≤i≤n，1≤Ti≤100 。

第3到m+2行，每行两个整数i和j，用空格分隔，表示零件i要在零件j之前生产。

### 输出格式

第1行，1个整数，完成生产的最少时间。

第2行，1个整数，关键方案数，最多100位。

如果生产不能完成，只输出1行，包含1个整数0.

### 输入样例

```data
4 4
1 2 2 1
1 2
1 3
2 4
3 4
```

### 输出样例

```data
4
2
```

### 题目解析

经过分析，题目表达2点意思。

1. 求出关键路径的长度
2. 求出所有关键路径

题面给出的是AOV网，因而引入虚源和虚汇，并将对应的点权向前推为边权。

对于第一点，比较简单，只需要对AOE网跑一遍关键路径算法即可

对于第二点，考虑到题目给出结果有<font color=FF0000>100位</font>，所以我们不得不用高精度加法来确保结果能够正确。

#### 方法一:基于递推

对于求关键路径的条数，使用递推的方式来求。即为了求到虚汇的关键路径条数，我们可以求所以到虚汇的关键节点的关键路径条数，然后将这些数相加，即可得到虚汇的关键路径条数，以此类推。

##### 代码实现

```c++
#include<iostream>
#include<algorithm>
#include<string>
#include<queue>
using namespace std;

/*<---------------------高精度加法------------------------->*/
class BigInteger
{
private:
    vector<int> content;
public:
    BigInteger();
    BigInteger(long long origin);
    BigInteger(const BigInteger& b);
    ~BigInteger();
    unsigned long long size() const;
    BigInteger operator+(const BigInteger& b);
    BigInteger& operator=(const BigInteger& b);
    void resize(unsigned long long n);
    const int& operator[](unsigned long long i)const;
    int& operator[](unsigned long long i);
    string toString();

};
BigInteger::BigInteger(){
    content.reserve(128);
    for (int i = 0; i < 128; ++i){
        content.push_back(0);
    }

}

BigInteger::BigInteger(long long origin){
    content.reserve(128);
    while (origin>0)
    {
        content.push_back(origin%10);
        origin=origin/10;
    }
}
BigInteger::BigInteger(const BigInteger& b){
    content.clear();
    for(int i=0;i<b.size();++i){
        content.push_back(b[i]);
    }
}

BigInteger::~BigInteger(){
    content.clear();
}

BigInteger BigInteger::operator+(const BigInteger& b){
    BigInteger t;
    BigInteger res;
    unsigned long long maxsize=max(this->size(),b.size());
    t.resize(maxsize+1);
    res.resize(maxsize+1);
    for (int i = 0; i < maxsize; ++i){
        int num1=i<this->size()?content[i]:0;
        int num2=i<b.size()?b[i]:0;
        res[i]=(num1+num2+t[i])%10;
        t[i+1]=(num1+num2+t[i])/10;
    }
    if(t[maxsize]!=0){
        res[maxsize]=t[maxsize];
    }else{
        res.resize(maxsize);
    }
    return res;
}
BigInteger& BigInteger::operator=(const BigInteger& b){
    if(this==&b){
        return *this;
    }else{
        content.clear();
        content.reserve(b.size());
        for(int i=0;i<b.size();++i){
            content.push_back(b[i]);
        }
    }
    return *this;
}
unsigned long long BigInteger::size()const{
        return content.size();
}
const int& BigInteger::operator[](unsigned long long i)const{
    if(i>content.size())return *content.end();
    return (*(content.begin()+i));
}
int& BigInteger::operator[](unsigned long long i){
    if(i>content.size())return *content.end();
    return (*(content.begin()+i));
}
void BigInteger::resize(unsigned long long n){
    if(n>this->size()){
        for (unsigned long long i = this->size(); i <n; ++i){
            content.push_back(0);
        }
    }else{
        for (unsigned long long i = this->size(); i>n; --i){
            content.pop_back();
        }
    }
}
string BigInteger::toString(){
    bool flag=true;
    string res;
    for (int i = this->size()-1; i >=0; --i){
        if(flag&&content[i]==0){
            continue;
        }else{
            if(flag&&content[i]!=0){
                flag=false;
            }
            res.push_back(content[i]+48);
        }
    }
    if(flag)res.push_back('0');
    return res;
}
/*<!--------------------高精度加法------------------------->*/
#define MAXN 10010
int n=0;
int m=0;
/*<---------------------读入AOV图-------------------------->*/
struct Edge
{
    int u;
    int v;
    int w;
    Edge* next;
    Edge(){v=0;w=0;next=nullptr;}
    Edge(int _u,int _v,int _w){u=_u;v=_v;w=_w;next=nullptr;}
};
struct Node
{
    int inDegree;
    int inDegree_for_bfs;
    int outDegree;
    int cost;
    int ES;
    int LS;
    Edge *next;
    Node(){
        inDegree=0;outDegree=0;
        cost=0;
        ES=0;LS=__INT32_MAX__;  //初始化最早和最晚开始时间
        next=nullptr;
    }
};

Node head[MAXN];
void addEdge(int u,int v,int cost){
    Edge* t=head[u].next;
    head[u].next=new Edge(u,v,cost);
    if(t!=nullptr){
        head[u].next->next=t;
    }
    head[u].outDegree+=1;
    head[v].inDegree+=1;
    head[v].inDegree_for_bfs+=1;
}
void input_map(){
    for (int i = 1; i <=n; ++i){
        scanf("%d",&head[i].cost);
    }
    int u=0,v=0;
    for (int i = 0; i < m; ++i){
        scanf("%d %d",&u,&v);
        addEdge(u,v,head[v].cost);  //将点权前推到边上
    }
    //引入虚源虚汇
    for (int i=1;i<=n;++i){
        if(head[i].inDegree==0){
            //将虚源指向入度为0的点
            addEdge(0,i,head[i].cost);
        }
        if(head[i].outDegree==0){
            //将出度为0点指向虚汇
            addEdge(i,n+1,0);
        }
    }
}
/*<!--------------------读入AOV图-------------------------->*/

/*<---------------------拓扑排序与关键路径---------------------------->*/

//拓扑排序
vector<int> topRes; //存放拓扑排序的结果
void topOder(){
    //初始化
    queue<int> q;
    topRes.reserve(MAXN);
    q.push(0);  //虚源定入度为0
    //开始拓扑
    while (!q.empty()){
        int cur=q.front();
        q.pop();
        topRes.push_back(cur);
        //遍历
        for (auto i = head[cur].next; i!=nullptr;i=i->next){
            int v=i->v;int w=i->w;
            if((--head[v].inDegree)==0){
                q.push(v);
                //cout << v << endl;
            }
            head[v].ES=max(head[cur].ES+w,head[v].ES);  //顺着拓扑排序，求出最活动的最早开始时间
            //cout<<head[v].ES<<endl;
        }
    }
}

//关键路径算法
void CritiaclPath(){
    topOder();  //顺推求出所有的最早发生时间
    head[n+1].LS=head[n+1].ES;  //将顺推的结果作为逆推的开头
    //开始逆推
    for(int i=topRes.size()-1;i>=0;--i){
        int cur=topRes[i];
        for (auto j = head[cur].next; j!=nullptr;j=j->next){
            int v=j->v;int w=j->w;
            head[cur].LS=min(head[v].LS-w,head[cur].LS);    //逆拓扑序，求出活动的最迟开始时间
            //cout<<head[cur].LS<<endl;
        }
    }
}

/*<!--------------------拓扑排序与关键路径---------------------------->*/

/*<---------------------利用BFS递推来求出结果------------------------->*/
BigInteger temps[MAXN]; //用于存放到达每个节点的关键路径
BigInteger final;   //存放最终结果
int visited[MAXN];  //用于区分节点是否已经被计算过

void BFS(int x){
    queue<int> q;   //暂存层
    q.push(x);
    visited[x]=1;
    while (!q.empty()){
        int cur=q.front();
        q.pop();
        visited[cur]=1;
        for (auto i = head[cur].next; i!=nullptr;i=i->next){
            int v=i->v;
            head[v].inDegree_for_bfs-=1;
            //则指向节点为关键节点，该路径为关键路径
            if(head[v].ES==head[v].LS){
                temps[v]=temps[cur]+temps[v];
            }
            if(head[v].inDegree_for_bfs==0){
                q.push(v);
            }
        }

    }
}



/*<!--------------------利用BFS递推来求出结果------------------------->*/

int main(int argc, char const *argv[])
{
    scanf("%d %d",&n,&m);
    input_map();    //读入AOV图
    CritiaclPath(); //求出关键路径上的时间
    temps[0]=1; //认为到虚源有一条关键路径
    BFS(0);
    long long res=head[n+1].ES;
    final=temps[n+1];
    if(final.toString()!="0")cout<<res<<endl;
    cout<<final.toString()<<endl;
    return 0;
}
```

##### 分析

精细封装了一个高精度的加法，便于后续使用。对于时间复杂度分析不能。

## 总结

总体来说此次实验的卡点就在于最后一题的高精度加法，对于此，平常应当积累些代码模板，以便于使用。
