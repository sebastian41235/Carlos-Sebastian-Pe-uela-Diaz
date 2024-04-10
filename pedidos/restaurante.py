import tkinter as tk
from tkinter import ttk
import mysql.connector

class holi:
    def __init__(self, root):
        self.root = root
        self.root.title("hola como estas")
        
        
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="",  
            database="pedidos"
        )
        self.cursor = self.conexion.cursor()
        
        self.precios_comida = {
            "hamburguesa": 10,
            "pizza": 8,
            "empanada": 6,
       
        }
        self.precios_bebida = {
            "agua": 1,
            "cocacola": 2,
            "lechita": 2,
           
        }
        self.total = 0
        self.pedido_comida = {}
        self.pedido_bebida = {}
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)
        self.tab_comida = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_comida, text="comida")
        self.tab_bebida = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_bebida, text="ebida")
        self.comida_var = tk.StringVar(root)
        self.comida_var.set("seleccionar una comida")
        self.comida_dropdown = tk.OptionMenu(self.tab_comida, self.comida_var, *self.precios_comida.keys())
        self.comida_dropdown.pack(pady=10, side="left")
        self.precio_comida_label = tk.Label(self.tab_comida, text="")
        self.precio_comida_label.pack(pady=10, side="left")
        self.agregar_comida_button = tk.Button(self.tab_comida, text="añadir al carrito", command=self.agregar_comida)
        self.agregar_comida_button.pack(pady=5, side="left")
        self.comida_label = tk.Label(self.tab_comida, text="comida:")
        self.comida_label.pack(pady=5)
        self.bebida_var = tk.StringVar(root)
        self.bebida_var.set("selecciona una bebida")
        self.bebida_dropdown = tk.OptionMenu(self.tab_bebida, self.bebida_var, *self.precios_bebida.keys())
        self.bebida_dropdown.pack(pady=10, side="left")
        self.precio_bebida_label = tk.Label(self.tab_bebida, text="")
        self.precio_bebida_label.pack(pady=10, side="left")
        self.agregar_bebida_button = tk.Button(self.tab_bebida, text="agregar bebida", command=self.agregar_bebida)
        self.agregar_bebida_button.pack(pady=5, side="left")
        self.bebida_label = tk.Label(self.tab_bebida, text="bebida:")
        self.bebida_label.pack(pady=5)
        self.total_label = tk.Label(root, text="total: $0")
        self.total_label.pack(pady=10)
        self.confirmar_button = tk.Button(root, text="enviar pedido", command=self.confirmar_pedido)
        self.confirmar_button.pack(pady=5)

    def actualizar_precio_comida(self, *args):
        comida_seleccionada = self.comida_var.get()
        precio = self.precios_comida.get(comida_seleccionada, 0)
        self.precio_comida_label.config(text=f"Precio: ${precio}")

    def actualizar_precio_bebida(self, *args):
        bebida_seleccionada = self.bebida_var.get()
        precio = self.precios_bebida.get(bebida_seleccionada, 0)
        self.precio_bebida_label.config(text=f"Precio: ${precio}")

    def agregar_comida(self):
        comida = self.comida_var.get()
        precio = self.precios_comida.get(comida, 0)
        if comida in self.pedido_comida:
            self.pedido_comida[comida] += 1
        else:
            self.pedido_comida[comida] = 1
        
        self.total += precio
        self.actualizar_pedido()
        
    def agregar_bebida(self):
        bebida = self.bebida_var.get()
        precio = self.precios_bebida.get(bebida, 0)
        if bebida in self.pedido_bebida:
            self.pedido_bebida[bebida] += 1
        else:
            self.pedido_bebida[bebida] = 1
        
        self.total += precio
        self.actualizar_pedido()
        
    def actualizar_pedido(self):
        comida_texto = ", ".join([f"{cantidad} {comida}" for comida, cantidad in self.pedido_comida.items()])
        bebida_texto = ", ".join([f"{cantidad} {bebida}" for bebida, cantidad in self.pedido_bebida.items()])
        self.comida_label.config(text=f"comida: {comida_texto}")
        self.bebida_label.config(text=f"bebida: {bebida_texto}")
        self.total_label.config(text=f"total: ${self.total}")
        
    def confirmar_pedido(self):
        mesa_seleccionada = 1 
        
        insert_pedido_query = "INSERT INTO pedidos (fecha, mesa, total) VALUES (NOW(), %s, %s)"
        self.cursor.execute(insert_pedido_query, (mesa_seleccionada, self.total))
        pedido_id = self.cursor.lastrowid
        for comida, cantidad in self.pedido_comida.items():
            comida_id = self.obtener_id_comida(comida)
            insert_comida_query = "INSERT INTO pedidos_comida (id_p, id_c, cantidad) VALUES (%s, %s, %s)"
            self.cursor.execute(insert_comida_query, (pedido_id, comida_id, cantidad))
        for bebida, cantidad in self.pedido_bebida.items():
            bebida_id = self.obtener_id_bebida(bebida)
            insert_bebida_query = "INSERT INTO pedidos_bebida (id_p, id_b, cantidad) VALUES (%s, %s, %s)"
            self.cursor.execute(insert_bebida_query, (pedido_id, bebida_id, cantidad))
        self.conexion.commit()
        print("mesa que mas aplauda", mesa_seleccionada)
        print("comida:", self.pedido_comida)
        print("bebida:", self.pedido_bebida)
        print("total:", self.total)
        self.total = 0
        self.pedido_comida = {}
        self.pedido_bebida = {}
        self.actualizar_pedido()
        
    def obtener_id_comida(self, comida):
        query = "SELECT id_comida FROM comida WHERE nombre_c = %s"
        self.cursor.execute(query, (comida,))
        resultado = self.cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return None
        
    def obtener_id_bebida(self, bebida):
        query = "SELECT id_bebida FROM bebida WHERE nombre_b = %s"
        self.cursor.execute(query, (bebida,))
        resultado = self.cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = holi(root)
    root.mainloop()