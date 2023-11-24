from grafica import Grafica
from tkinter import Tk,PhotoImage

imgA='img/icon8.png'



if __name__ == '__main__':
    ventana = Tk()
    ventana.geometry('742x535')
    ventana.config(bg='gray30', bd=4)
    ventana.wm_title('Grafica Matplodlib animacion')
    ventana.minsize(width=700, height=400)
    ventana.call('wm', 'iconphoto', ventana._w, PhotoImage(file = imgA))

    app = Grafica(ventana)
    app.mainloop()
