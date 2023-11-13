"""
Title: chat room client
Author: 張家菖
Date: 2022-11-19
ID: 108202016
Key: python, socket, tcp, GUI(tkinter), muliti-thread
"""
import socket
import threading
import tkinter


# 傳送訊息
def SendMessage():
    # 從打字版，取得消息
    clientMessage = txtYourMessage.get()
    # Echo 自己的訊息
    txtMessages.insert(tkinter.END, "\n" + "You: " + clientMessage)
    # 發送給 Server
    clientSocket.send(clientMessage.encode("utf-8"))


# 接收訊息
def RecvMessage():
    while True:
        # 從 Server 得到別人的消息
        serverMessage = clientSocket.recv(1024).decode("utf-8")
        print(serverMessage)
        # 插入消息版呈現
        txtMessages.insert(tkinter.END, "\n"+serverMessage)


# 離開聊天
def Exit():
    # 以傳送 EXIT 給 Server，即剔除該名Client
    # 並且廣播給其他 Clients 知道
    clientMessage = 'EXIT'
    txtMessages.insert(tkinter.END, "\n" + "You: " + clientMessage)
    clientSocket.send(clientMessage.encode("utf-8"))
    # Tk.window 關閉
    window.destroy()


# 月曆與星期
def Calender():
    # 分割取得 Date
    date = []
    clientMessage = txtYourMessage.get()
    date = clientMessage.split(' ')

    # 若日期沒打好，則 Error Date
    if(len(date) != 3):
        txtMessages.insert(tkinter.END, "\n" + "Error Date")
    else:
        # 取得 年月日
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        txtMessages.insert(tkinter.END, "\n")
        # 檢查日期
        if((year < 1) or (month > 12) or (month < 1) or (day > 31)):
            txtMessages.insert(tkinter.END, "\n" + "** Wrong Date **" + "\n")

        # 取得星期幾
        if(WhichDate(year, month, day) == 1):
            txtMessages.insert(tkinter.END, "\n" + "*Monday*")
        elif(WhichDate(year, month, day) == 2):
            txtMessages.insert(tkinter.END, "\n" + "*Tuesday*")
        elif(WhichDate(year, month, day) == 3):
            txtMessages.insert(tkinter.END, "\n" + "*Wednesday*")
        elif(WhichDate(year, month, day) == 4):
            txtMessages.insert(tkinter.END, "\n" + "*Thursday*")
        elif(WhichDate(year, month, day) == 5):
            txtMessages.insert(tkinter.END, "\n" + "*Friday*")
        elif(WhichDate(year, month, day) == 6):
            txtMessages.insert(tkinter.END, "\n" + "*Saturday*")
        elif(WhichDate(year, month, day) == 0):
            txtMessages.insert(tkinter.END, "\n" + "*Sunday*")
        # 月曆呈現
        DisplayC(year, month, day)


# 根據數學，來計算星期幾
def WhichDate(year, month, day):
    if(month == 1 or month == 2):
        month += 12
        year -= 1
    return int(((day + 2 * month + 3 * (month + 1) / 5 + year + year / 4 - year / 100 + year / 400) + 1) % 7)


# 月曆呈現
def DisplayC(year, month, day):
    txtMessages.insert(tkinter.END, "\n" + "   0   1   2   3   4   5   6")
    txtMessages.insert(tkinter.END, "\n" + "============================")
    week = WhichDate(year, month, day)
    row = int((day - 1) / 7)
    first = (day - 7 * row)
    block = 0
    # block 代表該月1號，位於星期幾
    if (first - (week + 1) >= 0):
        block = 7 - (first - (week + 1))
    else:
        block = 0 - (first - (week + 1))

    # 取得該月天數
    dayMax = 0
    if((month == 1) or (month == 3) or (month == 5) or (month == 7) or (month == 8) or (month == 10) or (month == 12)):
        dayMax = 31
    elif(month == 2):
        dayMax = 28
    else:
        dayMax = 30

    # 檢查2月閏年
    if (((year % 4) != 0) and (month == 2)):
        dayMax = 28
    elif (((year % 4) == 0) and ((year % 100) != 0) and (month == 2)):
        dayMax = 29
    elif (((year % 100) == 0) and ((year % 400) != 0) and (month == 2)):
        dayMax = 28
    elif (((year % 400) == 0) and (month == 2)):
        dayMax = 29
    txtMessages.insert(tkinter.END, "\n")

    # 月曆呈現格式
    flag = 0
    for i in range(int(1-block), int(dayMax+1), 1):
        flag += 1
        if ((i > 0) and (i < 10) and (i != day)):
            txtMessages.insert(tkinter.END, "   " + str(i))
        elif((i >= 10) and (i != day)):
            txtMessages.insert(tkinter.END, "  " + str(i))
        elif((i > 0) and (i < 10) and (i == day)):
            txtMessages.insert(tkinter.END, "  *" + str(i))
        elif((i >= 10) and (i == day)):
            txtMessages.insert(tkinter.END, " *" + str(i))
        else:
            txtMessages.insert(tkinter.END, "    ")
        if((flag % 7) == 0):
            txtMessages.insert(tkinter.END, "\n")
            continue
    txtMessages.insert(tkinter.END, "\n")
    txtMessages.insert(tkinter.END, "\n"+"============================")


HOST = input("IP: ")
PORT = int(input("PORT(1000~65535): "))
# Check Port range
while(PORT > 65535 or PORT < 1000):
    PORT = int(input("Choose another PORT(1000~65535): "))
# AF_INET: IPv4
# SOCK_STREAM: TCP
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
clientSocket.connect((HOST, PORT))

# GUI(tkinter)
window = tkinter.Tk()
window.title("Connected to: " + HOST + ":"+str(PORT))
# 設定視窗大小為 350x580，視窗（左上角）在螢幕上的座標位置為 (250, 150)
window.geometry("350x580+250+150")
# 消息版
txtMessages = tkinter.Text(window, width=35)
txtMessages.grid(row=0, column=0, padx=10, pady=5)
# 打字版
txtYourMessage = tkinter.Entry(window, width=35)
txtYourMessage.insert(0, "Hello!")
txtYourMessage.grid(row=1, column=0, padx=10, pady=5)

# 發送消息按鈕
btnSendMessage = tkinter.Button(
    window, text="Send", width=10, bg='yellow',
    # 設定滑鼠位於按鈕時的背景顏色
    activebackground='#BE77FF',
    # 設定滑鼠位於按鈕時的前景顏色
    activeforeground='#FFFFFF', command=SendMessage)
btnSendMessage.grid(row=2, column=0)
# 離開按鈕
btnExit = tkinter.Button(window, text='Exit', bg='red',
                         # 設定滑鼠位於按鈕時的背景顏色
                         activebackground='#BE77FF',
                         # 設定滑鼠位於按鈕時的前景顏色
                         activeforeground='#FFFFFF', command=Exit)
btnExit.grid(row=2, column=1)
# 取得月曆按鈕
btnCalender = tkinter.Button(
    window, text="Calendar", width=10, bg='green',
    # 設定滑鼠位於按鈕時的背景顏色
    activebackground='#BE77FF',
    # 設定滑鼠位於按鈕時的前景顏色
    activeforeground='#FFFFFF', command=Calender)
btnCalender.grid(row=3, column=0)

# 用 muliti-thread 取得消息
recvThread = threading.Thread(target=RecvMessage)
recvThread.daemon = True
recvThread.start()

window.mainloop()
