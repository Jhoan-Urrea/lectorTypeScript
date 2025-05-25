#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pruebas específicas para el analizador léxico de TypeScript.
"""

import sys
import os
import unittest
import pytest

# Añadir la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analizadores.lexer import AnalizadorLexico
from tokens import Categoria, Token

class TestTypeScript(unittest.TestCase):
    def setUp(self):
        self.analizador = AnalizadorLexico()
    
    def test_tipos_primitivos(self):
        codigo = """
        let numero: number = 42;
        let texto: string = "Hola";
        let booleano: boolean = true;
        let nulo: null = null;
        let indefinido: undefined = undefined;
        let simbolo: symbol = Symbol();
        let objeto: object = {};
        let cualquiera: any = "cualquier cosa";
        let desconocido: unknown = "valor desconocido";
        let nunca: never = (() => { throw new Error(); })();
        let vacio: void = undefined;
        """
        tokens, errores = self.analizador.analizar(codigo)
        self.assertEqual(len(errores), 0, "No debería haber errores")
        
        # Verificar que los tipos primitivos son reconocidos correctamente
        tipos_primitivos = [token for token in tokens if token.categoria == Categoria.TIPO_PRIMITIVO]
        self.assertEqual(len(tipos_primitivos), 11, "Debería haber 11 tipos primitivos")
    
    def test_tipos_genericos(self):
        codigo = """
        interface Array<T> {
            length: number;
            push(...items: T[]): number;
            pop(): T | undefined;
        }
        
        type Lista<T> = T[];
        type Par<K, V> = [K, V];
        type Promesa<T> = Promise<T>;
        """
        tokens, errores = self.analizador.analizar(codigo)
        self.assertEqual(len(errores), 0, "No debería haber errores")
        
        # Verificar que los tipos genéricos son reconocidos correctamente
        tipos_genericos = [token for token in tokens if token.categoria == Categoria.TIPO_GENERICO]
        self.assertTrue(len(tipos_genericos) > 0, "Debería haber tipos genéricos")
    
    def test_tipos_union(self):
        codigo = """
        type ID = string | number;
        type Estado = "activo" | "inactivo" | "pendiente";
        type Numero = 1 | 2 | 3 | 4 | 5;
        type Combinado = string | number | boolean;
        """
        tokens, errores = self.analizador.analizar(codigo)
        self.assertEqual(len(errores), 0, "No debería haber errores")
        
        # Verificar que los tipos union son reconocidos correctamente
        tipos_union = [token for token in tokens if token.categoria == Categoria.TIPO_UNION]
        self.assertTrue(len(tipos_union) > 0, "Debería haber tipos union")
    
    def test_tipos_intersection(self):
        codigo = """
        type Empleado = Usuario & {
            departamento: string;
            salario: number;
        };
        
        type ConMetodos = {
            metodo1(): void;
        } & {
            metodo2(): number;
        };
        """
        tokens, errores = self.analizador.analizar(codigo)
        self.assertEqual(len(errores), 0, "No debería haber errores")
        
        # Verificar que los tipos intersection son reconocidos correctamente
        tipos_intersection = [token for token in tokens if token.categoria == Categoria.TIPO_INTERSECCION]
        self.assertTrue(len(tipos_intersection) > 0, "Debería haber tipos intersection")
    
    def test_tipos_mapeados(self):
        codigo = """
        type Readonly<T> = {
            readonly [P in keyof T]: T[P];
        };
        
        type Partial<T> = {
            [P in keyof T]?: T[P];
        };
        
        type Pick<T, K extends keyof T> = {
            [P in K]: T[P];
        };
        """
        tokens, errores = self.analizador.analizar(codigo)
        self.assertEqual(len(errores), 0, "No debería haber errores")
        
        # Verificar que los tipos mapeados son reconocidos correctamente
        tipos_mapeados = [token for token in tokens if token.categoria == Categoria.TIPO_MAPPED]
        self.assertTrue(len(tipos_mapeados) > 0, "Debería haber tipos mapeados")
    
    def test_tipos_condicionales(self):
        codigo = """
        type Tipo<T> = T extends string ? "string" : "otro";
        type NoNulo<T> = T extends null | undefined ? never : T;
        type EsArray<T> = T extends any[] ? true : false;
        """
        tokens, errores = self.analizador.analizar(codigo)
        self.assertEqual(len(errores), 0, "No debería haber errores")
        
        # Verificar que los tipos condicionales son reconocidos correctamente
        tipos_condicionales = [token for token in tokens if token.categoria == Categoria.TIPO_CONDITIONAL]
        self.assertTrue(len(tipos_condicionales) > 0, "Debería haber tipos condicionales")
    
    def test_tipos_template_literals(self):
        codigo = """
        type Saludo<T extends string> = `Hola ${T}`;
        type Despedida<T extends string> = `Adiós ${T}`;
        type Mensaje<T extends string, U extends string> = `${T} ${U}`;
        """
        tokens, errores = self.analizador.analizar(codigo)
        self.assertEqual(len(errores), 0, "No debería haber errores")
        
        # Verificar que los tipos template literals son reconocidos correctamente
        tipos_template = [token for token in tokens if token.categoria == Categoria.TIPO_TEMPLATE_LITERAL]
        self.assertTrue(len(tipos_template) > 0, "Debería haber tipos template literals")
    
    def test_tipos_index(self):
        codigo = """
        type Propiedades<T> = T[keyof T];
        type Valor<T, K extends keyof T> = T[K];
        type Elemento<T extends any[]> = T[number];
        """
        tokens, errores = self.analizador.analizar(codigo)
        self.assertEqual(len(errores), 0, "No debería haber errores")
        
        # Verificar que los tipos index son reconocidos correctamente
        tipos_index = [token for token in tokens if token.categoria == Categoria.TIPO_INDEX]
        self.assertTrue(len(tipos_index) > 0, "Debería haber tipos index")
    
    def test_tipos_keyof(self):
        codigo = """
        type Claves<T> = keyof T;
        type Metodos<T> = {
            [K in keyof T]: T[K] extends Function ? K : never;
        }[keyof T];
        """
        tokens, errores = self.analizador.analizar(codigo)
        self.assertEqual(len(errores), 0, "No debería haber errores")
        
        # Verificar que los tipos keyof son reconocidos correctamente
        tipos_keyof = [token for token in tokens if token.categoria == Categoria.TIPO_KEYOF]
        self.assertTrue(len(tipos_keyof) > 0, "Debería haber tipos keyof")
    
    def test_tipos_infer(self):
        codigo = """
        type Retorno<T> = T extends (...args: any[]) => infer R ? R : any;
        type Elemento<T> = T extends (infer U)[] ? U : never;
        type Promesa<T> = T extends Promise<infer U> ? U : never;
        """
        tokens, errores = self.analizador.analizar(codigo)
        self.assertEqual(len(errores), 0, "No debería haber errores")
        
        # Verificar que los tipos infer son reconocidos correctamente
        tipos_infer = [token for token in tokens if token.categoria == Categoria.TIPO_INFER]
        self.assertTrue(len(tipos_infer) > 0, "Debería haber tipos infer")

if __name__ == '__main__':
    unittest.main() 