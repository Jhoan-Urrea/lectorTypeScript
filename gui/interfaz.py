import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os

# Añadir la raíz del proyecto al path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analizadores.identificador import IdentificadorAFD
from lexer import AnalizadorLexico
from tokens import Categoria

class InterfazLexer:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico - JavaScript")
        self.root.geometry("900x700")  # Ajustar tamaño para más espacio
        
        # Definir colores para categorías de tokens
        self.colores_categoria = {
            Categoria.PALABRA_RESERVADA: "blue",
            Categoria.IDENTIFICADOR: "black",
            Categoria.NUMERO_NATURAL: "dark green",
            Categoria.NUMERO_REAL: "green",
            Categoria.CADENA: "purple",
            Categoria.COMENTARIO_LINEA: "gray",
            Categoria.COMENTARIO_BLOQUE: "gray",
            Categoria.OPERADOR_ARITMETICO: "orange red",
            Categoria.OPERADOR_COMPARACION: "orange red",
            Categoria.OPERADOR_LOGICO: "orange red",
            Categoria.OPERADOR_ASIGNACION: "orange red",
            Categoria.OPERADOR_INCREMENTO: "orange red",
            Categoria.OPERADOR_DECREMENTO: "orange red",
            Categoria.OPERADOR_ACCESO: "dark orange",
            Categoria.PARENTESIS_APERTURA: "dark cyan",
            Categoria.PARENTESIS_CIERRE: "dark cyan",
            Categoria.LLAVE_APERTURA: "dark cyan",
            Categoria.LLAVE_CIERRE: "dark cyan",
            Categoria.CORCHETE_APERTURA: "dark slate gray",
            Categoria.CORCHETE_CIERRE: "dark slate gray",
            Categoria.DOS_PUNTOS: "firebrick",
            Categoria.SIGNO_INTERROGACION: "purple4",
            Categoria.OPERADOR_OPTIONAL_CHAINING: "orchid",
            Categoria.OPERADOR_NULISH_COALESCING: "orchid",
            Categoria.TERMINAL: "magenta",
            Categoria.SEPARADOR: "magenta",
            # Categoria.ERROR se maneja en el panel de errores, no necesita color aquí
        }
        
        # Configuración de la interfaz
        self.configure_ui()
        
        # Inicializar analizador léxico
        self.analizador = AnalizadorLexico()
        
    def configure_ui(self):
        """Configura todos los elementos de la interfaz gráfica"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo para el editor
        left_frame = ttk.LabelFrame(main_frame, text="Código JavaScript")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.editor = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, width=50, height=30)
        self.editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel derecho para resultados (tokens y errores)
        right_frame = ttk.Frame(main_frame) # Quitar LabelFrame para mejor distribución interna
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botones de acción
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X, pady=(0,5)) # pady inferior para separar de la tabla
        
        self.btn_analizar = ttk.Button(btn_frame, text="Analizar Código", command=self.analizar_codigo)
        self.btn_analizar.pack(side=tk.LEFT, padx=(0,5))
        
        self.btn_limpiar = ttk.Button(btn_frame, text="Limpiar", command=self.limpiar)
        self.btn_limpiar.pack(side=tk.LEFT)
        
        # Panel para la tabla de Tokens
        tokens_frame = ttk.LabelFrame(right_frame, text="Tokens Identificados")
        tokens_frame.pack(fill=tk.BOTH, expand=True, pady=(5,5))

        columns = ("lexema", "categoria", "fila", "columna")
        self.tabla_tokens = ttk.Treeview(tokens_frame, columns=columns, show="headings")
        
        self.tabla_tokens.heading("lexema", text="Lexema")
        self.tabla_tokens.heading("categoria", text="Categoría")
        self.tabla_tokens.heading("fila", text="Fila")
        self.tabla_tokens.heading("columna", text="Columna")
        
        self.tabla_tokens.column("lexema", width=150, anchor=tk.W)
        self.tabla_tokens.column("categoria", width=150, anchor=tk.W)
        self.tabla_tokens.column("fila", width=50, anchor=tk.CENTER)
        self.tabla_tokens.column("columna", width=50, anchor=tk.CENTER)
        
        # Configurar tags para colores
        for categoria, color in self.colores_categoria.items():
            # Usamos el nombre simple de la categoría como tag para simplificar
            tag_name = categoria.split('.')[-1] if '.' in categoria else categoria
            self.tabla_tokens.tag_configure(tag_name, foreground=color)
        
        scrollbar_tokens = ttk.Scrollbar(tokens_frame, orient=tk.VERTICAL, command=self.tabla_tokens.yview)
        self.tabla_tokens.configure(yscroll=scrollbar_tokens.set)
        
        self.tabla_tokens.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_tokens.pack(side=tk.RIGHT, fill=tk.Y)

        # Panel para Errores Léxicos
        errores_frame = ttk.LabelFrame(right_frame, text="Errores Léxicos")
        # Ajustar altura relativa para el panel de errores, ej. 1/3 de la tabla de tokens
        errores_frame.pack(fill=tk.BOTH, expand=True, pady=(5,0), ipady=5) 
        
        self.texto_errores = scrolledtext.ScrolledText(errores_frame, wrap=tk.WORD, width=40, height=5, state=tk.DISABLED)
        self.texto_errores.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
             
    def analizar_codigo(self):
        """Analiza el código completo usando el analizador léxico"""
        self.limpiar_resultados()
        
        codigo = self.editor.get("1.0", tk.END)
        if not codigo.strip():
            messagebox.showinfo("Aviso", "Por favor ingresa código para analizar.")
            return
            
        tokens, errores = self.analizador.analizar(codigo)
        
        # Mostrar tokens en la tabla
        for token in tokens:
            categoria_completa = token.categoria # Guardamos la original por si acaso
            categoria_simple = categoria_completa.split('.')[-1] if '.' in categoria_completa else categoria_completa
            
            # Determinar el tag para el color
            # El tag debe ser el nombre simple de la categoría que usamos al configurar
            tag_aplicar = categoria_simple 
            
            self.tabla_tokens.insert("", "end", values=(
                token.lexema, 
                categoria_simple,
                token.fila, 
                token.columna
            ), tags=(tag_aplicar,))
        
        # Mostrar errores en el panel de errores
        self.texto_errores.config(state=tk.NORMAL)
        self.texto_errores.delete("1.0", tk.END)
        if errores:
            for i, error in enumerate(errores, 1):
                mensaje_error = f"{i}. Error: Carácter '{error.lexema}' no reconocido en Fila {error.fila}, Columna {error.columna}\n"
                self.texto_errores.insert(tk.END, mensaje_error)
            messagebox.showwarning(
                "Errores Léxicos Encontrados", 
                f"Se encontraron {len(errores)} errores léxicos. Revise el panel de errores."
            )
        else:
            self.texto_errores.insert(tk.END, "No se encontraron errores léxicos.\n")
        self.texto_errores.config(state=tk.DISABLED)
    
    def limpiar_tabla_tokens(self):
        """Limpia la tabla de tokens"""
        for item in self.tabla_tokens.get_children():
            self.tabla_tokens.delete(item)

    def limpiar_panel_errores(self):
        """Limpia el panel de errores"""
        self.texto_errores.config(state=tk.NORMAL)
        self.texto_errores.delete("1.0", tk.END)
        self.texto_errores.config(state=tk.DISABLED)
            
    def limpiar_resultados(self):
        self.limpiar_tabla_tokens()
        self.limpiar_panel_errores()

    def limpiar(self):
        """Limpia editor y todos los resultados"""
        self.editor.delete("1.0", tk.END)
        self.limpiar_resultados()

if __name__ == "__main__":
    root = tk.Tk()
    # Renombrar la clase de la interfaz si es necesario, ej. InterfazLexer
    app = InterfazLexer(root) 
    root.mainloop()