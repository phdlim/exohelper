from math import*
import sys
import traceback
def exception_hook(ex_type,ex_value,tb):
    traceback.print_exception(ex_type,ex_value,tb)
    input("Press Enter to exit.")
    pass
sys.excepthook=exception_hook

f = open(r'star.txt')
lines = f.readlines()

sind=lambda d: sin(radians(d))
cosd=lambda d: cos(radians(d))
tand=lambda d: tan(radians(d))

class Star: #외계행성의 구조체 만들기
    def __lt__(self,other):
        return self.name<other.name
    def parse(self,string):

        splitted=string.split(",")
        self.name=splitted[0] #행성의 이름 저장
        self.period=float(splitted[1]) #행성의 주기 저장
        self.ra=float(splitted[2]) #행성의 적경 저장
        self.dec=float(splitted[3]) #행성의 적위 저장
        self.t14=float(splitted[4]) #행성이 항성 앞을 지나가는 시간 저장
        self.tt=float(splitted[5]) #행성의 극심시각 저장
    def high(self,phi,dec,t):
        h=asin(sind(dec)*sind(phi)+cosd(dec)*cosd(phi)*cosd(t))
        return h
    
stars=list()
for i in range(len(lines)):
    try:
        star=Star()
        star.parse(lines[i])
        stars.append(star)
    except ValueError:
        pass
stars.sort()

from tkinter import *
from tkinter import ttk




#graph and recommand time
def search():
    global k
    global period
    global ra
    global dec
    global t14
    global tt
    global year
    global month
    global day
    global phidegree
    global phiminute
    global phisecond
    global lambdahour
    global lambdaminute
    global lambdasecond
    global JD
    global phi_degree
    global lambda_degree
    global exo_namjung
    global sun_namjung
    global exorise
    global exoset
    global exo_high
    global sunrise
    global sunset
    global flatstart
    global flatend
    global tstart
    global tend
    global x_JD
    global dec_sun
        
#pick error
    try:
        #error in date
        if int(month)==2 and int(year)%4==0 and int(year)%100!=0 and int(day)>29:
            messagebox.showerror('date error', 'please repick date')
            return 0
        elif int(month)==2 and int(year)%400==0 and int(day)>29:
            messagebox.showerror('date error', 'please repick date')
            return 0
        elif int(month)==2 and int(day)>28:
            messagebox.showerror('date error', 'please repick date')
            return 0
        elif int(month)==4 or int(month)==6 or int(month)==9 or int(month)==11:
            if int(day)==31:
                messagebox.showerror('date error', 'please repick date')
                return 0
        elif int(phidegree)==90 and (int(phiminute)>0 or int(phisecond)>0):
            messagebox.showerror('latitude error', 'please repick latitude')
            return 0

        period=stars[k].period
        ra=stars[k].ra
        dec=stars[k].dec
        t14=stars[k].t14
        tt=stars[k].tt

    #error of not put anything
    except NameError:
        messagebox.showerror('exoplanet or date error or location error', 'please pick exoplanet or date or location')

    #calculate JD,phi,lambda
    calJD()
    calphi()
    callambda()
    calsun()
    caltransit()
    sun_south()
    
    #draw graph

    root2=Tk()
    root2.title('graph zone')
    canvas=Canvas(root2,width=900,height=600,bg='white')
    canvas.grid()
    canvas.create_line(100,500,800,500,width=2)
    canvas.create_line(100,50,100,500,width=2)
    canvas.create_text(100,40,text='height')
    canvas.create_text(830,500,text='time')
    if 90<=dec+phi_degree or dec-phi_degree<=-90:
        start=-12
        end=12
    else:
        exo_time()
        start=int(exorise)-1
        end=int(exoset)+2
    if start<0:
        start+=24
    if end<0:
        end+=24

    if start>end:
        end+=24
        cha=float(end-start)
    elif start==end:
        cha=24.0
    else:
        cha=float(end-start)
    if (exoset%24)<(exorise%24) and start%24<end%24:
        start=-12
        end=12
        cha=24.0            
    inter=700.0/cha
    for i in range(0,int(cha)+1):
        canvas.create_line(100+inter*i,500,100+inter*i,520,width=2)
        canvas.create_text(100+inter*i,530,text=(start+i)%24)


    for i in range(101,800):
        x=start+(i-100)/700.0*cha
        alpha=asin(sind(dec_sun)*sind(phi_degree)+cosd(dec_sun)*cosd(phi_degree)*cosd((sun_south()-x)*15))
        if alpha*180/pi<=-6:
            canvas.create_line(i,50,i,499,width=1,fill="#aaa")
        elif alpha*180/pi<=6:
            canvas.create_line(i,50,i,499,width=1,fill="#f0f")
        else:
            canvas.create_line(i,50,i,499,width=1,fill="#0ff")
        

        
    for i in range(0,10):
        canvas.create_line(80,500-i*50,100,500-i*50,width=2)
        canvas.create_text(70,500-i*50,text=i*10)
    for i in range(100,800):
        x=start+(i-100)/700.0*cha
        x_JD=JD+x/24
        y=star.high(phi_degree,dec,(exo_namjung-x)*15)*180/pi
        if ((tt-x_JD)%period)<=t14/86400/2+1/24 or ((tt-x_JD)%period)>=period-t14/86400/2-1/24:
            if y*5+15>=0:
                if y*5-15<0:
                    canvas.create_line(i,500-y*5-15,i,500,width=1,fill="#ff0")
                else:
                    canvas.create_line(i,500-y*5-15,i,500-y*5+15,width=1,fill="#ff0")

    for i in range(100,800):
        x=start+(i-100)/700.0*cha
        x_JD=JD+x/24
        y=star.high(phi_degree,dec,(exo_namjung-x)*15)*180/pi
        if ((tt-x_JD)%period)<=t14/86400/2 or ((tt-x_JD)%period)>=period-t14/86400/2:
            if y*5+15>=0:
                if y*5-15<0:
                    canvas.create_line(i,500-y*5-15,i,500,width=1,fill="green")
                else:
                    canvas.create_line(i,500-y*5-15,i,500-y*5+15,width=1,fill="green")
    for i in range(100,800):
        x=start+(i-100)/700.0*cha
        y=star.high(phi_degree,dec,(exo_namjung-x)*15)*180/pi
        if(y>=0):
            canvas.create_line(i,500-y*5+1,i,500-y*5-2,width=1)
    exo_high=star.high(phi_degree,dec,0)
    

def caltime():
    global time
    global lambda_degree
    callambda()
    if lambda_degree%15<=0.00001 or lambda_degree%15>=14.99999:
        time=(-lambda_degree)/15
    else:
        time=int((-lambda_degree)/15)+1
        

def calsun():
    global ra_sun
    global dec_sun
    global JD
    global lon
    global EOT_min
    global time
    caltime()
    d=JD-2451543.5
    w=radians(282.9404+4.70935/(10**5)*d)
    e=0.016709-1.1519/(10**9)*d
    M=radians((356.0470+0.9856002585*d)%360.0)
    oblecl=radians(23.4393- 3.563/(10**7)*d)
    E=M+e*sin(M)*(1+e*cos(M))
    x=cos(E)-e
    y=sin(E)*sqrt(1-e*e)
    v=atan2(y,x)
    lon=v+w
    xequat=cos(lon)
    yequat=sin(lon)*cos(oblecl)
    zequat=sin(lon)*sin(oblecl)
    ra_sun=atan2(yequat,xequat)*180/pi/15
    dec_sun=atan2(zequat,sqrt(xequat*xequat+yequat*yequat))*180/pi
    EOT_min=-7.659*sin(M)+9.863*sin(2*M+3.5932)

def sun_south():
    global JD
    global ra_sun
    global dec_sun
    global lon
    global EOT_min
    global lambda_degree
    global time
    
    calsun()
    JD_cen=(JD-2451545.0)/36525
    #꼭 점검하기 GST 식 의심
    LST=ra_sun
    GST=LST+lambda_degree/15.0
    theta= 100.46061837+36000.770053608*JD_cen+0.000387933*(JD_cen**2)+(JD_cen**3)/38710000.0
    UT=(GST-(theta%360.0)/15.0)/1.00273790935+EOT_min/60
    KST=UT+time
    return KST

def exo_south():
    global ra
    global lambda_degree
    global JD
    global time
    caltime()
    JD_cen=(JD-2451545.0)/36525
    #꼭 점검하기 GST 식 의심
    LST=ra
    GST=LST+lambda_degree/15.0
    theta= 100.46061837+36000.770053608*JD_cen+0.000387933*(JD_cen**2)+(JD_cen**3)/38710000.0
    UT=(GST-(theta%360.0)/15.0)/1.00273790935
    KST=UT+time
    return KST

def caltransit():
    global tt
    global t14
    global tstart
    global tend
    global period
    
    tstart=tt-(t14/2)/86400
    tend=tt+(t14/2)/86400

def exo_time():
    global phi_degree
    global dec
    global exo_namjung
    global exorise
    global exoset

    t=acos(-tan(radians(phi_degree))*tan(radians(dec)))
    exo_namjung=exo_south()
    if exo_namjung<0:
        exo_namjung+=24
    exorise=exo_namjung-t*12/pi
    exoset=exo_namjung+t*12/pi
    if exorise<0:
        exorise+=24
    if exoset<0:
        exoset+=24
    if exorise>24:
        exorise-=24
    if exoset>24:
        exoset-=24

def calJD():
    global JD
    global year
    global month
    global day
    global year_1
    global month_1
    global day_1
    global time
    caltime()
    if int(month)==1 or int(month)==2:
        month_1=int(month)+12 
        year_1=int(year)-1
    else:
        month_1=int(month)
        year_1=int(year)
    day_1=int(day)
    JD=int(365.25*year_1)+int(year_1/400.0)-int(year_1/100.0)+int(30.59*(month_1-2))+day_1-678912+2400000.5-time/24
    
def calphi():
    global phidegree
    global phiminute
    global phisecond
    global phi_degree
    phi_degree=float(phidegree)+float(phiminute)/60+float(phisecond)/3600

def callambda():
    global lambdadegree
    global lambdaminute
    global lambdasecond
    global lambdadirection
    global lambda_degree
    if(lambdadirection=='w'):
        lambda_degree=float(lambdadegree)+float(lambdaminute)/60+float(lambdasecond)/3600
    elif(lambdadirection=='e'):
        lambda_degree=-(float(lambdadegree)+float(lambdaminute)/60+float(lambdasecond)/3600)
#get date
def chkyear(evt):
    global year
    global Cyear
    year=Cyear.get()
def chkmonth(evt):
    global month
    global Cmonth
    month=Cmonth.get()
def chkday(evt):
    global day
    global Cday
    day=Cday.get()
def chkphidegree(evt):
    global phidegree
    global Cphidegree
    phidegree=Cphidegree.get()
def chkphiminute(evt):
    global phiminute
    global Cphiminute
    phiminute=Cphiminute.get()
def chkphisecond(evt):
    global phisecond
    global Cphisecond
    phisecond=Cphisecond.get()
def chklambdadegree(evt):
    global lambdadegree
    global Clambdadegree
    lambdadegree=Clambdadegree.get()
def chklambdaminute(evt):
    global lambdaminute
    global Clambdaminute
    lambdaminute=Clambdaminute.get()
def chklambdasecond(evt):
    global lambdasecond
    global Clambdasecond
    lambdasecond=Clambdasecond.get()
def chklambdadirection(evt):
    global lambdadirection
    global Clambdadirection
    lambdadirection=Clambdadirection.get()
#get latitude
#find exoplanet
def move(evt):
    global k
    global searchlist
    global tv
    k=searchlist.curselection()[0]
    tv.set(stars[k].name)
def findexo():
    global searchlist
    root1=Tk()
    frame=Frame(root1)
    frame.grid()
    search=Entry(root1)
    search.grid()
    searchlist=Listbox(root1,selectmode=SINGLE)
    stars.sort()
    for i in range(len(stars)):
        searchlist.insert(i, stars[i].name)
    searchlist.bind('<Double-1>',move)
    searchlist.grid()
   

Start=Tk()
Start.title("Exo Helper ver3")
note=ttk.Notebook(Start)
note.grid()



#frame
root=ttk.Frame(note)
tv=StringVar()
tv.set("Not Selected")
#exoplanet search
B1=Button(root,text="find exoplanet")
B1['command']=findexo
T1=Label(root,textvariable=tv)
#Pick time
Tdate=Label(root,text="date")
yearlist=list(range(2000,2100))
Cyear=ttk.Combobox(root,width=4)
Cyear['values']=yearlist
Cyear.bind('<<ComboboxSelected>>', chkyear)
Tyear=Label(root,text="year")
Cmonth=ttk.Combobox(root,width=2)
monthlist=list(range(1,13))
Cmonth['values']=monthlist
Cmonth.bind('<<ComboboxSelected>>', chkmonth)
Tmonth=Label(root,text="month")
Cday=ttk.Combobox(root,width=2)
Cday.bind('<<ComboboxSelected>>', chkday)
daylist=list(range(1,32))
Cday['values']=daylist
Tday=Label(root,text="day")
#Pick latitude
Tphi=Label(root,text='latitude')
#pick degree
Cphidegree=ttk.Combobox(root, width=2)
phidegreelist=list(range(0,91))
Cphidegree['values']=phidegreelist
Cphidegree.bind('<<ComboboxSelected>>',chkphidegree)
Tphidegree=Label(root,text='deg')
#pick minute
phiminutelist=list(range(0,60))
Cphiminute=ttk.Combobox(root,width=2)
Cphiminute['values']=phiminutelist
Cphiminute.bind('<<ComboboxSelected>>',chkphiminute)
Tphiminute=Label(root,text='min')
#pick second
phisecondlist=list(range(0,60))
Cphisecond=ttk.Combobox(root,width=2)
Cphisecond['values']=phisecondlist
Cphisecond.bind('<<ComboboxSelected>>',chkphisecond)
Tphisecond=Label(root,text='sec')
#Pick longitude
Tlambda=Label(root,text='longitude')
#pick west east
lambdadirectionlist=[E,W]
Clambdadirection=ttk.Combobox(root,width=1)
Clambdadirection['values']=lambdadirectionlist
Clambdadirection.bind('<<ComboboxSelected>>',chklambdadirection)
#pick degree
lambdadegreelist=list(range(0,180))
Clambdadegree=ttk.Combobox(root, width=3)
Clambdadegree['values']=lambdadegreelist
Clambdadegree.bind('<<ComboboxSelected>>',chklambdadegree)
Tlambdadegree=Label(root,text='deg')
#pick minute
lambdaminutelist=list(range(0,60))
Clambdaminute=ttk.Combobox(root,width=2)
Clambdaminute['values']=lambdaminutelist
Clambdaminute.bind('<<ComboboxSelected>>',chklambdaminute)
Tlambdaminute=Label(root,text='min')
#pick second
lambdasecondlist=list(range(0,60))
Clambdasecond=ttk.Combobox(root,width=2)
Clambdasecond['values']=lambdasecondlist
Clambdasecond.bind('<<ComboboxSelected>>',chklambdasecond)
Tlambdasecond=Label(root,text='sec')
Bfind=Button(root,text="search!!!")
Bfind['command']=search
Tdev=Label(root,text="developed by DOHOON LIM")

B1.grid(row=1,column=3)
T1.grid(row=2,column=3)

Tdate.grid()
Cyear.grid(row=3,column=1)
Tyear.grid(row=3,column=2)
Cmonth.grid(row=3,column=3)
Tmonth.grid(row=3,column=4)
Cday.grid(row=3,column=5)
Tday.grid(row=3,column=6)
Tphi.grid(row=4,column=0)
Cphidegree.grid(row=4,column=1)
Tphidegree.grid(row=4, column=2)
Cphiminute.grid(row=4,column=3)
Tphiminute.grid(row=4,column=4)
Cphisecond.grid(row=4,column=5)
Tphisecond.grid(row=4,column=6)
Tlambda.grid(row=5,column=0)
Clambdadirection.grid(row=5,column=1)
Clambdadegree.grid(row=5,column=2)
Tlambdadegree.grid(row=5, column=3)
Clambdaminute.grid(row=5,column=4)
Tlambdaminute.grid(row=5,column=5)
Clambdasecond.grid(row=5,column=6)
Tlambdasecond.grid(row=5,column=7)
Bfind.grid(column=3)
Tdev.grid()
tab1 = note.add(root,text = "Search single exoplanet")

def calsun1():
    global ra_sun1
    global dec_sun1
    global JD1
    global lon1
    global EOT_min1

    d=JD1-2451543.5
    w=radians(282.9404+4.70935/(10**5)*d)
    e=0.016709-1.1519/(10**9)*d
    M=radians((356.0470+0.9856002585*d)%360.0)
    oblecl=radians(23.4393- 3.563/(10**7)*d)
    E=M+e*sin(M)*(1+e*cos(M))
    x=cos(E)-e
    y=sin(E)*sqrt(1-e*e)
    v=atan2(y,x)
    lon1=v+w
    xequat=cos(lon1)
    yequat=sin(lon1)*cos(oblecl)
    zequat=sin(lon1)*sin(oblecl)
    ra_sun1=atan2(yequat,xequat)*180/pi/15
    dec_sun1=atan2(zequat,sqrt(xequat*xequat+yequat*yequat))*180/pi
    EOT_min1=-7.659*sin(M)+9.863*sin(2*M+3.5932)

def sun_south1():
    global JD1
    global ra_sun1
    global dec_sun1
    global lon1
    global EOT_min1
    global lambda_degree1
    global time1
    
    caltime1()
    calsun1()
    JD_cen=(JD1-2451545.0)/36525
    #꼭 점검하기 GST 식 의심
    LST=ra_sun1
    GST=LST+lambda_degree1/15.0
    theta= 100.46061837+36000.770053608*JD_cen+0.000387933*(JD_cen**2)+(JD_cen**3)/38710000.0
    UT=(GST-(theta%360.0)/15.0)/1.00273790935+EOT_min1/60
    KST=UT+time1
    return KST

def exo_south1(k):
    ra=stars[k].ra
    global lambda_degree1
    global JD1
    global time1
    caltime1()

    JD_cen=(JD1-2451545.0)/36525
    #꼭 점검하기 GST 식 의심
    LST=ra
    GST=LST+lambda_degree1/15.0
    theta= 100.46061837+36000.770053608*JD_cen+0.000387933*(JD_cen**2)+(JD_cen**3)/38710000.0
    UT=(GST-(theta%360.0)/15.0)/1.00273790935
    KST=UT+time1
    return KST

def caltransit1(k):
    tt=stars[k].tt
    t14=stars[k].t14
    global tstart1
    global tend1
    period=stars[k].period
    tstart1=tt-(t14/2)/86400.0
    tend1=tt+(t14/2)/86400.0

def exo_time1(k):
    global phi_degree1
    dec=stars[k].dec
    global exo_namjung1
    global exorise1
    global exoset1

    if -tan(radians(phi_degree1))*tan(radians(dec))>1:
        a=1
    elif -tan(radians(phi_degree1))*tan(radians(dec))<-1:
        a=-1
    else:
        a=-tan(radians(phi_degree1))*tan(radians(dec))
    t=acos(a)
    exo_namjung1=exo_south1(k)
    if exo_namjung1<0:
        exo_namjung1+=24
    exorise1=exo_namjung1-t*12/pi
    exoset1=exo_namjung1+t*12/pi
    if exorise1<0:
        exorise1+=24
    if exoset1<0:
        exoset1+=24
    if exorise1>24:
        exorise1-=24
    if exoset1>24:
        exoset1-=24

def calJD1():
    global JD1
    global year1
    global month1
    global day1
    global time1
    caltime1()
    if int(month1)==1 or int(month1)==2:
        month_1=int(month1)+12 
        year_1=int(year1)-1
    else:
        month_1=int(month1)
        year_1=int(year1)
    day_1=int(day1)
    JD1=int(365.25*year_1)+int(year_1/400.0)-int(year_1/100.0)+int(30.59*(month_1-2))+day_1-678912+2400000.5-time1/24
    
def calphi1():
    global phidegree1
    global phiminute1
    global phisecond1
    global phi_degree1
    phi_degree1=float(phidegree1)+float(phiminute1)/60+float(phisecond1)/3600

def callambda1():
    global lambdadegree1
    global lambdaminute1
    global lambdasecond1
    global lambdadirection1
    global lambda_degree1
    if(lambdadirection1=='w'):
        lambda_degree1=float(lambdadegree1)+float(lambdaminute1)/60+float(lambdasecond1)/3600
    elif(lambdadirection1=='e'):
        lambda_degree1=-(float(lambdadegree1)+float(lambdaminute1)/60+float(lambdasecond1)/3600)
def caltime1():
    global time1
    global lambda_degree1
    callambda1()
    if lambda_degree1%15<=0.00001 or lambda_degree1%15>=14.99999:
        time1=(-lambda_degree1)/15
    else:
        time1=int((-lambda_degree1)/15)+1

def search1():
    global year1
    global month1
    global day1
    global phidegree1
    global phiminute1
    global phisecond1
    global lambdahour1
    global lambdaminute1
    global lambdasecond1
    global JD1
    global phi_degree1
    global lambda_degree1
    global exo_namjung1
    global sun_namjung1
    global exorise1
    global exoset1
    global exo_high1
    global tstart1
    global tend1
    global x_JD1
    global dec_sun1
    global starlist
    global searchlist1
    global starlist1
    
#pick error
    try:
        #error in date
        if int(month1)==2 and int(year1)%4==0 and int(year1)%100!=0 and int(day1)>29:
            messagebox.showerror('date error', 'please repick date')
            return 0
        elif int(month1)==2 and int(year1)%400==0 and int(day1)>29:
            messagebox.showerror('date error', 'please repick date')
            return 0
        elif int(month1)==2 and int(day1)>28:
            messagebox.showerror('date error', 'please repick date')
            return 0
        elif int(month1)==4 or int(month1)==6 or int(month1)==9 or int(month1)==11:
            if int(day1)==31:
                messagebox.showerror('date error', 'please repick date')
                return 0
        elif int(phidegree1)==90 and (int(phiminute1)>0 or int(phisecond1)>0):
            messagebox.showerror('latitude error', 'please repick latitude')
            return 0

    #error of not put anything
    except NameError:
        messagebox.showerror('date error or location error', 'please pick date or location')


    #calculate JD,phi,lambda
    calJD1()
    calphi1()
    callambda1()
    calsun1()
    sun_south1()

    starlist=list()
    for i in range(len(stars)):
        period=stars[i].period
        caltransit1(i)
        exo_time1(i)
        if exorise1<exoset1:
            b=exoset1/24+JD1
        else:
            b=exoset1/24+1+JD1
        a=JD1+exorise1/24
        R=int((a-tstart1)/period)
        S=int((b-tend1)/period)
        dec=stars[i].dec
        if radians(phi_degree1)-radians(dec)<pi/2:
            if R<S:
                starlist.append(i)
            elif R==S and R==(a-tstart1)/period:
                starlist.append(i)
    
    root3=Tk()
    frame=Frame(root3)
    frame.grid()
    searchlist1=Listbox(root3,selectmode=SINGLE)
    for i in range(len(starlist)):
            searchlist1.insert(i, stars[starlist[i]].name)
    searchlist1.bind('<Double-1>',graph)
    searchlist1.grid()

    #draw graph
def graph(evt):
    global year1
    global month1
    global day1
    global phidegree1
    global phiminute1
    global phisecond1
    global lambdahour1
    global lambdaminute1
    global lambdasecond1
    global JD1
    global phi_degree1
    global lambda_degree1
    global exo_namjung1
    global sun_namjung1
    global exorise1
    global exoset1
    global exo_high1
    global tstart1
    global tend1
    global x_JD1
    global dec_sun1
    global starlist
    global searchlist1
    calJD1()
    calphi1()
    callambda1()
    calsun1()
    sun_south1()
    k=searchlist1.curselection()[0]
    caltransit1(starlist[k])
    exo_time1(starlist[k])
    dec=stars[starlist[k]].dec
    period=stars[starlist[k]].period
    ra=stars[starlist[k]].ra
    t14=stars[starlist[k]].t14
    tt=stars[starlist[k]].tt
    root4=Tk()
    root4.title('graph zone')
    canvas=Canvas(root4,width=900,height=600,bg='white')
    canvas.grid()
    canvas.create_line(100,500,800,500,width=2)
    canvas.create_line(100,50,100,500,width=2)
    canvas.create_text(100,40,text='height')
    canvas.create_text(830,500,text='time')
    if 90<=dec+phi_degree1 or dec-phi_degree1<=-90:
        start=-12
        end=12
    else:
        start=int(exorise1)-1
        end=int(exoset1)+2
    if start<0:
        start+=24
    if end<0:
        end+=24

    if start>end:
        end+=24
        cha=float(end-start)
    elif start==end:
        cha=24.0
    else:
        cha=float(end-start)
    if (exoset1%24)<(exorise1%24) and start%24<end%24:
        start=-12
        end=12
        cha=24.0            
    inter=700.0/cha
    for i in range(0,int(cha)+1):
        canvas.create_line(100+inter*i,500,100+inter*i,520,width=2)
        canvas.create_text(100+inter*i,530,text=(start+i)%24)


    for i in range(101,800):
        x=start+(i-100)/700.0*cha
        alpha=asin(sind(dec_sun1)*sind(phi_degree1)+cosd(dec_sun1)*cosd(phi_degree1)*cosd((sun_south1()-x)*15))
        if alpha*180/pi<=-6:
            canvas.create_line(i,50,i,499,width=1,fill="#aaa")
        elif alpha*180/pi<=6:
            canvas.create_line(i,50,i,499,width=1,fill="#f0f")
        else:
            canvas.create_line(i,50,i,499,width=1,fill="#0ff")
        

        
    for i in range(0,10):
        canvas.create_line(80,500-i*50,100,500-i*50,width=2)
        canvas.create_text(70,500-i*50,text=i*10)
    for i in range(100,800):
        x=start+(i-100)/700.0*cha
        x_JD1=JD1+x/24
        y=star.high(phi_degree1,dec,(exo_namjung1-x)*15)*180/pi
        if ((tt-x_JD1)%period)<=t14/86400/2+1/24 or ((tt-x_JD1)%period)>=period-t14/86400/2-1/24:
            if y*5+15>=0:
                if y*5-15<0:
                    canvas.create_line(i,500-y*5-15,i,500,width=1,fill="#ff0")
                else:
                    canvas.create_line(i,500-y*5-15,i,500-y*5+15,width=1,fill="#ff0")

    for i in range(100,800):
        x=start+(i-100)/700.0*cha
        x_JD1=JD1+x/24
        y=star.high(phi_degree1,dec,(exo_namjung1-x)*15)*180/pi
        if ((tt-x_JD1)%period)<=t14/86400/2 or ((tt-x_JD1)%period)>=period-t14/86400/2:
            if y*5+15>=0:
                if y*5-15<0:
                    canvas.create_line(i,500-y*5-15,i,500,width=1,fill="green")
                else:
                    canvas.create_line(i,500-y*5-15,i,500-y*5+15,width=1,fill="green")
    for i in range(100,800):
        x=start+(i-100)/700.0*cha
        y=star.high(phi_degree1,dec,(exo_namjung1-x)*15)*180/pi
        if(y>=0):
            canvas.create_line(i,500-y*5+1,i,500-y*5-2,width=1)
    exo_high=star.high(phi_degree1,dec,0)


def chkyear1(evt):
    global year1
    global Cyear1
    year1=Cyear1.get()
def chkmonth1(evt):
    global month1
    global Cmonth1
    month1=Cmonth1.get()
def chkday1(evt):
    global day1
    global Cday1
    day1=Cday1.get()
def chkphidegree1(evt):
    global phidegree1
    global Cphidegree1
    phidegree1=Cphidegree1.get()
def chkphiminute1(evt):
    global phiminute1
    global Cphiminute1
    phiminute1=Cphiminute1.get()
def chkphisecond1(evt):
    global phisecond1
    global Cphisecond1
    phisecond1=Cphisecond1.get()
def chklambdadegree1(evt):
    global lambdadegree1
    global Clambdadegree1
    lambdadegree1=Clambdadegree1.get()
def chklambdaminute1(evt):
    global lambdaminute1
    global Clambdaminute1
    lambdaminute1=Clambdaminute1.get()
def chklambdasecond1(evt):
    global lambdasecond1
    global Clambdasecond1
    lambdasecond1=Clambdasecond1.get()
def chklambdadirection1(evt):
    global lambdadirection1
    global Clambdadirection1
    lambdadirection1=Clambdadirection1.get()


#frame
rootprime=ttk.Frame(note)

#Pick time
Tdate1=Label(rootprime,text="date")
yearlist1=list(range(2000,2100))
Cyear1=ttk.Combobox(rootprime,width=4)
Cyear1['values']=yearlist1
Cyear1.bind('<<ComboboxSelected>>', chkyear1)
Tyear1=Label(rootprime,text="year")
Cmonth1=ttk.Combobox(rootprime,width=2)
monthlist1=list(range(1,13))
Cmonth1['values']=monthlist1
Cmonth1.bind('<<ComboboxSelected>>', chkmonth1)
Tmonth1=Label(rootprime,text="month")
Cday1=ttk.Combobox(rootprime,width=2)
Cday1.bind('<<ComboboxSelected>>', chkday1)
daylist1=list(range(1,32))
Cday1['values']=daylist1
Tday1=Label(rootprime,text="day")
#Pick latitude
Tphi1=Label(rootprime,text='latitude')
#pick degree
Cphidegree1=ttk.Combobox(rootprime, width=2)
phidegreelist1=list(range(0,91))
Cphidegree1['values']=phidegreelist1
Cphidegree1.bind('<<ComboboxSelected>>',chkphidegree1)
Tphidegree1=Label(rootprime,text='deg')
#pick minute
phiminutelist1=list(range(0,60))
Cphiminute1=ttk.Combobox(rootprime,width=2)
Cphiminute1['values']=phiminutelist1
Cphiminute1.bind('<<ComboboxSelected>>',chkphiminute1)
Tphiminute1=Label(rootprime,text='min')
#pick second
phisecondlist1=list(range(0,60))
Cphisecond1=ttk.Combobox(rootprime,width=2)
Cphisecond1['values']=phisecondlist1
Cphisecond1.bind('<<ComboboxSelected>>',chkphisecond1)
Tphisecond1=Label(rootprime,text='sec')
#Pick longitude
Tlambda1=Label(rootprime,text='longitude')
#pick west east
lambdadirectionlist1=[E,W]
Clambdadirection1=ttk.Combobox(rootprime,width=1)
Clambdadirection1['values']=lambdadirectionlist1
Clambdadirection1.bind('<<ComboboxSelected>>',chklambdadirection1)
#pick degree
lambdadegreelist1=list(range(0,180))
Clambdadegree1=ttk.Combobox(rootprime, width=3)
Clambdadegree1['values']=lambdadegreelist1
Clambdadegree1.bind('<<ComboboxSelected>>',chklambdadegree1)
Tlambdadegree1=Label(rootprime,text='deg')
#pick minute
lambdaminutelist1=list(range(0,60))
Clambdaminute1=ttk.Combobox(rootprime,width=2)
Clambdaminute1['values']=lambdaminutelist1
Clambdaminute1.bind('<<ComboboxSelected>>',chklambdaminute1)
Tlambdaminute1=Label(rootprime,text='min')
#pick second
lambdasecondlist1=list(range(0,60))
Clambdasecond1=ttk.Combobox(rootprime,width=2)
Clambdasecond1['values']=lambdasecondlist1
Clambdasecond1.bind('<<ComboboxSelected>>',chklambdasecond1)
Tlambdasecond1=Label(rootprime,text='sec')
Bfind1=Button(rootprime,text="search!!!")
Bfind1['command']=search1
Tdev1=Label(rootprime,text="developed by DOHOON LIM")

Tdate1.grid(row=2)
Cyear1.grid(row=2,column=1)
Tyear1.grid(row=2,column=2)
Cmonth1.grid(row=2,column=3)
Tmonth1.grid(row=2,column=4)
Cday1.grid(row=2,column=5)
Tday1.grid(row=2,column=6)
Tphi1.grid(row=3,column=0)
Cphidegree1.grid(row=3,column=1)
Tphidegree1.grid(row=3,column=2)
Cphiminute1.grid(row=3,column=3)
Tphiminute1.grid(row=3,column=4)
Cphisecond1.grid(row=3,column=5)
Tphisecond1.grid(row=3,column=6)
Tlambda1.grid(row=4,column=0)
Clambdadirection1.grid(row=4,column=1)
Clambdadegree1.grid(row=4,column=2)
Tlambdadegree1.grid(row=4, column=3)
Clambdaminute1.grid(row=4,column=4)
Tlambdaminute1.grid(row=4,column=5)
Clambdasecond1.grid(row=4,column=6)
Tlambdasecond1.grid(row=4,column=7)
Bfind1.grid(column=3)
Tdev1.grid()
tab2 = note.add(rootprime,text = "Search date")  
