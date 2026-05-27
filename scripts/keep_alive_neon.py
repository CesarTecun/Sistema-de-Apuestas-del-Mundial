#!/usr/bin/env python3
"""
Script para mantener activo el compute de Neon (ambas bases de datos).
Neon tiene scale-to-zero que suspende la computacion tras ~5 min de inactividad,
causando cold-start de 5-10 segundos en la primera peticion.

Este script conecta DIRECTAMENTE a ambas bases de datos Neon con psycopg2
cada 2 minutos para evitar la suspension. No depende del microservicio.

Uso:
    python scripts/keep_alive_neon.py

Para detener: Ctrl+C
"""

import time
import sys

# Base de datos del microservicio (proyecto 'tablero')
MARCADOR_DB = "postgresql://neondb_owner:npg_eZ7sPF3fGglv@ep-small-poetry-aqil41c7.c-8.us-east-1.aws.neon.tech/neondb?sslmode=require"

# Base de datos general de Django (proyecto 'BaseQuiniela')
DJANGO_DB = "postgresql://neondb_owner:npg_pQrLmJXlZ78I@ep-falling-cherry-aqc89mqe.c-8.us-east-1.aws.neon.tech:5432/quiniela?sslmode=require"

INTERVAL_SECONDS = 120  # 2 minutos (menor que el cold-start de Neon)


def ping_db(conn_str, label):
    try:
        import psycopg2
        start = time.time()
        conn = psycopg2.connect(conn_str, connect_timeout=10)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close()
        conn.close()
        elapsed = (time.time() - start) * 1000
        print(f"[{time.strftime('%H:%M:%S')}] {label} OK  ({elapsed:.0f}ms)")
        return True
    except ImportError:
        print(f"[{time.strftime('%H:%M:%S')}] {label} SKIP  (psycopg2 no instalado)")
        return False
    except Exception as exc:
        print(f"[{time.strftime('%H:%M:%S')}] {label} FAIL  {exc}")
        return False


def main():
    print("Keep-alive para Neon (directo a BD) iniciado.")
    print(f"Intervalo: {INTERVAL_SECONDS}s")
    print("Presiona Ctrl+C para detener.\n")

    while True:
        ping_db(MARCADOR_DB, "TABLERO")
        ping_db(DJANGO_DB, "QUINIELA")
        print()
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nKeep-alive detenido.")
        sys.exit(0)
