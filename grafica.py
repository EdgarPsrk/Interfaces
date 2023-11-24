import matplotlib.pyplot as plt
import matplotlib.animation as animation
import collections
from tkinter import Frame, Button,Label,ttk,PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from comunicacion_serial import Comunicacion
from serial import Serial

colorA='#000000'
colorB='#6E6D70'
colorC='blue'

imgA='img/icon8.png'

class Grafica(Frame):
    def __init__(self, master, *arg):
        super().__init__(master, *arg)

        self.datos_arduino = Comunicacion()
        self.actualizar_puertos()
        
        self.muestra = 100
        self.datos = 0.0

        self.fig = plt.Figure(facecolor =colorA , dpi = 100, figsize = (4,2))
        plt.title('Graficar datos de arduino', color = 'white', size = 12, family = 'Arial')
        ax = self.fig.add_subplot(111)
        ax.tick_params(direction = 'out', length = 5, width = 2, colors = 'white', grid_color = 'r', grid_alpha = 0.5)

        self.line1, = ax.plot( [], [], color = 'm', marker = 'o', linewidth = 2, markersize = 1, markeredgecolor = 'm')
        self.line2, = ax.plot( [], [], color = 'g', marker = 'o', linewidth = 2, markersize = 1, markeredgecolor = 'g')

        plt.xlim([0,self.muestra])
        plt.ylim([-5,6])

        ax.set_facecolor(colorB)
        ax.spines['bottom'].set_color(colorC)
        ax.spines['left'].set_color(colorC)
        ax.spines['top'].set_color(colorC)
        ax.spines['right'].set_color(colorC)

        self.datos_senal_uno = collections.deque([0]*self.muestra, maxlen = self.muestra)
        self.datos_senal_dos = collections.deque([0]*self.muestra, maxlen = self.muestra)

        self.widgets()

    def animate(self,i):
        self.datos = (self.datos_arduino.datos_recibidos.get())
        dato = self.datos.split(',')
        dato_uno = float(dato[0])
        dato_dos = float(dato[1])

        self.datos_senal_uno.append(dato_uno)
        self.datos_senal_dos.append(dato_dos)
        self.line1.set_data(range(self.muestra), self.datos_senal_uno)
        self.line2.set_data(range(self.muestra), self.datos_senal_dos)

    def iniciar(self):
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval =100, blit = False)
        self.bt_graficar.config(state = 'disabled')
        self.bt_pausar.config(state = 'normal')
        self.canvas.draw()

    def pausar(self):
        self.ani.event_source.stop()
        self.bt_reanudar.config(state = 'normal')

    def reanudar(self):
        self.ani.event_source.start()
        self.bt_reanudar.config(state = 'disabled')

    def widgets(self):
        frame = Frame(self.master, bg = 'gray50', bd = 2)
        frame.grid(column = 0, columnspan = 2, row = 0, sticky = 'nsew')

        frame1 = Frame(self.master, bg = 'black')
        frame2 = Frame(self.master, bg = 'black')
        frame3 = Frame(self.master, bg = 'black')
        frame4 = Frame(self.master, bg = 'black')

        frame1.grid(column = 2, row = 0, sticky = 'nsew')
        frame2.grid(column = 1, row = 1, sticky = 'nsew')
        frame3.grid(column = 2, row = 1, sticky = 'nsew')
        frame4.grid(column = 0, row = 1, sticky = 'nsew')

        self.master.columnconfigure(0, weight = 1)
        self.master.columnconfigure(1, weight = 1)
        self.master.columnconfigure(2, weight = 1)
        self.master.rowconfigure(0, weight = 5)
        self.master.rowconfigure(1, weight = 1)

        self.canvas = FigureCanvasTkAgg(self.fig, master = frame)
        self.canvas.get_tk_widget().pack(padx = 0, pady = 0, expand = True, fill = 'both')

        self.bt_graficar = Button(frame4, text = 'Graficar datos', font = ('Arial', 12, 'bold'), width=12, bg = 'purple4', fg = 'white', command = self.iniciar)
        self.bt_pausar = Button(frame4, state = 'disabled',text = 'Pausar', font = ('Arial', 12, 'bold'), width=12, bg = 'salmon', fg = 'white', command = self.pausar)
        self.bt_reanudar = Button(frame4,state = 'disabled', text = 'Reanudar', font = ('Arial', 12, 'bold'), width=12, bg = 'green', fg = 'white', command = self.reanudar)
        self.bt_graficar.pack(pady = 5, expand = 1)
        self.bt_pausar.pack(pady = 5, expand = 1)
        self.bt_reanudar.pack(pady = 5, expand = 1)

        Label(frame2, text = 'Control analogico', font = ('Arial', 15), bg = 'black', fg = 'white').pack(padx = 5, expand = 1)
        style = ttk.Style()
        style.configure('Horizontal.TScale', background = 'black')
        self.slider_uno = ttk.Scale(frame2, command = self.datos_slider_uno, state = 'disabled', to = 255, from_ = 0, orient = 'horizontal', length = 280, style = 'TScale')
        self.slider_dos = ttk.Scale(frame2, command = self.datos_slider_dos, state = 'disabled', to = 255, from_ = 0, orient = 'horizontal', length = 280, style = 'TScale')
        self.slider_uno.pack(pady = 5, expand = 1)
        self.slider_dos.pack(pady = 5, expand = 1)

        port = self.datos_arduino.puertos
        baud = self.datos_arduino.baudrates

        Label(frame1, text = 'Puertos', font = ('Arial', 12, 'bold'), bg = 'black', fg = 'white').pack(padx = 5, expand = 1)
        self.combobox_port = ttk.Combobox(frame1, values = port, justify = 'center', width = 12, font = 'Arial')
        self.combobox_port.pack(pady = 0, expand = 1)
        self.combobox_port.current(0)

        Label(frame1, text = 'Baudrates', font = ('Arial', 12, 'bold'), bg = 'black', fg = 'white').pack(padx = 0, expand = 1)
        self.combobox_baud = ttk.Combobox(frame1, values = baud, justify = 'center', width = 12, font = 'Arial')
        self.combobox_baud.pack(pady = 0, expand = 1)
        self.combobox_baud.current(3)

        self.bt_conectar = Button(frame1, text = 'Conectar', font = ('Arial', 12, 'bold'), width = 12, bg = 'green2', command = lambda: self.conectar_serial(Serial))
        self.bt_actualizar = Button(frame1, text = 'Actualizar', font = ('Arial', 12, 'bold'), width = 12, bg = 'magenta', command = lambda: self.actualizar_puertos)
        self.bt_desconectar = Button(frame1, text = 'Desconectar',state= 'disabled', font = ('Arial', 12, 'bold'), width = 12, bg = 'red2', command = lambda: self.desconectar_serial(Serial))
        self.bt_conectar.pack(pady = 5, expand = 1)
        self.bt_actualizar.pack(pady = 5, expand = 1)
        self.bt_desconectar.pack(pady = 5, expand = 1)

        self.logo = PhotoImage(file = imgA)

        Label(frame3, image = self.logo, bg = 'black').pack( pady = 5, expand = 1)

    def actualizar_puertos(self):
        self.datos_arduino.puertos_disponibles()

    def conectar_serial(self, serial):
        try:
            self.bt_conectar.config(state='disabled')
            self.bt_desconectar.config(state='normal')
            self.slider_uno.config(state='normal')
            self.slider_dos.config(state='normal')
            self.bt_graficar.config(state='normal')
            self.bt_reanudar.config(state='disabled')

            self.datos_arduino.arduino.port = self.combobox_port.get()
            self.datos_arduino.arduino.baudrate = self.combobox_baud.get()
            self.datos_arduino.conexion_serial()

        except serial.SerialException as e:
            print(f"Error connecting to serial: {e}")
            # You might want to show an error message to the user here

    def desconectar_serial(self, serial):
        try:
            self.bt_conectar.config(state='normal')
            self.bt_desconectar.config(state='disabled')
            self.bt_pausar.config(state='disabled')
            self.slider_uno.config(state='disabled')
            self.slider_dos.config(state='disabled')

            if hasattr(self, 'ani') and self.ani:
                try:
                    self.ani.event_source.stop()
                except Exception as e:
                    print(f"Error stopping animation: {e}")

            self.datos_arduino.desconectar()

        except serial.SerialException as e:
            print(f"Error disconnecting from serial: {e}")
            # You might want to show an error message to the user here


    def datos_slider_uno(self):
        dato = '1,' + str( int ( self.slider_uno.get() ) )
        self.datos_arduino.enviar_datos(dato)

    def datos_slider_dos(self):
        dato = '2,' + str( int ( self.slider_dos.get() ) )
        self.datos_arduino.enviar_datos(dato)
