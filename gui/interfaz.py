import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os

# Añadir la raíz del proyecto al path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analizadores.lexer import AnalizadorLexico
from tokens import Categoria

class InterfazLexica:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico - TypeScript")
        self.root.geometry("1200x800")  # Ventana más grande
        
        # Definir colores para categorías de tokens
        self.colores_categoria = {
            Categoria.IDENTIFICADOR: "black",
            Categoria.NUMERO_NATURAL: "blue",
            Categoria.NUMERO_REAL: "blue",
            Categoria.CADENA: "green",
            Categoria.PALABRA_RESERVADA: "purple",
            Categoria.TIPO_PRIMITIVO: "dark violet",
            Categoria.TIPO_INTERFACE: "dark violet",
            Categoria.TIPO_TYPE: "dark violet",
            Categoria.TIPO_ENUM: "dark violet",
            Categoria.TIPO_KEYOF: "dark violet",
            Categoria.TIPO_INFER: "dark violet",
            Categoria.TIPO_UNION: "dark violet",
            Categoria.TIPO_INTERSECTION: "dark violet",
            Categoria.TIPO_GENERIC: "dark violet",
            Categoria.TIPO_TEMPLATE: "dark violet",
            Categoria.OPERADOR_ARITMETICO: "orange",
            Categoria.OPERADOR_COMPARACION: "orange",
            Categoria.OPERADOR_LOGICO: "orange",
            Categoria.OPERADOR_ASIGNACION: "orange",
            Categoria.OPERADOR_INCREMENTO: "orange red",
            Categoria.OPERADOR_DECREMENTO: "orange red",
            Categoria.OPERADOR_ACCESO: "dark orange",
            Categoria.OPERADOR_TYPESCRIPT: "teal",
            Categoria.OPERADOR_UNION: "teal",
            Categoria.OPERADOR_INTERSECTION: "teal",
            Categoria.OPERADOR_OPTIONAL: "teal",
            Categoria.OPERADOR_NON_NULL: "teal",
            Categoria.PARENTESIS_IZQ: "dark cyan",
            Categoria.PARENTESIS_DER: "dark cyan",
            Categoria.LLAVE_IZQ: "dark cyan",
            Categoria.LLAVE_DER: "dark cyan",
            Categoria.CORCHETE_IZQ: "dark cyan",
            Categoria.CORCHETE_DER: "dark cyan",
            Categoria.PUNTO_Y_COMA: "brown",
            Categoria.COMA: "brown",
            Categoria.PUNTO: "brown",
            Categoria.MENOR_QUE: "dark cyan",
            Categoria.MAYOR_QUE: "dark cyan",
            Categoria.COMENTARIO_LINEA: "gray",
            Categoria.COMENTARIO_BLOQUE: "gray",
            Categoria.EOF: "black"
        }
        
        # Configuración de la interfaz
        self.configure_ui()
        
        # Inicializar analizador léxico
        self.analizador = AnalizadorLexico()
        
    def configure_ui(self):
        """Configura todos los elementos de la interfaz gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo para el editor
        left_frame = ttk.LabelFrame(main_frame, text="Código TypeScript")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Editor con fuente monoespaciada
        self.editor = scrolledtext.ScrolledText(
            left_frame,
            wrap=tk.NONE,  # Desactivar wrap para mejor visualización de código
            width=50,
            height=30,
            font=('Consolas', 10)  # Fuente monoespaciada
        )
        self.editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel derecho para resultados
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botones de acción
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X, pady=(0,5))
        
        self.btn_analizar = ttk.Button(
            btn_frame,
            text="Analizar Código",
            command=self.analizar_codigo
        )
        self.btn_analizar.pack(side=tk.LEFT, padx=(0,5))
        
        self.btn_limpiar = ttk.Button(
            btn_frame,
            text="Limpiar",
            command=self.limpiar
        )
        self.btn_limpiar.pack(side=tk.LEFT)
        
        # Panel para la tabla de Tokens
        tokens_frame = ttk.LabelFrame(right_frame, text="Tokens Identificados")
        tokens_frame.pack(fill=tk.BOTH, expand=True, pady=(5,5))

        # Configurar tabla de tokens
        columns = ("lexema", "categoria", "fila", "columna")
        self.tabla_tokens = ttk.Treeview(
            tokens_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )
        
        # Configurar encabezados
        self.tabla_tokens.heading("lexema", text="Lexema")
        self.tabla_tokens.heading("categoria", text="Categoría")
        self.tabla_tokens.heading("fila", text="Fila")
        self.tabla_tokens.heading("columna", text="Columna")
        
        # Configurar columnas
        self.tabla_tokens.column("lexema", width=200, anchor=tk.W)
        self.tabla_tokens.column("categoria", width=150, anchor=tk.W)
        self.tabla_tokens.column("fila", width=50, anchor=tk.CENTER)
        self.tabla_tokens.column("columna", width=50, anchor=tk.CENTER)
        
        # Configurar tags para colores
        for categoria, color in self.colores_categoria.items():
            tag_name = categoria.name
            self.tabla_tokens.tag_configure(tag_name, foreground=color)
        
        # Scrollbar para la tabla
        scrollbar_tokens = ttk.Scrollbar(
            tokens_frame,
            orient=tk.VERTICAL,
            command=self.tabla_tokens.yview
        )
        self.tabla_tokens.configure(yscroll=scrollbar_tokens.set)
        
        self.tabla_tokens.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_tokens.pack(side=tk.RIGHT, fill=tk.Y)

        # Panel para Errores Léxicos
        errores_frame = ttk.LabelFrame(right_frame, text="Errores Léxicos")
        errores_frame.pack(fill=tk.BOTH, expand=True, pady=(5,0), ipady=5)
        
        self.texto_errores = scrolledtext.ScrolledText(
            errores_frame,
            wrap=tk.WORD,
            width=40,
            height=5,
            state=tk.DISABLED,
            font=('Consolas', 9)
        )
        self.texto_errores.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
             
    def analizar_codigo(self):
        """Analiza el código completo usando el analizador léxico"""
        self.limpiar_resultados()
        
        codigo = self.editor.get("1.0", tk.END)
        if not codigo.strip():
            messagebox.showinfo("Aviso", "Por favor ingresa código para analizar.")
            return
            
        try:
            tokens, errores = self.analizador.analizar(codigo)
            
            # Mostrar tokens en la tabla
            self.mostrar_tokens(tokens)
            
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
                
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al analizar el código: {str(e)}"
            )
        finally:
            self.texto_errores.config(state=tk.DISABLED)
    
    def mostrar_tokens(self, tokens):
        """Muestra los tokens en la tabla con sus colores correspondientes"""
        self.tabla_tokens.delete(*self.tabla_tokens.get_children())
        for token in tokens:
            self.tabla_tokens.insert(
                "",
                "end",
                values=(
                    token.lexema,
                    token.categoria.name,
                    token.fila,
                    token.columna
                ),
                tags=(token.categoria.name,)
            )

    def limpiar_resultados(self):
        """Limpia la tabla de tokens y el panel de errores"""
        self.tabla_tokens.delete(*self.tabla_tokens.get_children())
        self.texto_errores.config(state=tk.NORMAL)
        self.texto_errores.delete("1.0", tk.END)
        self.texto_errores.config(state=tk.DISABLED)

    def limpiar(self):
        """Limpia el editor y todos los resultados"""
        self.editor.delete("1.0", tk.END)
        self.limpiar_resultados()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazLexica(root) 
    root.mainloop()