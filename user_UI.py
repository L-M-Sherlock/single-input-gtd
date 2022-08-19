import PySimpleGUI as sg
import numpy as np
import pandas as pd
import function.calendarUItest as cl
import function.clockUI as clock
import time
from datetime import date,datetime,timedelta
from classes.Finished import Finished
from classes.Task import Task
from pathlib import Path
import time

QT_ENTER_KEY1 = 'special 16777220'
QT_ENTER_KEY2 = 'special 16777221'

def find(column_name,content,df):
    index_with_content = df[df[column_name] == content].index.tolist()
    return index_with_content


def add_record(Record: Finished,file="record_sample.csv"):
    file_name = Path("./time_record", date.today().isoformat()).with_suffix(
        ".csv"
    )
    if not file_name.exists():
        column_names = pd.read_csv(file)
        column_names.to_csv(file_name,index=False)
    column_names = pd.read_csv(file_name)
    record = list(Record.format())
    print(record)
    new_record = dict(zip(column_names, record))
    column_names = pd.concat([column_names, pd.Series(new_record).to_frame().T], ignore_index=True)
    column_names.to_csv(file_name, index=False)

def set_default(key,values,datetuple,content): # 设置日期的时候的一些默认选项
    if key==[]:
        key=[""]
    values['id'] = time.time()
    content.update(values)
    values=content
    if datetuple == None:

        if values['hour'].isdigit():
            todays=date.today()
            datetuple=[todays.year,todays.month,todays.day]
            if 0<=int(values['hour'])<=24:
                if values['minute'].isdigit():
                    if 0<=int(values['minute'])<=60:
                        values['start_time']=time.mktime((*datetuple, int(values['hour']), int(values['minute']), 0, 0,0,0))
                    else:
                        sg.Popup('输入错误')
                        raise TypeError
                elif values['minute']=='':
                    values['minute']=0
                    values['start_time'] = time.mktime(
                        (*datetuple, int(values['hour']), int(values['minute']), 0, 0, 0, 0))
                else:
                    sg.Popup('输入错误')
                    raise TypeError
        elif values['hour']=='':
            values['start_time']=np.nan
        else:
            sg.Popup('输入错误')
            raise TypeError
    else:
        if values['hour']=='':
            values['hour']=0
            values['minute']=0
            values['start_time'] = time.mktime((*datetuple, int(values['hour']), int(values['minute']), 0, 0, 0, 0))
        elif values['hour'].isdigit():
            if 0<=int(values['hour'])<=24:
                if values['minute'].isdigit():
                    if 0<=int(values['minute'])<=60:
                        values['start_time']=time.mktime((*datetuple, int(values['hour']), int(values['minute']), 0, 0,0,0))
                    else:
                        sg.Popup('输入错误')
                        raise TypeError
                elif values['minute'] == '':
                    values['minute'] = 0
                    values['start_time'] = time.mktime(
                        (*datetuple, int(values['hour']), int(values['minute']), 0, 0, 0, 0))
                else:
                    sg.Popup('输入错误')
                    raise TypeError
        else:
            sg.Popup('输入错误')
            raise TypeError





    del values['hour'],values['minute']
    return values
def revise_content(key,df,file,content):
    if not np.isnan(content['start_time']):
        struct_times = time.localtime(content['start_time'])
        print(struct_times)
        datetuple = [struct_times.tm_year, struct_times.tm_mon, struct_times.tm_mday]
        content['hour'] = struct_times.tm_hour
        content['minute'] = struct_times.tm_min
    else:
        datetuple = None
    values=content_interface(key, content, datetuple)
    #print(find('id',key[0],df)[0])
    print(values)
    df.loc[find('id',key[0],df)[0]]=values

    df.to_csv(file, index=False)


def add_content(key,df,file):  #
    # if content==None:
    content={'name':'','num':'','hour':'','minute':'','repetition_gap':1,'task_value':''}
    datetuple = None
    havecontent=False
    # else:
    #     havecontent=True
    #     if not np.isnan(content['start_time']):
    #         struct_times=time.localtime(content['start_time'])
    #         print(struct_times)
    #         datetuple=[struct_times.tm_year,struct_times.tm_mon,struct_times.tm_mday]
    #         content['hour']=struct_times.tm_hour
    #         content['minute'] = struct_times.tm_min
    #     else:
    #         datetuple=None
    values=content_interface(key,content,datetuple)
    values['father']=key
    df = pd.concat([df, pd.Series(values).to_frame().T], ignore_index=True)
    df.to_csv(file, index=False)


def content_interface(key,content,datetuple):
    layout = [[sg.Text('名字')], [sg.Input(content['name'],key='name')],
              [sg.Text('重复次数')], [sg.Input(content['num'],key='num')],
              [sg.Text('截止时间')],
              [sg.Button('年月日', key='date')],
              [sg.Text(datetuple, key='date_tuple')],
              [sg.Text('时')], [sg.Input(content['hour'],key='hour')],
              [sg.Text('分')], [sg.Input(content['minute'],key='minute')],
              [sg.Text('间隔天数')], [sg.Input(content['repetition_gap'],key='repetition_gap')],
              [sg.Text('个人感官价值')], [sg.Input(content['task_value'],key='task_value')],

              [sg.Button('cancel'), sg.Button('ok')]]
    windowadd = sg.Window('add', layout,return_keyboard_events=True)

    while True:  # Event Loop
        event, values = windowadd.read()
        if event in (sg.WIN_CLOSED, 'cancel','Escape:27'):
            windowadd.close()
            return values
        if event in  ('ok','\r', QT_ENTER_KEY1, QT_ENTER_KEY2):
            break
        if event == 'date':
            datetuple = cl.popup_get_date()
            windowadd['date_tuple'].update(str(datetuple))
    windowadd.close()
    values['id']=key
    values = set_default(key, values, datetuple,content)
    return values

def cauculate_ddl(start_time):
    now=datetime.now()
    #print((now-start_time)//(24*60*60))

    if np.isnan(start_time):
        return ''

    else:
        delta1 =  datetime.fromtimestamp(int(start_time))-now
        if delta1<timedelta(0):
            return '已经超时'
        else:
        #print(type(datetime.fromtimestamp(int(start_time))))

        #if now-start_time>float(time.mktime(datetime(1970,1,1,0,0,0,0).timetuple())):
            print(delta1)
            if delta1.days>=1:
                return str(delta1.days)+'天'
            else:
                return str(delta1.min) + '分'+str(delta1.seconds)+'秒'


def option(df):
    return df.sort_values(by='start_time',inplace=False)


def readcsv(file): #读文件 ，并生成树状结构
    todoTree = sg.TreeData()
    df = pd.read_csv(file)
    df=option(df)
    df1=df[pd.isna(df['father'])]
    df2=df[np.logical_not(pd.isna(df['father']))]
    for i in df1.index:
        key = df.at[i, "id"]
        text = df.at[i, "name"]
        ddl=cauculate_ddl(df.at[i,'start_time'])
        todoTree.insert('',key,text,[ddl])
    for i in df2.index:
        parent = df.at[i, "father"]
        key = df.at[i, "id"]
        text = df.at[i, "name"]
        ddl = cauculate_ddl(df.at[i, 'start_time'])
        #todoTree.tree_dict[todoTree.tree_dict[key].parent].children.remove(todoTree.tree_dict[key])
        # todoTree.tree_dict[key].parent=parent
        # todoTree.tree_dict[parent].children.append(todoTree.tree_dict[key])
        todoTree.insert(parent, key, text, [ddl])



    layout = [
        [sg.Button('cancel')],
        [sg.Tree(data=todoTree, headings=['截止日期', ],
                 auto_size_columns=True,
                 select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                 num_rows=20,
                 col0_width=40,
                 key='TREE',
                 show_expanded=True,
                 enable_events=True,
                 expand_x=True,
                 expand_y=True,right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_EXIT)],
        [sg.Input(key='IN')],
        [sg.Button('add'),sg.Button('clear')],
        [sg.Button('delete'),sg.Button('revise')],
        [sg.Button('start')]
    ]
    return df,todoTree,layout

def delete_in_tree(df,file,values,window): # 删除树状图里面的内容
    df = tododelete(df, file, values['TREE'])
    df.to_csv(file, index=False)
    df, todoTree, layout = readcsv(file)
    window['TREE'].update(todoTree)
    return df,file,window

def tododelete(df,file,key):  # 删除数据里面的内容
    df=df[df.id!=key[0]]

    if not df[df.father==key[0]].empty:
        for i in df[df.father==key[0]].id:
            df=tododelete(df, file, [i])
    df=df[df.father!=key[0]]
    return df

def finished_delete(todo,file,window,values): # 任务结束后删除内容
    # try:
    exist_todo = todo
    df=exist_todo
    content=values['TREE'][0]
    content_isin = exist_todo["id"].isin([content])  # 返回是否含有content的表
    #print(content)

    if content_isin.any():  # 先判断一下有没有这一行，如果没有提早报错
        index_with_content=df[df.id==content].index.tolist()[0]
        num_of_sub=exist_todo.at[index_with_content,'repetition_gap']
        if num_of_sub == 0:  # 0就是无穷次
            remain_todo = exist_todo
        elif num_of_sub == 1:
            remain_todo = exist_todo[~content_isin]  # 也就是直接删了
        else:  # 数量减少一次
            remain_todo = exist_todo
            remain_todo.loc[
                remain_todo["id"] == content, ["num"]
            ] -= 1
        df=remain_todo
        df.to_csv(file, index=False)
        df, todoTree, layout = readcsv(file)
        window['TREE'].update(todoTree)
        return df, file,  window
    else:
        print("wrong")
        return False

def pause_task(current_task: Task, command: str): # 任务暂停
    if current_task.task_name == "":
        sg.Text('当前没有任务')
    else:
        current_task.end_time = datetime.now()

        if command == "!":
            current_task = end_task(current_task, "紧急事情")
            current_task.task_name = input("请输入当前的紧急事项")
            current_task = begin_task(current_task, current_task.task_name)
        elif command == "~":
            current_task = end_task(current_task, "休息")
        elif command == "p":
            current_task = end_task(current_task, "休息")
            current_task.task_name = ""
    return current_task

def finished_task(current_task: Task, command: str): # 任务结束
    if current_task.task_name == "":
        if command == "ok":
            sg.Popup('当前没有任务')
    else:
        current_task.end_time = datetime.now()
        current_task = end_task(current_task, "finished")
        current_task.task_name = ""
    return current_task


def begin_task(current_task: Task, task_name: str): # 任务开始
    current_task.task_name = task_name
    print(f"开始执行: {current_task.task_name}")
    current_task.start_time = datetime.now()
    return current_task


def end_task(current_tasks: Task, reason: str): # 任务结束记录
    current_tasks.end_time = datetime.now()
    layout=[[sg.Text("请输入你完成的内容")],[sg.Input()],[sg.Button('ok')]]
    window=sg.Window("请输入你完成的内容",layout,return_keyboard_events=True)
    while True:
        event,subname=window.read()
        subname=subname[0]
        if event in ('ok','\r', QT_ENTER_KEY1, QT_ENTER_KEY2):
            window.close()
            break
    record = Finished(
        name=current_tasks.task_name,
        subname=subname,
        actuall_start_time=current_tasks.start_time,
        actuall_end_time=current_tasks.end_time,
        actlength=0,
        actshift=0,
        reason=reason,
    )
    add_record(record,'./data/record_sample.csv')
    return current_tasks



def main():
    file='./data/todo.csv'
    df,todoTree,layout=readcsv(file)


    window = sg.Window('用户输入部分', layout,finalize=True,return_keyboard_events=True)
    current_task=Task()


    while True:     # Event Loop

        event, values = window.read()
        element=window.find_element_with_focus()
        print(event,values,element)

        if event in (sg.WIN_CLOSED, 'cancel','Escape:27'):
            break
        if event =='add':
            add_content(values['TREE'],df,file)
            df, todoTree, layout = readcsv(file)
            window['TREE'].update(todoTree)
        if event=='clear':
            window['TREE'].update(todoTree)
        if event=='delete':
            df,file,window=delete_in_tree(df,file,values,window)
        if event=='revise':
            content=dict(df.loc[find('id',values['TREE'][0],df)[0]])
            content['hour']=''
            content['minute']=''
            revise_content(values['TREE'], df, file,content)
            df, todoTree, layout = readcsv(file)
            window['TREE'].update(todoTree)
        if event in ('start',' '):
            if type(element)==type(window['TREE']):
                current_task = begin_task(current_task, df.at[find('id',values['TREE'][0],df)[0], 'name'])
                start_time,endtime,clockevent,paused=clock.main(current_task.task_name)
                if clockevent=='-Finished-':
                    current_task = finished_task(current_task, 'q')
                    df,file,window=finished_delete(df,file,window,values)
                if clockevent in (sg.WIN_CLOSED, 'Exit','-RUN-PAUSE-'):
                    if paused==True:
                        current_task = pause_task(current_task, 'p')

        # 下面是键盘映射

        if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2):
            if values['IN']!='':
                newcontent={'name':values['IN'],'id':time.time(),'repetition_gap':1}
                df = pd.concat([df, pd.Series(newcontent).to_frame().T], ignore_index=True)
                df.to_csv(file, index=False)
                df, todoTree, layout = readcsv(file)
                window['TREE'].update(todoTree)
                window['IN'].update('')
            if values['IN']=='':
                if values['TREE']:
                    content = dict(df.loc[find('id', values['TREE'][0], df)[0]])
                    content['hour'] = ''
                    content['minute'] = ''
                    revise_content(values['TREE'], df, file, content)
                    df, todoTree, layout = readcsv(file)
                    window['TREE'].update(todoTree)
        if event=='Edit Me':
            if values['TREE']:
                content = dict(df.loc[find('id', values['TREE'][0], df)[0]])
                content['hour'] = ''
                content['minute'] = ''
                revise_content(values['TREE'], df, file, content)
                df, todoTree, layout = readcsv(file)
                window['TREE'].update(todoTree)
        if event=='Delete:46':
            df, file, window = delete_in_tree(df, file, values, window)
        if event in ('Down:40'):
            if values['TREE']==[]:
                values['TREE']=df.at[0,'id']
                window['TREE'].update(todoTree)
        if event in ('+'):
            add_content(values['TREE'], df, file)
            df, todoTree, layout = readcsv(file)
            window['TREE'].update(todoTree)








    window.close()

if __name__=="__main__":
    main()