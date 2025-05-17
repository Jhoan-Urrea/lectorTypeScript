#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Punto de entrada principal para el analizador léxico.
Este archivo inicia la interfaz gráfica.
"""

import tkinter as tk
from gui.interfaz import InterfazLexer

def main():
    """Función principal que inicia la aplicación."""
    root = tk.Tk()
    app = InterfazLexer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
