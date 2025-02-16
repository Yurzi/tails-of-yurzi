---
title: "最大连续子序列的和"
date: "2021-05-09T13:46:08+08:00"
lastmod: "2024-03-27T20:24:08+08:00"
author: ["Yurzi", "Lily"]
lang: "zh-CN"
description: "对于最大连续子序列的和的一些求解思路"
keywords:
  - Algorithm
  - Subsequences
tags:
  - Algorithm
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

## 题目:最喜爱的序列

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
**代码实现**

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

**分析:**
使用暴力法的时间复杂度显然是O(n*m)的，这实在太慢了:sweat_smile:，~~*虽然还有更慢的\*~~ 很容易被时间限制卡住。

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

&#160;**代码实现**

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

**分析**
因为每个前缀和序列中的元素只被访问了一次，时间复杂度是O(n),可以看到相比暴力穷举法，时间效率大大的提高了。如果使用数组自己维护双端队列 则空间还可以节省三分之一 ~~_我是five懒得写了_~~

---

<div align="center">
<font style="font-weight:bold" size='4'>下列方法只适用于不限制子序列长度</font>
</div>

#### 方法三:分治法

总的来说就是分三种情况来分治

1. 找到左半部分的最大子序列的和
2. 找到右半部分的最大子序列的和
3. 找到中间跨边界的最大子序列的和

   1. 向左一步，计算和，若大于上一步的和则更新
   2. 向右一步，计算和，若大于上一步的和则更新
   3. 将左侧的和与右侧的和相加得到中间的和

&#160;**代码实现**
~~_真的写不出能分治出定长区间和区间端点的_~~:cry:

```c++
#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

int n = 0;
int m = 0;        //用来存放输入的n和m
vector<int> list; //存放输入的喜爱值

int toSolve(int left, int right)
{
    if (left == right)
    {
        return list[left];
    }
    int middle = (left + right) >> 1;
    int sum_left = toSolve(left, middle);
    int sum_right = toSolve(middle + 1, right);
    int sumL = 0, sumR = 0, tL = 0, tR = 0;
    for (int i = middle; i >= left; --i)
    {
        tL += list[i];
        sumL = max(sumL, tL);
    }
    for (int i = middle + 1; i < right; ++i)
    {
        tR += list[i];
        sumR = max(sumR, tR);
    }
    int sum = sumL + sumR;

    return max(max(sum_left, sum_right), sum);
}

int main(int argc, char const *argv[])
{
    //读入数据
    scanf("%d %d", &n, &m);
    getchar();     //去除回车 以防万一
    int itemp = 0; //暂存读入的数据，用来加入vector
    for (int i = 1; i <= n; ++i)
    {
        scanf("%d", &itemp);
        getchar();
        list.push_back(itemp);
    }
    int Max = toSolve(0, n - 1);

    printf("%d", Max);
    return 0;
}
```

**算法分析**
最坏时间复杂度为O($n^2$)阶的，因为最终每个递归树叶子节点都遍历了全部链表~~并没有比优化后的暴力好~~
最优时间复杂度为O(n),每个叶子节点都只遍历了一遍
期望时间复杂度应该是O($n\log n$)

#### 方法四:动态规划

用动态规划的思路去思考问题，每一步决策无非就是，是否将下一个数加入到当前的序列中
因为我们只求和，所以只需要用一个变量来存放当前序列的和
为什么可以这样做？
因为和最大的连续子序列拥有最优子结构的特性
例如在[-1,4,5,-10,3]中
[4,5]是和最大的连续子序列
而[4]也是在[-1,4]中和最大的连续子序列。
**代码实现**

```c++
#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

int n = 0;
int m = 0;        //用来存放输入的n和m
vector<int> list; //存放输入的喜爱值
int main(int argc, char const *argv[])
{
    //读入数据
    scanf("%d %d", &n, &m);
    getchar();     //去除回车 以防万一
    int itemp = 0; //暂存读入的数据，用来加入vector
    for (int i = 1; i <= n; ++i)
    {
        scanf("%d", &itemp);
        getchar();
        list.push_back(itemp);
    }
    int Max=0;
    int Max_t=0;
    Max_t=list[0];
    for(int i=1;i<n;++i){
        if(Max_t){
            Max_t=Max_t+list[i];
        }else{
            Max_t=list[i];  //这里假设了有从i开始的和最大的子序列
        }
        Max=max(Max,Max_t);//可以修改此段以输出最大子序列的和的区间端点
    }
    printf("%d", Max);
    return 0;
}
```

&#160;**算法分析**
很显然，整个算法只扫描了一遍序列，算法的时间复杂度是O(n)的，与单调队列一样。这个算法还有个名字叫[kadane算法](https://baike.baidu.com/item/%E6%9C%80%E5%A4%A7%E5%AD%90%E6%95%B0%E5%88%97%E9%97%AE%E9%A2%98/22828059#1)。用动态规划还是非常不错的，代码短速度快空间也省。~~_就是不能很好的契合这道题_~~:sweat_smile:

## 总结

总得来说求最大连续子序列和的问题有这样四种思路，各有优缺点，其中暴力法容易理解；单调队列适用场景广；分治法虽然在这里可行，但显然难以发挥其优势；而动态规划可以说没有缺点 ~~(我是five，不知道能不能改成定长区间的)~~。所以在合适的场景选择合适的算法才是\*ao\*的。极力推荐，单调队列和动态规划。
