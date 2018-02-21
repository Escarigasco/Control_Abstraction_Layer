

import tkinter as tk


class GUI(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.L1 = tk.Label(self, text="Parameter")
        self.L1.grid(row=0, column=0)
        self.E1 = tk.Entry(self)
        self.E1.grid(row=0, column=1)

        self.L2 = tk.Label(self, text="Setpoint")
        self.L2.grid(row=1, column=0)
        self.E2 = tk.Entry(self)
        self.E2.grid(row=1, column=1)

        self.L3 = tk.Label(self, text="Sensor")
        self.L3.grid(row=2, column=0)
        self.E3 = tk.Entry(self)
        self.E3.grid(row=2, column=1)

        self.button = tk.Button(self, text="Update", command=self.on_button)
        self.button.grid()
        '''self.E1.pack(row=3, column=1)
        self.E2.pack()
        self.E3.pack()'''

    def on_button(self):  # you have to make this method private
        self.parameter = self.E1.get()
        print(self.E1.get())
        self.setpoint = self.E2.get()
        print(self.E2.get())
        self.sensor = self.E3.get()
        print(self.E3.get())

    def get_parameters(self):
        array_of_parameters = {}
        self.parameter = 1
        self.setpoint = 2
        self.sensor = 3
        array_of_parameters["parameter"] = self.parameter
        array_of_parameters["setpoint"] = self.setpoint
        array_of_parameters["sensor"] = self.sensor
        return array_of_parameters


app = GUI()
app.mainloop()  # this can't be in the main because it stays looping, it doesn't exit this method as it s the one keeps alive the GUI
print(app.get_parameters)
