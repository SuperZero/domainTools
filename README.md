#### domainTools
a domain tools
最近在看域名相关的东西，感觉不如写个相关的小东西来加深理解。

2017-04-14 一个可运行的小demo，待完善功能。  
2017-04-16 修改了一下结构，尝试修改了一部分线程池问题，发现了一堆解决的问题。  
2017-04-17  
- 添加功能，修复bug, 尝试了修改nameservers，但是失败，放弃。
- 增添输出信息的分级和色彩，(windows cmd终端不起效，powershell可以)  

2017-04-23  
- 添加对线程池的终止（https://noswap.com/blog/python-multiprocessing-keyboardinterrupt）(http://stackoverflow.com/questions/1408356/keyboard-interrupts-with-pythons-multiprocessing-pool)
(http://stackoverflow.com/questions/11312525/catch-ctrlc-sigint-and-exit-multiprocesses-gracefully-in-python)
- 美化信息输出  
- 增加站长之家的域名whois 查询
#### 第三方库
- requests
- dnspython
- BeautifulSoup3（暂未使用）
- termcolor
- cymruwhois（暂未使用） 