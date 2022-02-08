from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ArabaSatma:
    def __init__(self,master):
        frame = Frame(master)
        frame.grid()

        self.markaList = []
        self.modelList = []
        self.altModelList = []
        self.fiyatList = []
        self.intFiyatList = []
        self.toplamFiyat = 0
        self.ortalamaFiyat = 0
        self.tavsiyeFiyat = 0

        self.yilVar = IntVar()
        self.kmVar = IntVar()
        self.tramerVar = IntVar()

        self.var1 = IntVar()
        self.var2 = IntVar()
        self.var3 = IntVar()

        self.initUI()

    def initUI(self):

        self.markaLabel = Label(text="Araba markası :",height=2)
        self.markaLabel.grid(row=1,column=0)

        self.comboboxMarkalar()
        self.markaComboBox = ttk.Combobox(value=self.markaList)
        self.markaComboBox.current(0)
        self.markaComboBox.grid(row=1,column=1)

        self.markaButton = Button(text="Model ara..",height=1,width=8,command=lambda : self.modelCek(self.markaComboBox.get()))
        self.markaButton.grid(row=1,column=2)

        self.modelButton = Button(text="Alt model ara..", height=1, width=11,command=lambda: self.altModelCek(self.markaComboBox.get(),self.modelComboBox.get()))
        self.modelButton.grid(row=2, column=2)

        self.modelLabel = Label(text="Araba modeli :",height=2)
        self.modelLabel.grid(row=2, column=0)

        self.modelComboBox = ttk.Combobox()
        self.modelComboBox.configure(state="disabled")
        self.modelComboBox.grid(row=2, column=1)

        self.altModelLabel = Label(text="Alt araba modeli :", height=2)
        self.altModelLabel.grid(row=3, column=0)

        self.altModelComboBox = ttk.Combobox()
        self.altModelComboBox.configure(state="disabled")
        self.altModelComboBox.grid(row=3, column=1)

        self.minYilLabel = Label(text="Araba yılı :",height=2)
        self.minYilLabel.grid(row=5,column=0)

        self.minYilEntry = Entry(textvariable=self.yilVar, width=5)
        self.minYilEntry.grid(row=5, column=1, sticky=W)

        self.minKmLabel = Label(text="Kilometre :",height=2)
        self.minKmLabel.grid(row=7, column=0)

        self.minKmEntry = Entry(textvariable = self.kmVar)
        self.minKmEntry.grid(row=7, column=1)

        self.yakitLabel = Label(text="Yakıt tipi :",height=2)
        self.yakitLabel.grid(row=8,column=0,sticky=W)

        self.yakitRb1 = Radiobutton(text="Dizel",value=1,variable=self.var1)
        self.yakitRb1.grid(row=9,column=0,sticky=W)

        self.yakitRb2 = Radiobutton(text="Benzin",value=2,variable=self.var1)
        self.yakitRb2.grid(row=10,column=0,sticky=W)

        self.yakitRb3 = Radiobutton(text="LPG",value=3,variable=self.var1)
        self.yakitRb3.grid(row=11, column=0,sticky=W)

        self.yakitRb4 = Radiobutton(text="Elektrik",value=4,variable=self.var1)
        self.yakitRb4.grid(row=12, column=0,sticky=W)

        self.yakitRb5 = Radiobutton(text="Hybrid", value=5, variable=self.var1)
        self.yakitRb5.grid(row=13, column=0, sticky=W)

        self.tramerLabel = Label(text="Tramer kaydı :",height=2)
        self.tramerLabel.grid(row=9,column=1)

        self.tramerRb1 = Radiobutton(text="Var",value=5,variable=self.var2,command=self.enableEntry)
        self.tramerRb1.grid(row=10,column=1,sticky=N)

        self.tramerRb2 = Radiobutton(text="Yok",value=6,variable=self.var2,command=self.disableEntry)
        self.tramerRb2.grid(row=11,column=1,sticky=N)

        self.tramerEntry = Entry(textvariable = self.tramerVar)
        self.tramerEntry.grid(row=10,column=2,sticky=N)

        self.vitesLabel = Label(text="Vites tipi :",height=2)
        self.vitesLabel.grid(row=14,column=0,sticky=W)

        self.vitesRb1 = Radiobutton(text="Otomatik",value=7,variable=self.var3)
        self.vitesRb1.grid(row=14,column=0,sticky=SW)

        self.vitesRb2 = Radiobutton(text="Manuel",value=8,variable=self.var3)
        self.vitesRb2.grid(row=15,column=0,sticky=NW)

        self.vitesRb3 = Radiobutton(text="Yarı-otomatik", value=9, variable=self.var3)
        self.vitesRb3.grid(row=16, column=0, sticky=NW)

        self.araBut = Button(text="Ara",command=self.arama,height=5,width=10,bg="#20bebe",font="Raleway",fg="white")
        self.araBut.grid(row=14,column=1)

        self.textBox = Text(width=45, height=3)
        self.textBox.place(relx=0, rely=0.95, anchor=W)


    def arama(self):
        link = "https://www.sahibinden.com/"
        yakit = ""
        vites = ""
        if (" " in self.markaComboBox.get()):
            marka = self.markaComboBox.get().replace(" ", "-")
        else:
            marka = self.markaComboBox.get()

        if (" " in self.modelComboBox.get()):
            model = self.modelComboBox.get().replace(" ", "-")
        else:
            model = self.modelComboBox.get()

        if (" " in self.altModelComboBox.get()):
            altModel = self.altModelComboBox.get().replace(" ", "-")
        else:
            altModel = self.altModelComboBox.get()

        if (self.var1.get() == 1):
            yakit = "dizel"
        elif (self.var1.get() == 2):
            yakit = "benzin"
        elif (self.var1.get() == 3):
            yakit = "lpg"
        elif (self.var1.get() == 4):
            yakit = "elektrik"
        elif (self.var1.get() == 5):
            yakit = "hybrid"

        if (self.var3.get() == 7):
            vites = "otomatik"
        elif (self.var3.get() == 8):
            vites = "manuel"
        elif (self.var3.get() == 9):
            vites = "yari-otomatik"

        link = link + marka.lower() + "-" + model.lower() + "-" + altModel.lower() + "/" + yakit + "/" + vites + "?a4_min=" + str(self.kmVar.get()) + "&a5_min=" + str(self.yilVar.get())
        self.fiyatCek(link)

    def enableEntry(self):
        self.tramerEntry.configure(state="normal")
        self.tramerEntry.update()

    def disableEntry(self):
        self.tramerEntry.configure(state="disabled")
        self.tramerEntry.update()

    def comboboxMarkalar(self):
        PATH = r"C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        driver.get("https://www.sahibinden.com/otomobil")
        sourceCode = driver.page_source

        soup = BeautifulSoup(sourceCode, "html.parser")

        gelen_veri = soup.find_all("div", attrs={"class": "jspPane"})
        for marka in gelen_veri[0].find_all("a"):
            self.markaList.append(marka.get("title"))
        driver.quit()


    def modelCek(self,marka):
        self.modelList = []
        if (" " in marka):
            marka = marka.replace(" ", "-")

        PATH = r"C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)

        link = "https://www.sahibinden.com/" + marka.lower()
        driver.get(link)
        sourceCode = driver.page_source
        soup = BeautifulSoup(sourceCode, "html.parser")
        gelen_veri = soup.find_all("div", attrs={"class": "jspPane"})
        for model in gelen_veri[1].find_all("a"):
            self.modelList.append(model.get("title"))
        driver.quit()
        self.modelComboBox.configure(state="normal")
        self.modelComboBox['values'] = self.modelList
        self.modelComboBox.update()

    def altModelCek(self, marka,model):
        self.modelList = []
        if (" " in marka):
            marka = marka.replace(" ", "-")
        if (" " in model):
            model = model.replace(" ","-")

        PATH = r"C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)

        link = "https://www.sahibinden.com/" + marka.lower() + "-" + model.lower()
        driver.get(link)
        sourceCode = driver.page_source
        soup = BeautifulSoup(sourceCode, "html.parser")
        gelen_veri = soup.find_all("div", attrs={"class": "jspPane"})
        for model in gelen_veri[1].find_all("a"):
            self.altModelList.append(model.get("title"))
        driver.quit()
        self.altModelComboBox.configure(state="normal")
        self.altModelComboBox['values'] = self.altModelList
        self.altModelComboBox.update()

    def sayfaDolas(self,link):
        linkList = []
        PATH = r"C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        driver.get(link)
        sourceCode = driver.page_source

        soup = BeautifulSoup(sourceCode, "html.parser")

        gelen_veri = soup.find_all("div", attrs={"class": "pageNavTable"})

        for i in gelen_veri[0].find_all("a"):
            linkList.append(i.get("href"))
        driver.quit()
        return linkList

    def fiyatCek(self,link):
        linkList = self.sayfaDolas(link)
        anaLink = "https://www.sahibinden.com"
        self.textBox.delete(1.0,END)
        self.fiyatList = []
        PATH = r"C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        for sayfa in linkList:
            driver.get(anaLink+sayfa)
            sourceCode = driver.page_source

            soup = BeautifulSoup(sourceCode, "html.parser")

            gelen_veri = soup.find_all("td", attrs={"class": "searchResultsPriceValue"})

            for i in gelen_veri:
                for j in i.find_all("div"):
                    self.fiyatList.append(j.decode_contents())

            self.intFiyatList = []

            for e in self.fiyatList:
                e = e.replace('.', '')
                e = e.replace(',', '')
                e = e.replace(' TL', '')
                e = e.replace(' ', '')
                self.intFiyatList.append(e)

        for i in range(0, len(self.intFiyatList)):
            self.intFiyatList[i] = int(self.intFiyatList[i])

        self.toplamFiyat = 0
        self.ortalamaFiyat = 0
        self.tavsiyeFiyat = 0

        for i in self.intFiyatList:
            self.toplamFiyat = self.toplamFiyat + i

        self.ortalamaFiyat = self.toplamFiyat // len(self.intFiyatList)

        if (self.var2.get() == 5):
            self.tavsiyeFiyat = self.ortalamaFiyat - (20*(self.tramerVar.get())//100)
            self.textBox.insert("end","Aracınızı ")
            self.textBox.insert("end",self.tavsiyeFiyat)
            self.textBox.insert("end"," TL den satabilirsiniz..")

        elif (self.var2.get() == 6):
            self.textBox.insert("end","Aracınızı ")
            self.textBox.insert("end",self.ortalamaFiyat)
            self.textBox.insert("end"," TL den satabilirsiniz..")

master = Tk()
b=ArabaSatma(master)
master.geometry("400x600")
master.title("Araç Fiyatı Hesaplama Programi")
master.mainloop()