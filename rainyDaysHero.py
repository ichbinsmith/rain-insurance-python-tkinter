#Authors : Smith Djamoura & Arnaud Ott

#Imports and global variables
import math
import tkinter as TK
from tkinter import messagebox as tkMessageBox
from tkcalendar import Calendar, DateEntry
from PIL import ImageTk,Image 
from fpdf import FPDF
import os
import requests as REQ
import pandas as pd
import matplotlib.pyplot as plt

import datetime as DtT

interestRate = 0.1

cityId = {'Nice' :'181' , 'Paris':'188' , 'Nantes':'221'}
baseUrl = 'https://www.historique-meteo.net/site/export.php?ville_id='


'''  Utils  '''

def dataUpdateCity(city):
    r = REQ.get(baseUrl+city, allow_redirects=True)
    print( r.headers.get('Content-disposition').split(';')[1].split('=')[1] )
    open(os.path.dirname(os.path.realpath(__file__))+"\\data\\"+r.headers.get('Content-disposition').split(';')[1].split('=')[1], 'wb').write(r.content)

def dataUpdateAllCity():
    for city in cityId.values():
        dataUpdateCity(city)


def popupmsg(msg):
    popup = TK.Tk()
    popup.eval('tk::PlaceWindow . center')
    popup.configure(bg='#EBF5FB')
    default_font = TK.font.nametofont("TkDefaultFont")
    default_font.configure(size=12)
    popup.wm_title("!")
    popup.resizable(0, 0)
    popup.configure(bg='#EBF5FB')
    label = TK.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = TK.Button(popup, text='Okay', command = popup.destroy)
    B1.pack()
    popup.after(1, lambda: popup.focus_force())
    popup.mainloop()

def buildQuotationPDF(clientName='Carrefour Antibes',turnover=1000, fixedCosts=998,rainfall=0.5,date=DtT.date.today(), location='Paris', premium=10000):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.rect(5.0, 5.0, 200.0,287.0)
    pdf.rect(8.0, 8.0, 194.0,282.0)

    #App pic
    pdf.image(os.path.dirname(os.path.realpath(__file__))+"\\img\\rdh.png", 10, 8, 33)
    pdf.set_font('Arial', 'B', 15)

    # Client Name
    pdf.cell(140)
    pdf.cell(0, 5, clientName, ln=1)

    #Company name
    pdf.ln(25)
    pdf.cell(0, 5, 'Rainy Days Hero', ln=1)
    
    #Informatios
    pdf.set_text_color(238, 58, 20)
    pdf.ln(6)
    pdf.cell(60)
    pdf.cell(65, 10, 'Rain Insurance quotation','B', ln=2)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(65, 10, "Max daily turover: "+str(turnover), ln=2)
    pdf.cell(65, 10, "Fixed costs: "+str(fixedCosts), ln=2)
    pdf.cell(65, 10, "Crucial rainfall: "+str(rainfall), ln=2)
    pdf.cell(65, 10, "Subsciption date: "+date.strftime("%Y-%m-%d"), ln=2)
    pdf.cell(65, 10, "Duration: "+"365 days", ln=2)
    pdf.cell(65, 10, "Location: "+location, ln=2)

    #premium
    pdf.set_text_color(39, 174, 96)
    pdf.ln(25)
    pdf.cell(60)
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(65, 10, "Premium: "+str("%.2f" % premium)+" "+chr(128), ln=2)




    if os.path.exists(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')+'\\quotation.pdf'):
        os.remove(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')+'\\quotation.pdf')
    pdf.output(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')+'\\quotation.pdf','F')


def buildRetroPDF(clientName='Carrefour Antibes',turnover=1000, fixedCosts=998,rainfall=0.5,date=DtT.date.today(), location='Paris', premium=10000,c=[10 for _ in range(365)],nc=[10 for _ in range(365)]):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.rect(5.0, 5.0, 200.0,287.0)
    pdf.rect(8.0, 8.0, 194.0,282.0)

    #App pic
    pdf.image(os.path.dirname(os.path.realpath(__file__))+"\\img\\rdh.png", 10, 8, 33)
    pdf.set_font('Arial', 'B', 15)

    # Client Name
    pdf.cell(140)
    pdf.cell(0, 5, clientName, ln=1)

    #Company name
    pdf.ln(25)
    pdf.cell(0, 5, 'Rainy Days Hero', ln=1)
    
    #Informations
    pdf.set_text_color(238, 58, 20)
    pdf.ln(6)
    pdf.cell(60)
    pdf.cell(65, 10, 'Rain Insurance retrospective','B', ln=2)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(65, 10, "Max daily turover: "+str(turnover), ln=2)
    pdf.cell(65, 10, "Fixed costs: "+str(fixedCosts), ln=2)
    pdf.cell(65, 10, "Crucial rainfall: "+str(rainfall), ln=2)
    pdf.cell(65, 10, "Subsciption date: "+date.strftime("%Y-%m-%d"), ln=2)
    pdf.cell(65, 10, "Duration: "+"365 days", ln=2)
    pdf.cell(65, 10, "Location: "+location, ln=2)

    #premium
    pdf.set_text_color(39, 174, 96)
    pdf.ln(10)
    pdf.cell(60)
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(65, 10, "Premium Price: "+str("%.2f" % premium)+" "+chr(128), ln=2)
    pdf.cell(65, 10, "Covered Result: "+str("%.2f" % (sum(c)-premium) )+" "+chr(128), ln=2)
    pdf.cell(65, 10, "Uncovered Result: "+str("%.2f" % sum(nc))+" "+chr(128), ln=2)

    #graph
    days = [i for i in range(365)]

    plt.plot(days,c,label="Covered")
    plt.plot(days,nc,label="Uncovered")


    #plot graph
    plt.title("Result Evolution Graph", fontweight="bold", fontsize=16, color="blue")
    plt.tight_layout()
    #plt.legend(loc='best')
    lgd = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),fancybox=True, shadow=True, ncol=5)
    plt.savefig(os.path.dirname(os.path.realpath(__file__))+"\\img\\graph.png", bbox_extra_artists=(lgd,), bbox_inches='tight')


    pdf.image(os.path.dirname(os.path.realpath(__file__))+"\\img\\graph.png",45, 170 ,120)

    #delete the fig
    os.remove(os.path.dirname(os.path.realpath(__file__))+"\\img\\graph.png")


    if os.path.exists(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')+'\\retrospective.pdf'):
        os.remove(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')+'\\retrospective.pdf')
    pdf.output(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')+'\\retrospective.pdf','F')

    plt.clf()




'''End Utils'''


#annual prime - 365 days, daily sinister protection
def calculatePrice(mainFrame):
    print("Princing...")
    premium = 0
    def printArgs():
        print('clientName', mainFrame.clientNameEntry.get())
        print('turnover', mainFrame.turnoverEntry.get())
        print('fixedCostsEntry', mainFrame.fixedCostsEntry.get())
        print('rainfallEntry', mainFrame.rainfallEntry.get())
        print('subscriptionDateEntry', mainFrame.subscriptionDateEntry.get())
        print('locationEntry', mainFrame.locationEntry.get())
    printArgs()
    clientName = mainFrame.clientNameEntry.get()
    turnover= float(mainFrame.turnoverEntry.get())
    fixedCostsEntry= float(mainFrame.fixedCostsEntry.get())
    rainfallEntry= float(mainFrame.rainfallEntry.get())
    subscriptionDateEntry= mainFrame.subscriptionDateEntry.get()
    locationEntry= mainFrame.locationEntry.get()

    #data to use according to city : init dataFrame //TODO : update data before using
    locationEntry = locationEntry.lower()
    df = pd.read_csv(os.path.dirname(os.path.realpath(__file__))+"\\data\\export-"+locationEntry+".csv",skiprows=3)

    #compute premium
    tempDate = subscriptionDateEntry
    subscriptionDateEntry = DtT.datetime.strptime(subscriptionDateEntry, "%Y-%m-%d")
    tempDate = DtT.datetime.strptime(tempDate, "%Y-%m-%d")
    plca = (1 - fixedCostsEntry/turnover)*rainfallEntry
    countSinister = 0
    for i in range(365):
        tempDate = tempDate + DtT.timedelta(days=1)
        mm = '%02d' %  tempDate.month
        dd = '%02d' %  tempDate.day
        pltDf = df[df['DATE'].str.contains(mm+'-'+dd)]
        plt = sum((pltDf['PRECIP_TOTAL_DAY_MM'])) / len(pltDf.index)

        '''
        if plt > plca:
            sinister = 0
            if plt > rainfallEntry:
                sinister = fixedCostsEntry
            else:
                sinister = turnover*( (rainfallEntry - plt) / rainfallEntry ) - fixedCostsEntry
            premium+= (1 / ( 1 + interestRate*i/360 ) )*(abs(fixedCostsEntry-sinister))
        '''
        sinister = 0
        if plt > rainfallEntry:
            sinister = fixedCostsEntry
        else:
            sinister = -min(0, turnover*( (rainfallEntry - plt) / rainfallEntry ) - fixedCostsEntry)
        premium+= sinister / ( 1 + interestRate*i/360 )
        if sinister > 0 :
            countSinister+=1
    print('Premium = ',premium)
    print('Total sinister = ',countSinister)
    choice = tkMessageBox.askquestion("Premium", "Price: "+str("%.2f" % premium)+" "+chr(8364)+"."+"\n" +"Print quotation ?", icon='info')
    if choice == 'yes':
        print('aight ! we gonna print your quotation.')
        buildQuotationPDF(clientName,turnover, fixedCostsEntry,rainfallEntry,subscriptionDateEntry, locationEntry.capitalize(), premium)
    else:
        print('goodbye !')


#Retrospective for given args
def computeRetro(mainFrame):
    print("Computing...")
    def printArgs():
        print('clientName', mainFrame.clientNameEntry.get())
        print('turnover', mainFrame.turnoverEntry.get())
        print('fixedCostsEntry', mainFrame.fixedCostsEntry.get())
        print('rainfallEntry', mainFrame.rainfallEntry.get())
        print('RetroYearEntry', mainFrame.retroYearEntry.get())
        print('locationEntry', mainFrame.locationEntry.get())
    printArgs()
    clientName = mainFrame.clientNameEntry.get()
    turnover= float(mainFrame.turnoverEntry.get())
    fixedCostsEntry= float(mainFrame.fixedCostsEntry.get())
    rainfallEntry= float(mainFrame.rainfallEntry.get())
    retroYearEntry= mainFrame.retroYearEntry.get()
    locationEntry= mainFrame.locationEntry.get()

    days = [i for i in range(365)]
    nc = [-fixedCostsEntry for _ in range(365)]
    c = [0 for _ in range(365)]

    #data to use according to city : init dataFrame //TODO : update data before using
    locationEntry = locationEntry.lower()
    df = pd.read_csv(os.path.dirname(os.path.realpath(__file__))+"\\data\\export-"+locationEntry+".csv",skiprows=3)

    #compute retro
    tempDate = retroYearEntry+'-01-01'
    subscriptionDateEntry = DtT.datetime.strptime(tempDate, "%Y-%m-%d")
    tempDate = DtT.datetime.strptime(tempDate, "%Y-%m-%d")
    plca = (1 - fixedCostsEntry/turnover)*rainfallEntry
    countSinister = 0
    premium = 0
    for i in range(365):
        tempDate = tempDate + DtT.timedelta(days=1)
        mm = '%02d' %  tempDate.month
        dd = '%02d' %  tempDate.day
        pltDf = df[df['DATE'].str.contains(mm+'-'+dd)]
        #pltDf = df[df['DATE'].str.contains(mm+'-'+dd) and df['DATE'] < retroYearEntry ]
        plt = sum((pltDf['PRECIP_TOTAL_DAY_MM'])) / len(pltDf.index)


        sinister = 0
        if plt > rainfallEntry:
            sinister = fixedCostsEntry
        else:
            sinister = -min(0, turnover*( (rainfallEntry - plt) / rainfallEntry ) - fixedCostsEntry)

        if sinister > 0 :
            nc[i] = - sinister
            c[i] = 0
            countSinister+=1
        else:
            nc[i] = turnover*( (rainfallEntry - plt) / rainfallEntry ) - fixedCostsEntry
            c[i] = turnover*( (rainfallEntry - plt) / rainfallEntry ) - fixedCostsEntry

        premium+= sinister / ( 1 + interestRate*i/360 )

    print('Premium = ',premium)
    print('Total sinister = ',countSinister)
    choice = tkMessageBox.askquestion("Premium", "Premium Price: "+str("%.2f" % premium)+" "+chr(8364)+"."+"\n"+"Covered Result: "+str(sum(c)-premium )+"\n" +"Uncovered Result: "+str(sum(nc))+"\n"+"Print retrospective ?", icon='info')
    if choice == 'yes':
        print('aight ! we gonna print your retrospective.')
        buildRetroPDF(clientName,turnover, fixedCostsEntry,rainfallEntry,subscriptionDateEntry, locationEntry.capitalize(), premium,c,nc)
    else:
        print('goodbye !')

class App(TK.Tk):
    def __init__(self, *args, **kwargs):
        TK.Tk.__init__(self, *args, **kwargs)

        #windows creation and default configs
        self.ico = TK.PhotoImage(file = os.path.dirname(os.path.realpath(__file__))+"\\img\\rdh.png")
        self.iconphoto(False, self.ico)
        self.eval('tk::PlaceWindow . center')
        self.title('RainyDaysHero')
        self.geometry("500x300")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.resizable(0, 0)
        self.configure(bg='#EBF5FB')
        default_font = TK.font.nametofont("TkDefaultFont")
        default_font.configure(size=12)

        #Setup Menu
        MainMenu(self)

        #Setup Frame
        container = TK.Frame(self,bg='#EBF5FB')
        container.grid(row=0, column=0, sticky='WE', padx=10, pady=10)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        self.frames = {}

        for F in (StartFrame, PricingFrame, RetroFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartFrame) 
    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

class StartFrame(TK.Frame):
    def __init__(self, parent, controller):
        TK.Frame.__init__(self, parent)
        self.configure(bg='#EBF5FB')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=7)

        #page title
        welcomeLabel = TK.Label(self,text = "Welcome to RainyDaysHero", fg="#B9770E", font=("Helvetica", 18))
        welcomeLabel.configure(underline = True)
        welcomeLabel.grid(row=0, column=0, columnspan=2, sticky='WENS', ipady=5)

        #image
        self.img = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.realpath(__file__))+"\\img\\covered.png"))
        startPageImg = TK.Label(self,image = self.img)
        startPageImg.grid(row=1, column=0, columnspan=2, sticky='NSEW')


class PricingFrame(TK.Frame):
    def __init__(self, parent, controller):
        TK.Frame.__init__(self, parent)
        self.configure(bg='#EBF5FB')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)

        #Welcome message
        welcomeLabel = TK.Label(self,text = "Welcome to RainyDaysHero", fg="#B9770E", font=("Helvetica", 18))
        welcomeLabel.configure(underline = True)
        welcomeLabel.grid(row=0, column=0, columnspan=2, sticky='WE', ipady=5)

        #client informations
        clientNameLabel = TK.Label(self,text = "Client Name", bg='#EBF5FB')
        self.clientNameEntry = TK.Entry(self)
        clientNameLabel.grid(row=1, column=0, sticky='W')
        self.clientNameEntry.grid(row=1, column=1, sticky='WE')

        turnoverLabel = TK.Label(self,text = "Daily max turnover", bg='#EBF5FB')
        self.turnoverEntry = TK.Entry(self)
        turnoverLabel.grid(row=2, column=0, sticky='W')
        self.turnoverEntry.grid(row=2, column=1, sticky='WE')

        fixedCostsLabel = TK.Label(self,text = "Fixed costs", bg='#EBF5FB')
        self.fixedCostsEntry = TK.Entry(self)
        fixedCostsLabel.grid(row=3, column=0, sticky='W')
        self.fixedCostsEntry.grid(row=3, column=1, sticky='WE')

        rainfallLabel = TK.Label(self,text = "Rainfall", bg='#EBF5FB')
        self.rainfallEntry = TK.Entry(self)
        rainfallLabel.grid(row=4, column=0, sticky='W')
        self.rainfallEntry.grid(row=4, column=1, sticky='WE')

        subscriptionDateLabel = TK.Label(self,text = "Subsciption date", bg='#EBF5FB')
        self.subscriptionDateEntry = DateEntry(self, date_pattern='y-mm-dd', width=12, background='darkblue',foreground='white', borderwidth=2)
        subscriptionDateLabel.grid(row=5, column=0, sticky='W')
        self.subscriptionDateEntry.grid(row=5, column=1, sticky='WE')

        locationLabel = TK.Label(self,text = "Location (City)", bg='#EBF5FB')
        self.locationEntry = TK.ttk.Combobox(self, values=['Paris', 'Nice', 'Nantes'])
        locationLabel.grid(row=6, column=0, sticky='W')
        self.locationEntry.grid(row=6, column=1, sticky='WE')
        self.locationEntry.current(0)

        #price calculation trigger
        calculateButton = TK.Button(self, text="Calculate", command= lambda: calculatePrice(self), bg='#2E86C1', fg='white')
        calculateButton.grid(row=7, column=0, columnspan=2, pady=30)




class RetroFrame(TK.Frame):
    def __init__(self, parent, controller):
        TK.Frame.__init__(self, parent)
        self.configure(bg='#EBF5FB')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)

        #Welcome message
        welcomeLabel = TK.Label(self,text = "Welcome to RainyDaysHero", fg="#B9770E", font=("Helvetica", 18))
        welcomeLabel.configure(underline = True)
        welcomeLabel.grid(row=0, column=0, columnspan=2, sticky='WE', ipady=5)

        #client informations
        clientNameLabel = TK.Label(self,text = "Client Name", bg='#EBF5FB')
        self.clientNameEntry = TK.Entry(self)
        clientNameLabel.grid(row=1, column=0, sticky='W')
        self.clientNameEntry.grid(row=1, column=1, sticky='WE')


        turnoverLabel = TK.Label(self,text = "Daily max turnover", bg='#EBF5FB')
        self.turnoverEntry = TK.Entry(self)
        turnoverLabel.grid(row=2, column=0, sticky='W')
        self.turnoverEntry.grid(row=2, column=1, sticky='WE')

        fixedCostsLabel = TK.Label(self,text = "Fixed costs", bg='#EBF5FB')
        self.fixedCostsEntry = TK.Entry(self)
        fixedCostsLabel.grid(row=3, column=0, sticky='W')
        self.fixedCostsEntry.grid(row=3, column=1, sticky='WE')

        rainfallLabel = TK.Label(self,text = "Rainfall", bg='#EBF5FB')
        self.rainfallEntry = TK.Entry(self)
        rainfallLabel.grid(row=4, column=0, sticky='W')
        self.rainfallEntry.grid(row=4, column=1, sticky='WE')

        retroYearLabel = TK.Label(self,text = "Retrospective Year", bg='#EBF5FB')
        self.retroYearEntry = TK.Entry(self)
        retroYearLabel.grid(row=5, column=0, sticky='W')
        self.retroYearEntry.grid(row=5, column=1, sticky='WE')

        locationLabel = TK.Label(self,text = "Location (City)", bg='#EBF5FB')
        self.locationEntry = TK.ttk.Combobox(self, values=['Paris', 'Nice', 'Nantes'])
        locationLabel.grid(row=6, column=0, sticky='W')
        self.locationEntry.grid(row=6, column=1, sticky='WE')
        self.locationEntry.current(0)

        #retrospective trigger
        computeRetroButton = TK.Button(self, text="Retrospective", command= lambda: computeRetro(self), bg='#2E86C1', fg='white')
        computeRetroButton.grid(row=7, column=0, columnspan=2, pady=30)


class MainMenu:
    def __init__(self, root):
        menubar = TK.Menu(root)
        filemenu = TK.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Start Page",  command=lambda:root.show_frame(StartFrame))
        filemenu.add_command(label="Pricing", command=lambda:root.show_frame(PricingFrame))
        filemenu.add_command(label="Retrospective",  command=lambda:root.show_frame(RetroFrame))
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="Menu", menu=filemenu)
        root.config(menu=menubar)

def main():
    app = App()
    #dataUpdateAllCity()
    app.mainloop()

if __name__== "__main__" :
    main()

