import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import serial
import serial.tools.list_ports


class InductorPanel:
    inductorFrame = []
    label = []
    onButton = []
    offButton = []
    onMsg = ""
    offMsg = ""
    labelName = ""
    name = ""
    onColor = "green"
    offColor = "red"
    number = 0
    elementPanel = []
    onButtonName = ""
    offButtonName = ""
    app = []
    status = False

    def GetCommand(self, msg):
        if msg == "On":

            try:
                self.app.serial.write(bytes(self.onMsg.encode()))
                self.label.config(background=self.onColor)
                self.onButton.config(state="disable")
                self.offButton.config(state="active")
                self.status = True
            except Exception as error:
                messagebox.showinfo("Error", error)
                self.app.TerminateConnectionAndInitMainWindow()

        elif msg == "Off":

            try:
                self.app.serial.write(bytes(self.offMsg.encode()))
                self.label.config(background=self.offColor)
                self.offButton.config(state="disable")
                self.onButton.config(state="active")
                self.status = False
            except Exception as error:
                messagebox.showinfo("Error", error)
                self.app.TerminateConnectionAndInitMainWindow()

    def __init__(self, number, elementFrame, app):
        self.inductorFrame = tk.Frame(elementFrame, background="red", height=190, width=160)
        self.inductorFrame.pack(side=tk.LEFT, padx=5, pady=10)
        self.app = app
        self.number = number
        self.onMsg = '{}{}{}'.format("Inductor", self.number, "On")
        self.offMsg = '{}{}{}'.format("Inductor", self.number, "Off")
        self.labelName = '{}{}{}'.format("Inductor", " ", self.number)
        self.name = self.labelName
        self.onButtonName = '{}{}{}'.format("Turn On", " ", self.name)
        self.offButtonName = '{}{}{}'.format("Turn Off", " ", self.name)

        self.label = tk.Label(self.inductorFrame, text=self.labelName, background=self.offColor, height=7, width=22)
        self.label.place(x=0, y=0)
        self.onButton = tk.Button(self.inductorFrame, text=self.onButtonName, width=22, height=2,
                                  command=lambda: self.GetCommand("On"))
        self.onButton.place(x=0, y=110)
        self.offButton = tk.Button(self.inductorFrame, text=self.offButtonName, width=22, height=2,
                                   command=lambda: self.GetCommand("Off"))
        self.offButton.place(x=0, y=150)


class MainApplication(tk.Frame):
    mainFrame = []
    comPortInterface = []
    labelComPort = []
    comportCombo = []
    connectButton = []
    disConnectButton = []
    refreshButton = []
    labelMultipleSelection = []
    entryMultiple = []
    multipleSelectionButtonOn = []
    multipleSelectionButtonOff = []
    elementFrame = []
    serial = []
    nInductor = 7
    inductors = [None] * nInductor
    ports = [None]
    multipleInductorIndex = [0] * nInductor
    errorMsg = ""
    multipleInputError = False

    def TerminateConnectionAndInitMainWindow(self):
        self.serial.close()
        self.connectButton.config(state="active")
        self.refreshButton.config(state="active")
        self.comportCombo.config(state="normal")
        self.disConnectButton.config(state="disable")
        self.multipleSelectionButtonOn.config(state="disable")
        self.labelMultipleSelection.config(state="disable")
        self.multipleSelectionButtonOff.config(state="disable")
        self.entryMultiple.delete(0, 'end')
        self.DisableElementPanel()
        self.ports = []
        self.comportCombo.config(values=self.ports)
        self.comportCombo.set('')
        self.ports = [str(ports).split(" ")[0] for ports in serial.tools.list_ports.comports(include_links=False)]
        if not self.ports:
            messagebox.showinfo("Error", "No Device Found")
            self.connectButton.config(state="disable")
        else:
            self.comportCombo.config(values=self.ports)
            self.comportCombo.set(self.ports[0])

    def DisableElementPanel(self):
        for inductor in self.inductors:
            inductor.onButton.config(state="disable")
            inductor.offButton.config(state="disable")
            inductor.label.config(background=inductor.offColor)
            inductor.label.config(state="disable")
            inductor.status = False

    def InitElementPanel(self):
        for inductor in self.inductors:
            inductor.onButton.config(state="active")
            inductor.offButton.config(state="disable")
            inductor.label.config(state="normal")

    def LimitInductorSetInput(self, *args):
        value = self.inductorSet.get()
        if len(value) > self.nInductor:
            self.inductorSet.set(value[:self.nInductor])

    def SetConnection(self, msg):
        if msg == "Connect":

            if self.comportCombo.get() != "":
                try:
                    self.serial = serial.Serial(port=self.ports[self.comportCombo.current()], baudrate=115200)
                    print("connected")
                    self.serial.write(bytes(("1234567" + "Z").encode()))
                    self.comportCombo.config(state="disable")
                    self.connectButton.config(state="disable")
                    self.refreshButton.config(state="disable")
                    self.disConnectButton.config(state="active")
                    self.entryMultiple.config(state="normal")
                    self.multipleSelectionButtonOn.config(state="active")
                    self.labelMultipleSelection.config(state="normal")
                    self.multipleSelectionButtonOff.config(state="active")
                    self.InitElementPanel()
                except Exception as error:
                    messagebox.showinfo("Error", error)
            else:
                messagebox.showinfo(" Error ", "Select Port !")

        elif msg == "Disconnect":
            try:
                self.serial.write(bytes(("1234567" + "Z").encode()))
                self.serial.close()
                print("disconnected")
                self.connectButton.config(state="active")
                self.disConnectButton.config(state="disable")
                self.refreshButton.config(state="active")
                self.comportCombo.config(state="normal")
                self.entryMultiple.config(state="disable")
                self.multipleSelectionButtonOn.config(state="disable")
                self.labelMultipleSelection.config(state="disable")
                self.multipleSelectionButtonOff.config(state="disable")
                self.DisableElementPanel()
            except Exception as error:
                messagebox.showinfo("Error", error)
                self.TerminateConnectionAndInitMainWindow()
        elif msg == "Refresh":
            self.ports = [str(ports).split(" ")[0] for ports in serial.tools.list_ports.comports(include_links=False)]
            if not self.ports:
                messagebox.showinfo("Error", "No Device Found")
            else:
                messagebox.showinfo("Message", " Device(s) Found")
                self.comportCombo.config(values=self.ports)
                self.comportCombo.set(self.ports[0])
                self.connectButton.config(state="active")
        elif msg == "Multiple-On":
            self.multipleInductorIndex = [0] * self.nInductor
            if self.entryMultiple.get().isdigit() and len(self.entryMultiple.get()) != 0:
                for i in range(0, len(self.entryMultiple.get())):
                    if self.nInductor >= int(self.entryMultiple.get()[i]) >= 1:
                        self.errorMsg = False
                    else:
                        self.errorMsg = True
                        messagebox.showinfo("Error", " Inductor's Input out of range !")
                        break
                if not self.errorMsg:
                    for i in range(0, len(self.entryMultiple.get())):
                        self.multipleInductorIndex[int(self.entryMultiple.get()[i]) - 1] += 1
                    for i in range(0, self.nInductor):
                        if self.multipleInductorIndex[i] >= 2:
                            self.multipleInputError = True
                            self.errorMsg += str(i + 1) + " " + str(
                                self.multipleInductorIndex[i]) + " times\n"
                    if not self.multipleInputError:
                        try:
                            self.serial.write(bytes((self.entryMultiple.get() + "X").encode()))
                            # for inductor in self.inductors:
                            #     if inductor.status:
                            #         inductor.label.config(background=inductor.offColor)
                            #         inductor.onButton.config(state="active")
                            #         inductor.offButton.config(state="disable")
                            #         inductor.status = False

                            for inductor in self.entryMultiple.get():
                                self.inductors[int(inductor) - 1].label.config(
                                    background=self.inductors[int(inductor) - 1].onColor)
                                self.inductors[int(inductor) - 1].onButton.config(state="disable")
                                self.inductors[int(inductor) - 1].offButton.config(state="active")
                                self.inductors[int(inductor) - 1].status = True
                        except Exception as error:
                            messagebox.showinfo("Error", error)
                            self.TerminateConnectionAndInitMainWindow()
                    elif self.multipleInputError:
                        messagebox.showinfo("Error", " You've entered\n" + self.errorMsg)
                        self.errorMsg = ""
            elif len(self.entryMultiple.get()) == 0:
                messagebox.showinfo("Error", " Enter Inductor's Set !")
            else:
                messagebox.showinfo("Error", " Enter Digits Only !")
        elif msg == "Multiple-Off":
            self.multipleInductorIndex = [0] * self.nInductor
            if self.entryMultiple.get().isdigit() and len(self.entryMultiple.get()) != 0:
                for i in range(0, len(self.entryMultiple.get())):
                    if self.nInductor >= int(self.entryMultiple.get()[i]) >= 1:
                        self.errorMsg = False
                    else:
                        self.errorMsg = True
                        messagebox.showinfo("Error", " Inductor's Input out of range !")
                        break
                if not self.errorMsg:
                    for i in range(0, len(self.entryMultiple.get())):
                        self.multipleInductorIndex[int(self.entryMultiple.get()[i]) - 1] += 1
                    for i in range(0, self.nInductor):
                        if self.multipleInductorIndex[i] >= 2:
                            self.multipleInputError = True
                            self.errorMsg += str(i + 1) + " " + str(
                                self.multipleInductorIndex[i]) + " times\n"
                    if not self.multipleInputError:
                        try:
                            self.serial.write(bytes((self.entryMultiple.get() + "Z").encode()))
                            # for inductor in self.inductors:
                            #     if inductor.status:
                            #         inductor.label.config(background=inductor.offColor)
                            #         inductor.onButton.config(state="active")
                            #         inductor.offButton.config(state="disable")
                            #         inductor.status = False

                            for inductor in self.entryMultiple.get():
                                self.inductors[int(inductor) - 1].label.config(
                                    background=self.inductors[int(inductor) - 1].offColor)
                                self.inductors[int(inductor) - 1].onButton.config(state="active")
                                self.inductors[int(inductor) - 1].offButton.config(state="disable")
                                self.inductors[int(inductor) - 1].status = False
                        except Exception as error:
                            messagebox.showinfo("Error", error)
                            self.TerminateConnectionAndInitMainWindow()
                    elif self.multipleInputError:
                        messagebox.showinfo("Error", " You've entered\n" + self.errorMsg)
                        self.errorMsg = ""
            elif len(self.entryMultiple.get()) == 0:
                messagebox.showinfo("Error", " Enter Inductor's Set !")
            else:
                messagebox.showinfo("Error", " Enter Digits Only !")

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.mainFrame = tk.Frame(self.parent, background="bisque")
        self.mainFrame.pack(fill=tk.BOTH, expand=True)

        self.comPortInterface = tk.Frame(self.mainFrame, background="grey", height=30)
        self.comPortInterface.pack(fill=tk.X)
        self.ports = [str(ports).split(" ")[0] for ports in serial.tools.list_ports.comports(include_links=False)]
        self.labelComPort = tk.Label(self.comPortInterface, text="COM PORT :", width=10)
        self.labelComPort.pack(side=tk.LEFT, padx=5, pady=5)
        self.comportCombo = ttk.Combobox(self.comPortInterface, values=self.ports)
        self.comportCombo.pack(side=tk.LEFT, padx=5, pady=5)

        self.refreshButton = tk.Button(self.comPortInterface, text="Refresh", width=10,
                                       command=lambda: self.SetConnection("Refresh"))
        self.refreshButton.pack(side=tk.LEFT, padx=5, pady=5)

        self.connectButton = tk.Button(self.comPortInterface, text="Connect", width=10,
                                       command=lambda: self.SetConnection("Connect"))

        self.connectButton.pack(side=tk.LEFT, padx=5, pady=5)
        self.disConnectButton = tk.Button(self.comPortInterface, text="Disconnect", width=10,
                                          command=lambda: self.SetConnection("Disconnect"))
        self.disConnectButton.pack(side=tk.LEFT, padx=5, pady=5)
        self.disConnectButton.config(state="disable")

        self.labelMultipleSelection = tk.Label(self.comPortInterface, text="Multiple Inductor Selection :", width=22)
        self.labelMultipleSelection.pack(side=tk.LEFT, padx=5, pady=5)
        self.labelMultipleSelection.config(state="disable")
        self.inductorSet = tk.StringVar()
        self.inductorSet.trace('w', self.LimitInductorSetInput)
        self.entryMultiple = tk.Entry(self.comPortInterface, width=7, textvariable=self.inductorSet)
        self.entryMultiple.pack(side=tk.LEFT, padx=5, pady=5)
        self.entryMultiple.config(state="disable")

        self.multipleSelectionButtonOn = tk.Button(self.comPortInterface, text="Turn On", width=10,
                                                   command=lambda: self.SetConnection("Multiple-On"))
        self.multipleSelectionButtonOn.pack(side=tk.LEFT, padx=5, pady=5)
        self.multipleSelectionButtonOn.config(state="disable")

        self.multipleSelectionButtonOff = tk.Button(self.comPortInterface, text="Turn Off", width=10,
                                                    command=lambda: self.SetConnection("Multiple-Off"))
        self.multipleSelectionButtonOff.pack(side=tk.LEFT, padx=5, pady=5)
        self.multipleSelectionButtonOff.config(state="disable")

        self.elementFrame = tk.Frame(self.mainFrame, background="bisque", height=210)
        self.elementFrame.pack(fill=tk.X)
        for nPanel in range(1, self.nInductor + 1):
            self.inductors[nPanel - 1] = InductorPanel(nPanel, self.elementFrame, self)
        self.DisableElementPanel()
        if not self.ports:
            messagebox.showinfo("Error", "No Device Found")
            self.connectButton.config(state="disable")
        else:
            self.comportCombo.set(self.ports[0])


def Main():
    root = tk.Tk()
    root.geometry('1180x250')
    root.title("7 Inductors Controller")
    root.resizable(width=0, height=0)
    MainApplication(root).pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    Main()
