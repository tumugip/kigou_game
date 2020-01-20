import tkinter
import random

index = 0
timer = 0
score = 0
hisc = 1000
difficulty = 0
tsugi = 0
pw = 0

cursor_x = 0
cursor_y = 0
mouse_x = 0
mouse_y = 0
mouse_c = 0

def mouse_move(e):
    global mouse_x , mouse_y
    mouse_x = e.x
    mouse_y = e.y

def mouse_press(e):
    global mouse_c
    mouse_c=1

kigo=[]
check=[]
for i in range(10):
    kigo.append([0,0,0,0,0,0,0,0])
    check.append([0,0,0,0,0,0,0,0])

def draw_kigo():
    cvs.delete("KIGO")
    for y in range(10):
        for x in range(8):
            if kigo[y][x] > 0:
                cvs.create_image(x*72+60,y*72+60,image=img_kigo[kigo[y][x]],tag="KIGO")

def check_kigo():
    for y in range(10):
        for x in range(8):
            check[y][x] = kigo[y][x]
    
    for y in range(1,9):
        for x in range(8):
            if check[y][x] > 0:
                if check[y-1][x] == check[y][x] and check[y+1][x] == check[y][x]:
                    kigo[y-1][x] = 9
                    kigo[y][x] = 9
                    kigo[y+1][x] = 9
        
    for y in range(10):
        for x in range(1,7):
            if check[y][x] > 0:
                if check[y][x-1] == check[y][x] and check[y][x+1] == check[y][x]:
                    kigo[y][x-1] = 9
                    kigo[y][x] = 9
                    kigo[y][x+1] = 9


    for y in range(1,9):
        for x in range(1,7):
            if check[y][x] > 0:
                if check[y-1][x-1] == check[y][x] and check[y+1][x+1] == check[y][x]:
                    kigo[y-1][x-1] = 9
                    kigo[y][x] = 9
                    kigo[y+1][x+1] = 9

                if check[y+1][x-1] == check[y][x] and check[y-1][x+1] == check[y][x]:
                    kigo[y+1][x-1] = 9
                    kigo[y][x] = 9
                    kigo[y-1][x+1] = 9

def sweep_kigo():
    num = 0
    for y in range(10):
        for x in range(8):
            if kigo[y][x] == 9:
                kigo[y][x] = 0
                num = num+1

    return num


def drop_kigo():
    flg = False
    for y in range(8,-1,-1):
        for x in range(8):
            if kigo[y][x] != 0 and kigo[y+1][x] == 0:
                kigo[y+1][x] = kigo[y][x]
                kigo[y][x]= 0
                flg = True
    
    return flg

def over_kigo():
    for x in range(8):
        if kigo[0][x] > 0:
            return True

    return False

def set_kigo():
    for x in range(8):
        kigo[0][x] = random.randint(0,difficulty)


def draw_txt(txt,x,y,siz,col,tg):
    fnt = ("Times New Roman",siz,"bold")
    cvs.create_text(x+2,y+2,text=txt,fill="black",font=fnt,tag=tg)
    cvs.create_text(x,y,text=txt,fill=col,font=fnt,tag=tg)


def game_main():
    global index,timer,score,hisc,difficulty,tsugi
    global cursor_x,cursor_y,mouse_c

    def click_btn():
        global difficulty,index
        pw = entry.get()
        pw=int(pw)

        if pw == 3:
            
            difficulty=8
            cvs.delete("PASS")
            entry.destroy()
            pwb.destroy()
            index =2
        else :
            index = 0

        return index


    if index == 0:
        draw_txt("記号パズル",340,240,100,"violet","TITLE")

        cvs.create_rectangle(168,384,456,456,fill="skyblue",width=0,tag="TITLE")
        draw_txt("Easy",312,420,40,"white","TITLE")

        cvs.create_rectangle(168,528,456,600,fill="lightgreen",width=0,tag="TITLE")
        draw_txt("Normal",312,564,40,"white","TITLE")

        cvs.create_rectangle(168,672,456,744,fill="orange",width=0,tag="TITLE")
        draw_txt("Hard",312,708,40,"white","TITLE")

        index= 1
        mouse_c=0


    elif index ==1:
        difficulty=0
        if mouse_c==1:
            if 168< mouse_x and mouse_x < 456 and 384<mouse_y and mouse_y < 456:
                difficulty = 4
                
            if 168< mouse_x and mouse_x < 456 and 528<mouse_y and mouse_y < 600:
                difficulty = 5

            if 168< mouse_x and mouse_x < 456 and 672<mouse_y and mouse_y < 744:
                difficulty = 6

            if 636< mouse_x and mouse_x < 901 and 8<mouse_y and mouse_y < 287:
                index = 7

            
        if difficulty>0:
            for y in range(10):
                for x in range(8):
                    kigo[y][x] = 0
            mouse_c = 0
            score = 0
            tsugi=0
            cursor_x = 0
            cursor_y = 0
            set_kigo()
            draw_kigo()
            cvs.delete("TITLE")
            if difficulty == 8:
                index=7
            index=2


    elif index==2:
        if drop_kigo() ==False:
            index=3
        draw_kigo()


    elif index==3:
        check_kigo()
        draw_kigo()
        index=4


    elif index==4:
        sc= sweep_kigo()
        score = score+ sc*difficulty*4
        if score > hisc:
            hisc = score
        if sc> 0:
            index = 2
        else:
            if over_kigo() ==False:
                tsugi = random.randint(1,difficulty)
                index= 5
            else:
                index=6
                timer=0
        draw_kigo()
    

    elif index == 5:
        if 24 <= mouse_x and mouse_x <24+72*8 and 24<=mouse_y and mouse_y<24+72*10:
            cursor_x = int((mouse_x-24)/72)
            cursor_y= int((mouse_y-24)/72)
            if mouse_c == 1:
                mouse_c= 0
                set_kigo()
                kigo[cursor_y][cursor_x]=tsugi
                tsugi=0
                index=2
        cvs.delete("CURSOR")
        cvs.create_image(cursor_x*72+60,cursor_y*72+60,image=cursor,tag="CURSOR")
        draw_kigo()


    elif index == 6:
        timer= timer+1
        if timer==1:
            draw_txt("GAME OVER",312,348,60,"red","OVER")
            if timer ==15:
                cvs.delete("OVER")
                index=0


    elif index == 7:
        cvs.delete("TITLE")
        draw_txt("Password",312,348,60,"yellow","PASS")
        draw_txt("1+2=",312,450,60,"Black","PASS")
        entry = tkinter.Entry(font=("Times Nes Roman",32),width=32,)
        entry.place(x=220,y=400,width=200,height=120)
        entry.pack()
        pwb = tkinter.Button(text="check",font=("Times Nes Roman",32),command=click_btn)
        pwb.place(x=220,y=450)
        pwb.pack()

    
    cvs.delete("INFO")
    draw_txt("SCORE"+str(score),160,60,32,"blue","INFO")
    draw_txt("HISC"+str(hisc),450,60,32,"yellow","INFO")
    if tsugi > 0:
        cvs.create_image(752,128,image=img_kigo[tsugi],tag="INFO")
    root.after(100,game_main)


root = tkinter.Tk()
root.title("落ち物パズル「記号」")
root.resizable(False,False)
root.bind("<Motion>",mouse_move)
root.bind("<ButtonPress>",mouse_press)
cvs=tkinter.Canvas(root,width=912,height=768)
cvs.pack()

bg= tkinter.PhotoImage(file="haikei.png")
cursor = tkinter.PhotoImage(file="waku.png")
img_kigo=[
    None,
    tkinter.PhotoImage(file="plus.png"),
    tkinter.PhotoImage(file="Minus.png"),
    tkinter.PhotoImage(file="times.png"),
    tkinter.PhotoImage(file="devided.png"),
    tkinter.PhotoImage(file="iquaru.png"),
    tkinter.PhotoImage(file="not_iquaru.png"),
    tkinter.PhotoImage(file="less.png"),
    tkinter.PhotoImage(file="greater.png"),
    tkinter.PhotoImage(file="unlimited.png")
]

cvs.create_image(456,384,image=bg)
game_main()
root.mainloop()
