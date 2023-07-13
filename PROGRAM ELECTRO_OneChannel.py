import pyvisa as visa
import time
import serial
import tkinter as tk
from tkinter import *
from tkinter import simpledialog
from tkinter import scrolledtext
from tkinter import ttk

# Change value to run program, =1 to connect devices and =0 without devices 
rs485   = 1
comPort = 'com3'
GPIB    = 1

if GPIB == 1 :
    #Stanford PS530
    xx = "GPIB0::16::INSTR"
    ressourceManager = visa.ResourceManager() #utilises un nommage long, on s'en fout ça permet de mieux lire le code, ressourcesManager au lieu de rm, au passage rm veut dire remove en anglais
    ressourceList = ressourceManager.list_resources()
    generator = ressourceManager.open_resource(xx) #stock generator connection
    print("START, Find following resources: ", ressourceList)
    print("Opening ressource" + ressourceList[0])
    print(generator , "opened")

if rs485 == 1:
    #Modbus Serial
    ser = serial.Serial('com3',10067,timeout=0.1,bytesize=8, parity='N',stopbits=1)
    timeSleepRelay = 0.032
    print(ser, "opened")

#Definition des valeurs initiales
voltage = 0
TryVoltage = 0
IntervalTime = 0
HVvoltage = 0
LVvoltage = 0
HVduration = 0
LVduration = 0
HVintevalTime = 0
LVintevalTime = 0
Pulse_count = 0
LV_pulse_count = 0
HV_pulse_count = 0
entry_voltage = 0
entry_TryVoltage = 0
entry_LVvoltage = 0
entry_HVvoltage = 0
entry_ChargingTime = 0.5
entry_TimeBetweenPulse = 1
Totaltime = entry_TimeBetweenPulse + entry_ChargingTime

def rs485Write(data):
    if rs485 == 1:
        ser.write(bytes.fromhex(data))

def GeneratorReset():
    generator.write("*RST")
def GeneratorOn():
    generator.write("HVON")
def GeneratorOff():
    generator.write("HVOF")
def setVoltage():
    global voltage
    voltage = float(entry_voltage.get())
    voltageC = 0.8587*float(entry_voltage.get())
    generator.write(f"VSET {voltage}")
    print(f"Tension set to {voltage:.2f} V on generator, OUTPUT = {voltageC:.2f}")
    print("Due to RC circuit resistance, the OUTPUT voltage will be reduce. (0.8587*x)_ x= Current (V) input")

#ch1_0 = Transfect = 0
def ch1_0():
    relay  = "33 05 00 00 00 00 C9 D8"
    ser.write(bytes.fromhex(relay))
    print("Ch1 = 0 = Transfect")
#ch1_1 = Monitoring = 1
def ch1_1():
    relay  = "33 05 00 00 ff 00 88 28"
    ser.write(bytes.fromhex(relay))
    print("Ch1 = 1 = Impedance monitoring")
#ch2_0 = Charge = 0
def ch2_0():
    relay  = "33 05 00 01 00 00 98 18" 
    rs485Write(relay)
    print("Ch2 = 0 = Charge")
#ch2_1 = Discharge = 1
def ch2_1():
    relay  = "33 05 00 01 ff 00 D9 E8"
    rs485Write(relay)
    print("Ch2 = 1 = Discharge")

def chConfigEp():
    ch2_0()
    time.sleep(timeSleepRelay)
    ch1_0()
    print("Relay channels set to Charge condensator and directed to sample (Transfect)")
def chConfigImp():
    ch1_1()
    time.sleep(timeSleepRelay)
    ch2_1()
    print("Relay channels set to Monitoring and Discharge")



def GeneratorPulse():
    Gvoltage = float(entry_GeneratorPulseVoltage.get())
    Gduration = float(entry_GeneratorPulseDuration.get())
    Gintervalle= float(entry_GeneratorPulseInterval.get())
    Gtime = float(entry_GeneratorPulsetime.get())
    print ("Generator will pulse :",Gtime,"times", Gvoltage, "V during", Gduration, ",","with",Gintervalle," sec between pulses" )
def GeneratorPulseProgram():
    generator.write('VSET {}'.format(Gvoltage)) #Set voltage to generator
    for i in range(Gtime): 
            print (i) 
            generator.write('HVON') #start generator
            print ("Lancement du générateur...")
            time.sleep(Gduration)
            generator.write('HVOF')
            time.sleep(Gintervalle)    
    generator.write("*RST") #reset generator
    print("Generator OFF et RESET")    
    print("Fin du programme")

def MultiplePulseTimeConfig ():
    global ChargingTime
    global TimeBetweenPulse
    global Totaltime
    ChargingTime = float(entry_ChargingTime.get())
    TimeBetweenPulse = float(entry_TimeBetweenPulse.get())- ChargingTime
    Totaltime = ChargingTime + TimeBetweenPulse
    print(f"The program will be charge the condensator during : ", ChargingTime," seconds","to generate pulses each",Totaltime,"secondes. Please the minimum entry values should be superior at 0.032 sec")
    print (TimeBetweenPulse) 
def SetTryVoltage():
    global TryVoltage
    TryVoltage = float(entry_TryVoltage.get())
    print(f"Tension set to {TryVoltage:.2f} V on generator")


def WaitingTime():
    WaitingTimeDay = int(entry_timeDay.get())
    WaitingTimeMin = int(entry_timeMin.get())
    WaitingTimeSec = int(entry_timeSec.get())
    WaintingTimeSet = WaitingTimeDay * 24 * 60 * 60 + WaitingTimeMin * 60 + WaitingTimeSec
    print("Waiting time before Single Pulse program :", WaintingTimeSet, "secondes")
    return WaintingTimeSet

def WaitingTimeEP():
    WaitingTimeDayEP = int(entry_timeDayEP.get())
    WaitingTimeMinEP = int(entry_timeMinEP.get())
    WaitingTimeSecEP = int(entry_timeSecEP.get())
    WaintingTimeSetEP = WaitingTimeDayEP * 24 * 60 * 60 + WaitingTimeMinEP * 60 + WaitingTimeSecEP
    print("Waiting time before EP :", WaintingTimeSetEP, "secondes")
    return WaintingTimeSetEP

def setHVvoltage():
    global HVvoltage
    HVvoltage = float(entry_HVvoltage.get())
    HVvoltageC = 0.8587*float(entry_HVvoltage.get())
    print(f"HV pulse : Tension set to {HVvoltage:.2f} V on generator, OUTPUT = {HVvoltageC:.2f}")
def setLVvoltage():
    global LVvoltage
    LVvoltage = float(entry_LVvoltage.get())
    LVvoltageC = 0.8587*float(entry_LVvoltage.get())
    print(f"LV pulse : Tension set to {LVvoltage:.2f} V on generator, OUTPUT = {LVvoltageC:.2f} ")
    
def setHVduration():
    global HVduration
    HVduration = str(entry_HVduration.get())
    print(f"HV pulse duration : ", HVduration," seconds")
def setLVduration():
    global LVduration
    LVduration = str(entry_LVduration.get())
    print("LV pulse duration : ", LVduration , "seconds")
def setHVintervalTime():
    global HVintervalTime
    HVintervalTime = str(entry_HVintervalTime.get())
    print("Waiting time after HV pulse :" , HVintervalTime, "seconds")
def setLVintervalTime():
    global LVintervalTime
    LVintervalTime = str(entry_LVintervalTime.get())
    print("Waiting time between LV pulse :", LVintervalTime, "seconds")

def setPulseCount():
    global Pulse_count
    Pulse_count = int(entry_Pulse_count.get())
    print("Program will proceed to", Pulse_count," pulses")
def setHVpulseCount():
    global HV_pulse_count
    HV_pulse_count = int(entry_HV_pulse_count.get())
    print("Program will proceed to", HV_pulse_count," pulses")
def setLVpulseCount():
    global LV_pulse_count
    LV_pulse_count = int(entry_LV_pulse_count.get())
    print("Program will proceed to", LV_pulse_count," pulses")

            



def MultiplePulsesProgram ():
    WaitingTimeSet = WaitingTime()
    print("The program will be launch in", WaitingTimeSet,"seconds" )
    time.sleep(WaitingTimeSet)
    print("Beginnig of Multiple Pulse program for",Pulse_count," pulses" )
    print ("Launching Program :", TryVoltage, "V, separated by", Totaltime,"s")
    generator.write('VSET {}'.format(TryVoltage))
    generator.write('HVON') #start generator
    ch1_0 () 
    time.sleep(timeSleepRelay)
    ch2_0()   # charge of capacitor
    time.sleep(3)##attendre 3sec que le générateur charge
    print ("Beginning of pulses")
    for Pulse_number in range(int(Pulse_count)):
        ch1_1()   # charge 
        print ("Charge")
        time.sleep(ChargingTime)
        ch1_0() # Discharge
        time.sleep(TimeBetweenPulse)
        print ("Discharge : Pulse", Pulse_number+1, "at", TryVoltage, "V")
    print ("End of cycle of",Pulse_count,"pulses")
    ch1_1()
    print("Sample ready for impedance measurement")
    ch2_1()
    print ("Discharge of condensator by short circuiting")
    generator.write('HVOF')
    generator.write("*RST") #reset generator
    print("Generator OFF et RESET")    
    print("End of program")

def LaunchProgram ():
    WaitingTimeSetEP = WaitingTimeEP()
    print("The program will be launch in", WaitingTimeSetEP,"seconds" )
    time.sleep(WaitingTimeSetEP)
    print("Beginnig of EP program...")
    chAllOpen()
    generator.write('VSET {}'.format(HVvoltage)) #Set voltage HV to generator
    generator.write('HVON') #start generator
    print(HVvoltage)
    print ("Charging generator")
    time.sleep(2)##attendre 2sec que le générateur charge
     ch1_1()
    print ("Charging capacitor to",HVvoltage,"V")
    time.sleep(2)#chargement du condensateur
    start_HVtime = time.time()
    ch2_1()#First pulse
    voltageHV = float(generator.query('VOUT?'))
    print ("HV pulse start")
    ##  time.sleep(HVduration)  Time for HV pulse but limited by relay
    time.sleep(timeSleepRelay)#############################
    ch2_0()
    end_HVtime = time.time()
    start_HVintervaleTime = time.time()
    print ("HV pulse end")
    # pour dechargé le condensateur  plus rapidement (car il est toujours à HV)
    # on peut le court circuiter. Comme ça il retombe à 0V le temps que le générateur
    # se décharge à LV. 
    startDecrease_time = time.time()
    generator.write('VSET {}'.format(LVvoltage))
    while True:
        voltageBeforePulse = float(generator.query('VSET?')) ##j'ai remplacé VOUT? par VSET? car il bug trop #Get current voltage of the generator
        if voltageBeforePulse <= LVvoltage :
            print(voltageBeforePulse , "V (voltageBeforePulse)")
            endDecrease_time = time.time()
            break #le break te fait sortir de la boucle While, ce qui fait que tu ne l'exécutes qu'une seule fois, en ajoutant une tabulation le break n'est exécuté que si le voltage est supérieur à 360V #Ben
    ### Il faudra certainement retirer ce While 
    time.sleep(float(HVintervalTime))## Should be superior to 0.032sec (relay)
    end_HVintervaleTime = time.time()
    for LV_pulse_number in range(int(LV_pulse_count)):
        voltagePulse = float(generator.query('VOUT?'))
        print ("Chargement du condensateur à",voltagePulse, " V(voltagePulse), Pulse n°",LV_pulse_number+1)
        #Lancement du LV pulse 
        ch2_1() 
        start_LVpulseDuration = time.time()
        time.sleep(float(LVduration))# Should be superior to 0.032sec (relay)
        #time.sleep(timeSleepRelay)#############################
        ch2_0() #Before it was ch1_0 but now the voltage decrease directly (Square wave)
        end_LVpulseDuration = time.time()
        # Attente de X ms avant de générer la prochaine impulsion
        LVpulseDuration = end_LVpulseDuration - start_LVpulseDuration
        print('Time elapsed :', LVpulseDuration, " sec. during the pulse" , LV_pulse_number+1, "at" , voltagePulse, "V")
        start_LVpulseIntervale = time.time()
        #time.sleep(timeSleepRelay)#############################
        time.sleep(float(LVintervalTime)) # Should be superior to 0.032sec (relay)
        end_LVpulseIntervale = time.time()
        LVpulseIntervale = end_LVpulseIntervale - start_LVpulseIntervale
        print('Time elapsed :', LVpulseIntervale, "sec. before next pulse")
    print("End of EP program")
    generator.write('HVOF')
    generator.write("*RST") #reset generator
    print("Generator OFF et RESET")
    chAllOpen()
    HVtime = end_HVtime - start_HVtime
    print('Time elapsed :', HVtime, "seconds to perfom HV pulse at",voltageHV, " V")
    decreaseDecrease_time = endDecrease_time - startDecrease_time
    print('Time elapsed :', decreaseDecrease_time, "seconds to reach",voltageBeforePulse, " V(voltageBeforePulse)")
    HVintervaleTime = end_HVintervaleTime-start_HVintervaleTime
    print('Time elapsed :', HVintervaleTime, "seconds between HV pulse end and the loop beginning")

def on_hover(event):
    tooltip = CreateToolTip(event.widget, event.widget.tooltip_text)
def on_leave(event):
    tooltip.destroy()
def help_callback():
    # Crée une nouvelle fenêtre
    help_window = tk.Toplevel(root)
    # Crée un widget ScrolledText
    text = scrolledtext.ScrolledText(help_window, width=130, height=20)
    text.pack()
    # Ouvre le fichier d'aide et insère son contenu dans le widget Text
    with open('HelpElectroporation.txt', 'r') as help_file:
        text.insert('1.0', help_file.read())

class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.waittime = 1     # délai en ms avant d'afficher la tooltip
        self.wraplength = 180   # nombre de pixels avant le retour à la ligne de la tooltip
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hide()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.show)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def show(self, event=None):
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 0
        y += self.widget.winfo_rooty() + 30
        self.tw = tk.Toplevel(self.widget)
        self.tw.attributes('-topmost', True)
        self.tw.geometry("+%d+%d" % (x, y))
                         
        # Affichage du calcul des tensions
        voltageC = 0.8587*float(entry_voltage.get())
        label = tk.Label(self.tw, text=f"Tension set to {voltageC:.2f} V in output", justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)
        TryVoltageC = 0.8587*float(entry_TryVoltage.get())
        label = tk.Label(self.tw, text=f"Tension set to {TryVoltageC:.2f} V in output", justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)
        HVvoltageC = 0.8587*float(entry_HVvoltage.get())
        label = tk.Label(self.tw, text=f"HV pulse : Tension set to {HVvoltageC:.2f} V", justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)
        LVvoltageC = 0.8587*float(entry_LVvoltage.get())
        label = tk.Label(self.tw, text=f"LV pulse : Tension set to {LVvoltageC:.2f} V", justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hide(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()





root = tk.Tk()
root.title("Electroporator Window")
root.wm_geometry("800x650")



# Frame pour les boutons de contrôle du générateur
frame1 = tk.Frame(root)
bt_Resest = tk.Button(frame1,text="Reset",command=GeneratorReset,bg="orange").pack(side=tk.LEFT)
bt_Start = tk.Button(frame1,text="Start",command=GeneratorOn,bg="orange").pack(side=tk.LEFT)
bt_Stop = tk.Button(frame1,text="Stop",command=GeneratorOff,bg="orange").pack(side=tk.LEFT)
bt_Help = tk.Button(frame1, text="Help", command=help_callback).pack(side=tk.LEFT, padx=320)
frame1.pack(side=tk.TOP, anchor=tk.W, padx=10)

frame5 = tk.Frame(root)
label_voltage = tk.Label(frame5, text="Voltage (V): ").pack(side=tk.LEFT)
entry_voltage = tk.Entry(frame5, width=10)
entry_voltage.pack(side=tk.LEFT)
entry_voltage.insert(0,"0")
bt_set_voltage = tk.Button(frame5,text="Set Voltage",command=setVoltage,bg="orange")
bt_set_voltage.pack(side=tk.LEFT)
#CreateToolTip(bt_set_voltage, "Due to the system resistance : ")
                    
frame5.pack(side=tk.TOP, anchor=tk.W, padx=80, pady=20)

# Frame pour les boutons de contrôle des relais
frame2 = tk.Frame(root)
btCh1 = tk.Button(frame2,text="Transfect",command=ch1_0,bg="orange").pack(side=tk.LEFT)
btCh2 = tk.Button(frame2,text="Monitoring",command=ch1_1,bg="orange").pack(side=tk.LEFT)
btCh3 = tk.Button(frame2,text="Charge",command=ch2_0,bg="orange").pack(side=tk.LEFT)
btCh4 = tk.Button(frame2,text="Disharge",command=ch2_1,bg="orange").pack(side=tk.LEFT)

space_label = tk.Label(frame2, width=10).pack(side=tk.LEFT)

space_label = tk.Label(frame2, width=10).pack(side=tk.LEFT)
btCh6 = tk.Button(frame2,text="Channels config for Ep",command=chConfigEp,bg="orange").pack(side=tk.LEFT)
btCh5 = tk.Button(frame2,text="Channels config for Imp",command=chConfigImp,bg="orange").pack(side=tk.LEFT)


frame2.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
separator = tk.Canvas(root, width=400, height=2, bg='black')
separator.create_line(0, 1, 400, 1, fill='white', width=2)

# placement de la ligne de séparation dans le haut de la fenêtre
separator.place(in_=frame2, relx=0.7, rely=1.5, anchor='e')

frame12 = tk.Frame(root)
label_GeneratorPulseVoltage = tk.Label(frame12, text="Voltage(V): ").pack(side=tk.LEFT)
entry_GeneratorPulseVoltage = tk.Entry(frame12, width=10)
entry_GeneratorPulseVoltage.pack(side=tk.LEFT)
entry_GeneratorPulseVoltage.insert(0, "0")


label_GeneratorPulseDuration = tk.Label(frame12, text="Pulse duration(Sec) : ").pack(side=tk.LEFT)
entry_GeneratorPulseDuration = tk.Entry(frame12, width=10)
entry_GeneratorPulseDuration.pack(side=tk.LEFT)
entry_GeneratorPulseDuration.insert(0, "0")


label_GeneratorPulseInterval = tk.Label(frame12, text="Interval(Sec): ").pack(side=tk.LEFT)
entry_GeneratorPulseInterval = tk.Entry(frame12, width=10)
entry_GeneratorPulseInterval.pack(side=tk.LEFT)
entry_GeneratorPulseInterval.insert(0, "0")


label_GeneratorPulsetime = tk.Label(frame12, text="Duration(Sec): ").pack(side=tk.LEFT)
entry_GeneratorPulsetime = tk.Entry(frame12, width=10)
entry_GeneratorPulsetime.pack(side=tk.LEFT)
entry_GeneratorPulsetime.insert(0, "0")

bt_GeneratorPulseParameter = tk.Button(frame12,text="Set Parameters",command=GeneratorPulse,bg="orange").pack(side=tk.LEFT)
bt_GeneratorPulseProgram = tk.Button(frame12,text="Launch Pulses",command=GeneratorPulseProgram,bg="orange").pack(side=tk.LEFT,anchor=tk.W)

frame12.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
separator = tk.Canvas(root, width=400, height=2, bg='black')
separator.create_line(0, 1, 400, 1, fill='white', width=2)

# placement de la ligne de séparation dans le haut de la fenêtre
separator.place(in_=frame12, relx=0.6, rely=1.5, anchor='e')

#Frame for Multiple pulses generation

frame11 = tk.Frame(root)
label_time = tk.Label(frame11, text="Waiting time before Multiple Pulses program : ").pack(side=tk.LEFT)
entry_timeDay = tk.Entry(frame11, width=10)
entry_timeDay.pack(side=tk.LEFT)
entry_timeDay.insert(0, "0")
label_time = tk.Label(frame11, text="Days").pack(side=tk.LEFT)

entry_timeMin = tk.Entry(frame11, width=10)
entry_timeMin.pack(side=tk.LEFT)
entry_timeMin.insert(0, "0")
label_time = tk.Label(frame11, text="Minutes").pack(side=tk.LEFT)

entry_timeSec = tk.Entry(frame11, width=10)
entry_timeSec.pack(side=tk.LEFT)
entry_timeSec.insert(0, "0")
label_time = tk.Label(frame11, text="Secondes").pack(side=tk.LEFT)

btWaitingTime = tk.Button(frame11,text="Set time",command=WaitingTime,bg="orange").pack(side=tk.LEFT)
frame11.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

frame9 = tk.Frame(root)
label_TryVoltage = tk.Label(frame9, text="Voltage (V): ").pack(side=tk.LEFT)
entry_TryVoltage = tk.Entry(frame9, width=10)
entry_TryVoltage.pack(side=tk.LEFT)
entry_TryVoltage.insert(0,"0")
bt_set_TryVoltage = tk.Button(frame9,text="Set Voltage",command=SetTryVoltage,bg="orange")
bt_set_TryVoltage.pack(side=tk.LEFT)
entry_Pulse_count = tk.Entry(frame9, width=10)
entry_Pulse_count.pack(side=tk.LEFT)
entry_Pulse_count.insert(0,"0")
bt_Pulse_count = tk.Button(frame9, text="Set pulses number",command=setPulseCount,bg="orange").pack(side=tk.LEFT)
frame9.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

frame13 = tk.Frame(root)
label_ChargingTime = tk.Label(frame13, text="Charging time (Sec): ").pack(side=tk.LEFT)
entry_ChargingTime = tk.Entry(frame13, width=10)
entry_ChargingTime.pack(side=tk.LEFT)
entry_ChargingTime.insert(0,"0.5")
label_TimeBetweenPulse = tk.Label(frame13, text="Time between pulses (Sec): ").pack(side=tk.LEFT)
entry_TimeBetweenPulse = tk.Entry(frame13, width=10)
entry_TimeBetweenPulse.pack(side=tk.LEFT)
entry_TimeBetweenPulse.insert(0,"1")
bt_set_MultiplepulseTime = tk.Button(frame13,text="Set times",command=MultiplePulseTimeConfig,bg="orange")
bt_set_MultiplepulseTime.pack(side=tk.LEFT)
frame13.pack(side=tk.TOP,anchor=tk.W, padx=10, pady=10)
#Frame pour le bouton launch 
frame10 = tk.Frame(root)
bt_SinglePulseProgram = tk.Button(frame10,text="Launch Multiple Pulses program",command=MultiplePulsesProgram,bg="orange").pack(side=tk.LEFT)                    
frame10.pack(side=tk.TOP, anchor=tk.W, padx=80, pady=10)

separator = tk.Canvas(root, width=400, height=2, bg='black')
separator.create_line(0, 1, 400, 1, fill='white', width=2)
# placement de la ligne de séparation dans le haut de la fenêtre
separator.place(in_=frame10, relx=1, rely=1.5, anchor='center')

#Frame for HV et LV setting 
frame3 = tk.Frame(root)
label_voltage = tk.Label(frame3, text="Voltage (V): ").pack(side=tk.LEFT)

entry_HVvoltage = tk.Entry(frame3, width=10)
entry_HVvoltage.pack(side=tk.LEFT)
entry_HVvoltage.insert(0,"0")
bt_setHVvoltage = tk.Button(frame3, text="Set HV Voltage", command=setHVvoltage, bg="orange")
bt_setHVvoltage.pack(side=tk.LEFT)
#CreateToolTip(bt_setHVvoltage, " Due to the system resistance : ")

entry_LVvoltage = tk.Entry(frame3, width=10)
entry_LVvoltage.pack(side=tk.LEFT)
entry_LVvoltage.insert(0,"0")
bt_setLVvoltage = tk.Button(frame3,text="Set LV Voltage",command=setLVvoltage,bg="orange")
bt_setLVvoltage.pack(side=tk.LEFT)
#CreateToolTip(bt_setLVvoltage, "Due to the system resistance : ")

frame3.pack(side=tk.TOP,anchor=tk.W, padx=10, pady=10)


#Frame pour duration setting
frame4 = tk.Frame(root)
label_Duration = tk.Label(frame4, text="Duration (Sec): ").pack(side=tk.LEFT)

entry_HVduration = tk.Entry(frame4, width=10)
entry_HVduration.pack(side=tk.LEFT)
entry_HVduration.insert(0,"0")
bt_HVduration = tk.Button(frame4,text="Set HV Duration",command=setHVduration,bg="orange").pack(side=tk.LEFT)

entry_LVduration = tk.Entry(frame4, width=10)
entry_LVduration.pack(side=tk.LEFT)
entry_LVduration.insert(0,"0")
bt_LVduration = tk.Button(frame4,text="Set LV Duration",command=setLVduration,bg="orange").pack(side=tk.LEFT)
frame4.pack(side=tk.TOP,anchor=tk.W, padx=10, pady=10)

#Frame for intervalle duration setting
frame6 = tk.Frame(root)
label_IntervalDuration = tk.Label(frame6, text="Interval Duration (Sec): ").pack(side=tk.LEFT)

entry_HVintervalTime = tk.Entry(frame6, width=10)
entry_HVintervalTime.pack(side=tk.LEFT)
entry_HVintervalTime.insert(0,"0")
bt_HVintervalTime = tk.Button(frame6,text="Set HV Interval Duration",command=setHVintervalTime,bg="orange").pack(side=tk.LEFT)

entry_LVintervalTime = tk.Entry(frame6, width=10)
entry_LVintervalTime.pack(side=tk.LEFT)
entry_LVintervalTime.insert(0,"0")
bt_LVintervalTime = tk.Button(frame6,text="Set LV Interval Duration",command=setLVintervalTime,bg="orange").pack(side=tk.LEFT)
frame6.pack(side=tk.TOP,anchor=tk.W, padx=10, pady=10)

#Frame for number of LV pulse 
frame7 = tk.Frame(root)
entry_HV_pulse_count = tk.Entry(frame7, width=10)
entry_HV_pulse_count.pack(side=tk.LEFT)
entry_HV_pulse_count.insert(0,"0")
bt_HV_pulse_count = tk.Button(frame7,text="Set HV pulses number",command=setHVpulseCount,bg="orange").pack(side=tk.LEFT)

entry_LV_pulse_count = tk.Entry(frame7, width=10)
entry_LV_pulse_count.pack(side=tk.LEFT)
entry_LV_pulse_count.insert(0,"0")
bt_LV_pulse_count = tk.Button(frame7,text="Set LV pulses number",command=setLVpulseCount,bg="orange").pack(side=tk.LEFT)
frame7.pack(side=tk.TOP,anchor=tk.W, padx=10, pady=10)

# Ajouter une entrée pour le temps d'attente
frame8 = tk.Frame(root)
label_time = tk.Label(frame8, text="Waiting time before launch EP : ").pack(side=tk.LEFT)
entry_timeDayEP = tk.Entry(frame8, width=10)
entry_timeDayEP.pack(side=tk.LEFT)
entry_timeDayEP.insert(0, "0")
label_time = tk.Label(frame8, text="Days").pack(side=tk.LEFT)

entry_timeMinEP = tk.Entry(frame8, width=10)
entry_timeMinEP.pack(side=tk.LEFT)
entry_timeMinEP.insert(0, "0")
label_time = tk.Label(frame8, text="Minutes").pack(side=tk.LEFT)

entry_timeSecEP = tk.Entry(frame8, width=10)
entry_timeSecEP.pack(side=tk.LEFT)
entry_timeSecEP.insert(0, "0")
label_time = tk.Label(frame8, text="Secondes").pack(side=tk.LEFT)


btWaitingTimeEP = tk.Button(frame8,text="Set time",command=WaitingTimeEP,bg="orange").pack(side=tk.LEFT)
frame8.pack(side=tk.TOP,anchor=tk.W, padx=10, pady=5)

#Bouton launch program
frame10 = tk.Frame(root)
bt_LaunchProgram = tk.Button(frame10,text="Launch Electroporation Program",command=LaunchProgram,bg="orange").pack(side=tk.LEFT)
frame10.pack(side=tk.TOP,anchor=tk.W, padx=10, pady=5)



root.mainloop()



