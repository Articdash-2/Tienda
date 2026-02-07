import json
import os
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

class AdminApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FIEL ES DIOS - Panel Administrativo")
        self.geometry("1100x800")
        
        # Cargar datos iniciales
        self.productos = self.cargar_datos()
        self.indice_actual = 0

        # Configuración de Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- BARRA LATERAL (LISTA) ---
        self.sidebar = ctk.CTkScrollableFrame(self, width=300, label_text="Catálogo de Productos")
        self.sidebar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.actualizar_sidebar()

        # --- PANEL CENTRAL (EDICIÓN CON SCROLL) ---
        self.main_container = ctk.CTkScrollableFrame(self)
        self.main_container.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Imagen Previa
        self.img_label = ctk.CTkLabel(self.main_container, text="", width=350, height=350)
        self.img_label.pack(pady=20)

        # Campos de entrada
        self.entry_nombre = self.crear_campo("Nombre para la Web (Ej: Silla de Comedor):")
        self.entry_file = self.crear_campo("Nombre del Archivo (Ej: silla_roja):")
        self.entry_precio = self.crear_campo("Precio (L. sin comas):")
        self.entry_cat = self.crear_campo("Categoría (Hogar, Ropa, etc.):")
        self.entry_desc = self.crear_campo("Descripción Detallada (Aparecerá en la web):")

        # --- SECCIÓN DE BOTONES ---
        self.btn_save = ctk.CTkButton(self.main_container, text="GUARDAR CAMBIOS Y RENOMBRAR ✅", 
                                     fg_color="#27ae60", hover_color="#2ecc71",
                                     height=55, font=("Arial", 16, "bold"),
                                     command=self.guardar_todo)
        self.btn_save.pack(pady=25, fill="x", padx=80)

        self.btn_delete = ctk.CTkButton(self.main_container, text="ELIMINAR PRODUCTO 🗑️", 
                                       fg_color="#c0392b", hover_color="#e74c3c",
                                       height=45, font=("Arial", 13),
                                       command=self.eliminar_producto)
        self.btn_delete.pack(pady=10, fill="x", padx=150)

        # Cargar el primer producto si existe
        if self.productos:
            self.cargar_producto(0)

    def cargar_datos(self):
        if os.path.exists('productos.json'):
            with open('productos.json', 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except:
                    return []
        return []

    def crear_campo(self, texto):
        label = ctk.CTkLabel(self.main_container, text=texto, font=("Arial", 13, "bold"))
        label.pack(pady=(15, 0), anchor="w", padx=60)
        entry = ctk.CTkEntry(self.main_container, width=600, height=40)
        entry.pack(pady=5, padx=60)
        return entry

    def actualizar_sidebar(self):
        for widget in self.sidebar.winfo_children():
            widget.destroy()
        
        for i, p in enumerate(self.productos):
            # Naranja si no tiene precio o categoría válida
            color = "#d35400" if p.get('precio', 0) == 0 else "transparent"
            btn = ctk.CTkButton(self.sidebar, text=f"{p.get('id', 'NUEVO')} - {p.get('nombre', 'Sin Nombre')[:25]}", 
                               fg_color=color, anchor="w",
                               command=lambda idx=i: self.cargar_producto(idx))
            btn.pack(pady=2, fill="x")

    def cargar_producto(self, index):
        if not self.productos: return
        self.indice_actual = index
        p = self.productos[index]
        
        try:
            full_path = p['img'].replace("./", "")
            img = Image.open(full_path)
            ctk_img = ctk.CTkImage(light_image=img, size=(350, 350))
            self.img_label.configure(image=ctk_img, text="")
        except:
            self.img_label.configure(image=None, text="⚠️ Imagen no encontrada")

        self.entry_nombre.delete(0, 'end')
        self.entry_nombre.insert(0, p.get('nombre', ''))
        
        file_name = os.path.basename(p['img']).split(".")[0]
        self.entry_file.delete(0, 'end')
        self.entry_file.insert(0, file_name)
        
        self.entry_precio.delete(0, 'end')
        self.entry_precio.insert(0, str(p.get('precio', 0)))
        
        self.entry_cat.delete(0, 'end')
        self.entry_cat.insert(0, p.get('categoria', 'GENERAL'))
        
        # AQUÍ ESTÁ LA MAGIA: Carga la descripción correctamente
        self.entry_desc.delete(0, 'end')
        self.entry_desc.insert(0, p.get('description', ''))

    def guardar_todo(self):
        if not self.productos: return
        p = self.productos[self.indice_actual]
        vieja_ruta = p['img'].replace("./", "")
        
        # Limpieza de nombre de archivo
        nuevo_nombre_base = "".join(c for c in self.entry_file.get() if c.isalnum() or c in (' ', '_')).strip().replace(" ", "_").lower()
        extension = os.path.splitext(vieja_ruta)[1]
        nueva_ruta = f"img/todo/{nuevo_nombre_base}{extension}"
        
        if nueva_ruta != vieja_ruta:
            contador = 1
            while os.path.exists(nueva_ruta):
                nueva_ruta = f"img/todo/{nuevo_nombre_base}_{contador}{extension}"
                contador += 1
            try:
                os.rename(vieja_ruta, nueva_ruta)
                p['img'] = f"./{nueva_ruta}"
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo renombrar el archivo: {e}")
                return

        try:
            p['nombre'] = self.entry_nombre.get()
            p['precio'] = int(self.entry_precio.get())
            p['categoria'] = self.entry_cat.get().upper()
            
            # AQUÍ ESTÁ LA MAGIA: Guarda en la llave correcta
            p['description'] = self.entry_desc.get()
            
            with open('productos.json', 'w', encoding='utf-8') as f:
                json.dump(self.productos, f, indent=4, ensure_ascii=False)
            
            messagebox.showinfo("Éxito", "¡Cambios guardados con éxito! ✅")
            self.actualizar_sidebar()
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número entero.")

    def eliminar_producto(self):
        if not self.productos: return
        if messagebox.askyesno("Confirmar", "¿Eliminar este producto permanentemente?"):
            self.productos.pop(self.indice_actual)
            with open('productos.json', 'w', encoding='utf-8') as f:
                json.dump(self.productos, f, indent=4, ensure_ascii=False)
            self.actualizar_sidebar()
            if self.productos:
                self.cargar_producto(0)
            else:
                self.img_label.configure(image=None, text="Vacio")
            messagebox.showinfo("Borrado", "Producto eliminado.")

if __name__ == "__main__":
    app = AdminApp()
    app.mainloop()