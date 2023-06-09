import curses
import os

def get_new_file(stdscr):
    curses.echo()  # Habilitar la escritura de entrada del usuario
    stdscr.addstr(0, 0, "Ingrese el nombre del archivo para la nueva nota: ")
    stdscr.refresh()
    nombre_archivo = stdscr.getstr(1, 0).decode()  # Capturar la entrada del usuario
    curses.noecho()  # Deshabilitar la escritura de entrada del usuario
    return nombre_archivo
