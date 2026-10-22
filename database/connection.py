import os
from pathlib import Path
from types import SimpleNamespace

import mysql.connector
from mysql.connector import Error

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass


class BancoMySQL:
    """Conexão MySQL para uso local com XAMPP."""

    def __init__(self):
        self.config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "exercicios_css"),
        }

    def _conectar_servidor(self):
        return mysql.connector.connect(
            host=self.config["host"],
            port=self.config["port"],
            user=self.config["user"],
            password=self.config["password"],
        )

    def garantir_banco(self):
        conexao = self._conectar_servidor()
        try:
            cursor = conexao.cursor()
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{self.config['database']}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            conexao.commit()
            cursor.close()
        finally:
            conexao.close()

    def conectar(self):
        return mysql.connector.connect(
            host=self.config["host"],
            port=self.config["port"],
            user=self.config["user"],
            password=self.config["password"],
            database=self.config["database"],
        )

    def executar(self, sql, parametros=()):
        conexao = self.conectar()
        cursor = None
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute(sql, parametros)
            conexao.commit()
            return SimpleNamespace(
                lastrowid=cursor.lastrowid,
                rowcount=cursor.rowcount,
            )
        except Error:
            conexao.rollback()
            raise
        finally:
            if cursor is not None:
                cursor.close()
            conexao.close()

    def buscar_um(self, sql, parametros=()):
        conexao = self.conectar()
        cursor = None
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute(sql, parametros)
            return cursor.fetchone()
        finally:
            if cursor is not None:
                cursor.close()
            conexao.close()

    def buscar_todos(self, sql, parametros=()):
        conexao = self.conectar()
        cursor = None
        try:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute(sql, parametros)
            return cursor.fetchall()
        finally:
            if cursor is not None:
                cursor.close()
            conexao.close()
