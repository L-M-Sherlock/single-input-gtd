# single-input-gtd

目前来看windows版本是可用的，然后linux也是可以的，mac版本估计应该也可以
使用环境是python3.9

# 用前提醒

main.py是主程序  
plan.md的使用需要结合obsidain的看板功能，且to do那一行不能修改标题（以后应该会出plan.md的使用方法）  
ddl.csv是用于ddl的记录的 
另外每一天会生成一个当天日期的文件
add_ddl.py用于增加未来你的ddl
env.bat(windows使用)在你安装anaconda之后，就可以直接帮你配置好环境
run.bat(windows)在你运行完env.bat后可以直接使用，用来运行python程序，界面大一点，好看一些
在使用程序的时需要python的pandas库，直接安装anaconda或者自己pip都可以

# 目前有的功能是

main.py  
进入界面显示你今天的todo项目和即将到来的ddl  
输入due进行ddl事项的任务（输入due后输入ddl的序号进行序号对应项目的内容）  
输入todo项目的序号可以进行序号对应项目的内容  
输入ok表示完成该项目  
输入wait表示还未完成该项目，但可以进行下一件事情  
！（中英文都可以）表示有紧急事情要补充  
输入q表示结束本程序  
输入rest表示进行休息（可以补充休息的内容，如游戏，吃饭等）  
输入b代表撤回正在执行的任务
输入空格进行内容的刷新（当你在软件执行的过程中更改了plan.md)
另外在开始任务时请输入数字，来代表你预估该项目的时间
另外还可以输入clock进行倒计时（不过得在进行任务的时候）
add_ddl.py
根据提示输入你的ddl的相关内容 
在ddl名字输入时直接回车可以退出程序 
输入年份直接回车，代表ddl是今年的 
输入月份的时 
1.直接回车，代表ddl是这个月的 
2.支持输入月份的英语或简写(August或Aug)中文的输入之后更新 
接下来输入ddl的日期 
输入完成后可以进行下一项ddl的输入 
huatu.py
可以将你的时间使用可视化（但是比较简单，未来准备完善）

# 未来打算增加的功能

1. 进行项目时的comment（附带在项目上） 
2. 灵感的记录（memo式），把零碎的点子和未来要做但不紧急的事情记录下来 
3. code reconstruct 目前的代码的效率和可读性都太差，很多地方都可以code reuse，在后续版本中将进行相关的升级 
4. 增加优先级，并且根据优先级和ddl进行智能的排序
5. 不使用obsidian照样能阅览的看板模式 
6. 增加每日习惯的记录和打卡 
7. 根据你现有的数据进行分析，可视化，并且能够提出意见 
8. sm plan的导入
9. 所有内容的交互界面的优化
10. 通过软件可以查看你摸鱼的时间（自动化统计，估计之后先用manictime先导出）
11. 在讲项目移动到to do时可以知道这个项目的原本的父节点是什么
12.在不进行任何项目的时候进行正计时，更改项目的时候直接switch（就是不需要记录结束时间，而是记录状态）
