# TAREAS PENDIENTES
# - CREAR NUEVAS NOTAS
# - MOSTRAR ESTADO ABAJO, EDITANDO...
# - ELIMINAR NOTAS
# - QUITAR EL BUCLE Y QUE SE ACTUALICE CADA VEZ QUE TOCO UNA TECLA
# - SEPARAR EN FUNCIONES EN EL MISMO ARCHIVO
# - SEPARAR EN FUNCIONES EN VARIOS ARCHIVOS

# Librerias
import curses
import os
import time
import textwrap

# Archivos mios
import functions

PATH_NOTES = '/data'
EXTENTION_FILES = '.tm'
INIT_PROMT_NEW_FILE = 'NUEVO - Nombre'
INIT_PROMT_DELETE_FILE = 'ELIMINAR - Nombre'

# Muestra leyendas en el footer
def showStatus(footer_win, width, height, footer_height, promt_height, editing, cursor_y, cursor_x):
    yy = str(cursor_y)
    xx = str(cursor_x)
    footer_win.clear()
    footer_win.border('|', '|', '-', '-', '+', '+', '+', '+')
    if (editing):
        footer_win.addstr(1, 1, "[" + yy + ", " + xx + "]  Editando...")
    # footer_win.addstr(2, 1, "   - Flecha arriba/abajo: Navegar en el listado de notas")
    footer_win.addstr(3, 1, "   [Enter]: Edit  [Escape]: Save and close  [/]: Promt [new, del]  [n]: new file  [d]: del file")
    footer_win.refresh()


# Dibuja el prompt
def showPromt(promt_win, cursor_prompt_y, cursor_prompt_x, text, color):
    promt_win.clear()
    promt_win.border('|', '|', '-', '-', '+', '+', '+', '+')
    if (color is not None):
        promt_win.addstr(1, 1, text, color)
    else:
        promt_win.addstr(1, 1, text)
    promt_win.move(cursor_prompt_y + 1, cursor_prompt_x + 1)
    promt_win.refresh()

def hidePromt(promt_win):
    promt_win.clear()
    promt_win.refresh()


# Genera un nuevo archivo
def addNewFile(name):
    name_new_file = root_dir = os.getcwd() + PATH_NOTES + "/" + name + EXTENTION_FILES
    with open(name_new_file, "w") as newfile:
        newfile.write("...")
    root_dir = os.getcwd() + PATH_NOTES
    text_files = [file for file in os.listdir(root_dir) if file.endswith(EXTENTION_FILES)]
    return text_files


# Remover un archivo
def removeNewFile(name):
    text_files = None
    name_new_file = root_dir = os.getcwd() + PATH_NOTES + "/" + name + EXTENTION_FILES
    try:
        os.remove(name_new_file)
        root_dir = os.getcwd() + PATH_NOTES
        text_files = [file for file in os.listdir(root_dir) if file.endswith(EXTENTION_FILES)]
    except OSError as e:
        print("Error al eliminar el archivo:", e)
    return text_files


def main(stdscr):
    curses.curs_set(0)
    # stdscr.nodelay(1) # Es para que no espere que presione una tecla
    # screen = curses.initscr()

    # Definir los pares de colores
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN) # Color nota seleccionada Activa
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN) # Color nota seleccionada Editando
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED) # Color error (letra - fondo)
    editing = False
    promting = False
    height, width = stdscr.getmaxyx()

    left_width = width * 40 // 100
    right_width = width - left_width - 1 # Dejo un caracter de espacio

    # INIT PROMT
    promt_height = 3
    promt_win = stdscr.subwin(promt_height, width, height - promt_height, 0)
    # promt_win.border('|', '|', '-', '-', '+', '+', '+', '+')

    # INIT FOOTER
    footer_height = 5
    footer_win = stdscr.subwin(footer_height, width, height - footer_height - promt_height, 0)
    showStatus(footer_win, width, height, footer_height, promt_height, editing, 0, 0)


    # INIT LEFT
    left_win = stdscr.subwin(height - footer_height - promt_height, left_width, 0, 0)
    # left_win.box()

    # INIT RIGHT
    right_win = stdscr.subwin(height - footer_height - promt_height, right_width, 0, left_width + 1)
    #right_win.box()

    editor_win = stdscr.subwin(height - footer_height - promt_height, right_width, 0, left_width + 1)

    root_dir = os.getcwd() + PATH_NOTES
    text_files = [file for file in os.listdir(root_dir) if file.endswith(EXTENTION_FILES)]

    selected_index = 0
    # Limpio las secciones
    # left_win.clear()
    # right_win.clear()
    # footer_win.clear()

    # ----------------------------------------------------------------------------
    # INIT WHILE
    # ----------------------------------------------------------------------------
    while True:
        right_win.clear()
        left_win.clear()
        left_win.border('|', '|', '-', '-', '+', '+', '+', '+')

        # Busco las notas y las agrego a la izquierda
        for i, file_name in enumerate(text_files):
            file_name = file_name[:-len(EXTENTION_FILES)]
            if i == selected_index:
                left_win.addstr(i + 1, 1, file_name, curses.color_pair(1))
            else:
                left_win.addstr(i + 1, 1, file_name)

        selected_file = text_files[selected_index]
        file_path = os.path.join(root_dir, selected_file)

        # Leo la nota seleccionada y la agrego a la derecha
        with open(file_path, "r") as f:
            note_content = f.read()

        right_win.addstr(1, 0, note_content)

        left_win.refresh()
        right_win.refresh()
        promt_win.refresh()

        key = stdscr.getch()

        if key == ord('q') or key == ord('Q'):
            break
        elif key == curses.KEY_UP and selected_index > 0:
            selected_index -= 1
        elif key == curses.KEY_DOWN and selected_index < len(text_files) - 1:
            selected_index += 1
        if key == ord('/'):
            promt_text = ""
            cursor_prompt_y = 0
            cursor_prompt_x = 0
            promting = True
            curses.curs_set(1)

            # -----------------------------------------
            # Mientras escribo en el promt de abajo
            # -----------------------------------------
            while promting:
                showPromt(promt_win, cursor_prompt_y, cursor_prompt_x, promt_text, None)
                key = stdscr.getch()

                if key == 27: # Codigo ASCII para la tecla Escape
                    promting = False
                    promt_text = ""
                    hidePromt(promt_win)
                elif key == ord('\n'):
                    # acepto lo que escribo
                    promting = False
                elif key == curses.KEY_BACKSPACE or key == 127:
                    if cursor_prompt_x > 0:
                        cursor_prompt_x -= 1
                        promt_text = promt_text[:cursor_prompt_x]
                else: # Si no es una tecla de control entonces escribo sobre el contenido de la nota
                    if key >= 0 and key < 256:
                        character = chr(key)
                        if character.isprintable():
                            promt_text = promt_text[:cursor_prompt_x] + character
                            cursor_prompt_x += 1


            curses.curs_set(0)
            if (len(promt_text) > 0):
                # TODO AGREGAR COMANDO PARA BUSCAR NOTAS
                promt_array = promt_text.split(" ")
                if "new" in promt_array[0]:
                    text_files = addNewFile(promt_array[1])
                    selected_index = 0
                    result_promt = " Nota " + promt_array[1] + " generada"

                elif "del" in promt_array[0]:
                    text_files_aux = removeNewFile(promt_array[1])
                    selected_index = 0
                    if (text_files_aux is not None):
                        text_files = text_files_aux
                        result_promt = " Nota " + promt_array[1] + " eliminada"
                else:
                    result_promt = " ERROR: Comando invalido"
                showPromt(promt_win, cursor_prompt_y, cursor_prompt_x, result_promt, None)
                curses.napms(1000)
                hidePromt(promt_win)

        # GENERAR NUEVO ARCHIVO
        elif key == ord('n'):
            promt_text = INIT_PROMT_NEW_FILE + ': '
            cursor_prompt_y = 0
            cursor_prompt_x = 16
            promting = True
            curses.curs_set(1)

            while promting:
                showPromt(promt_win, cursor_prompt_y, cursor_prompt_x, promt_text, None)
                key = stdscr.getch()

                if key == 27: # Codigo ASCII para la tecla Escape
                    promting = False
                    promt_text = ""
                    hidePromt(promt_win)
                elif key == ord('\n'):
                    # acepto lo que escribo
                    promting = False
                elif key == curses.KEY_BACKSPACE or key == 127:
                    if cursor_prompt_x > 0:
                        cursor_prompt_x -= 1
                        promt_text = promt_text[:cursor_prompt_x]
                else: # Si no es una tecla de control entonces escribo sobre el contenido de la nota
                    if key >= 0 and key < 256:
                        character = chr(key)
                        if (character == ' '):
                            character = '_'
                        if character.isprintable():
                            promt_text = promt_text[:cursor_prompt_x] + character
                            cursor_prompt_x += 1
            curses.curs_set(0)
            if (len(promt_text) > 0):
                promt_array = promt_text.split(": ")
                color = curses.color_pair(1)
                if (promt_array[1]):
                    text_files = addNewFile(promt_array[1])
                    selected_index = 0
                    result_promt = " Nota " + promt_array[1] + " generada"
                else:
                    color = curses.color_pair(3)
                    result_promt = " ERROR: Archivo no generado"
                showPromt(promt_win, cursor_prompt_y, cursor_prompt_x, result_promt, color)
                curses.napms(1000)
                hidePromt(promt_win)


        # ELIMINAR ARCHIVO
        elif key == ord('d'):
            promt_text = INIT_PROMT_DELETE_FILE + ': ' + selected_file[:-len(EXTENTION_FILES)]
            cursor_prompt_y = 0
            cursor_prompt_x = 19
            promting = True
            curses.curs_set(1)

            while promting:
                showPromt(promt_win, cursor_prompt_y, cursor_prompt_x, promt_text, None)
                key = stdscr.getch()

                if key == 27: # Codigo ASCII para la tecla Escape
                    promting = False
                    promt_text = ""
                    hidePromt(promt_win)
                elif key == ord('\n'):
                    # acepto lo que escribo
                    promting = False
                elif key == curses.KEY_BACKSPACE or key == 127:
                    if cursor_prompt_x > 0:
                        cursor_prompt_x -= 1
                        promt_text = promt_text[:cursor_prompt_x]
                else: # Si no es una tecla de control entonces escribo sobre el contenido de la nota
                    if key >= 0 and key < 256:
                        character = chr(key)
                        if (character == ' '):
                            character = '_'
                        if character.isprintable():
                            promt_text = promt_text[:cursor_prompt_x] + character
                            cursor_prompt_x += 1
            curses.curs_set(0)
            if (len(promt_text) > 0):
                promt_array = promt_text.split(": ")
                color = curses.color_pair(1)
                if (promt_array[1]):
                    text_files_aux = removeNewFile(promt_array[1])
                    selected_index = 0
                    if (text_files_aux is not None):
                        text_files = text_files_aux
                        result_promt = " Nota " + promt_array[1] + " eliminada"
                else:
                    color = curses.color_pair(3)
                    result_promt = " ERROR: Comando invalido"
                showPromt(promt_win, cursor_prompt_y, cursor_prompt_x, result_promt, color)
                curses.napms(1000)
                hidePromt(promt_win)


        elif key == curses.KEY_ENTER or key == ord('\n'):
            # Cambio de color el cursor
            for i, file_name in enumerate(text_files):
                if i == selected_index:
                    left_win.addstr(i + 1, 1, file_name, curses.color_pair(2))
            else:
                left_win.addstr(i + 1, 1, file_name)
            left_win.refresh()

            # Agrego el texto
            editor_text = note_content.strip()
            editor_text_lines = editor_text.split('\n')
            editor_text_height = height - footer_height - promt_height

            # Seteo posicion inicial de cursor
            cursor_y = 0 # len(editor_text_lines[:editor_text_height]) - 1
            cursor_x = 0 # len(editor_text_lines[cursor_y])
            # Pongo visible el cursor
            editing = True
            hasChanges = False
            curses.curs_set(1)

            # Actualizo estados footer
            showStatus(footer_win, width, height, footer_height, promt_height, editing, cursor_y, cursor_x)

            # -----------------------------------------
            # Mientras edito una nota corre este while
            # -----------------------------------------
            while editing:
                editor_win.clear()
                editor_win.border('|', '|', '-', '-', '+', '+', '+', '+')
                for i, line in enumerate(editor_text_lines[:editor_text_height]):
                    editor_win.addstr(i + 1, 1, line)

                editor_win.move(cursor_y + 1, cursor_x + 1)
                editor_win.refresh()
                key = stdscr.getch()

                if key == 27: # Codigo ASCII para la tecla Escape
                    editing = False
                elif key == curses.KEY_UP and cursor_y > 0:
                    cursor_y -= 1
                    if cursor_x >= len(editor_text_lines[cursor_y]):
                        cursor_x = len(editor_text_lines[cursor_y])
                elif key == curses.KEY_DOWN and cursor_y < editor_text_height - 1:
                    if cursor_y < len(editor_text_lines)-1:
                        cursor_y += 1
                    if cursor_x >= len(editor_text_lines[cursor_y]):
                        cursor_x = len(editor_text_lines[cursor_y])
                elif key == curses.KEY_LEFT and cursor_x > 0:
                    cursor_x -= 1
                elif key == curses.KEY_RIGHT and cursor_x < right_width - 4:
                    if cursor_x < len(editor_text_lines[cursor_y]):
                        cursor_x += 1
                elif key == curses.KEY_BACKSPACE or key == 127:
                    hasChanges = True
                    if cursor_x > 0:
                        editor_text_lines[cursor_y] = editor_text_lines[cursor_y][:cursor_x - 1] + editor_text_lines[cursor_y][cursor_x:]
                        cursor_x -= 1
                    elif cursor_y > 0:
                        cursor_x = len(editor_text_lines[cursor_y - 1])
                        editor_text_lines[cursor_y - 1] += editor_text_lines[cursor_y]
                        del editor_text_lines[cursor_y]
                        cursor_y -= 1
                        editor_text_height -= 1
                elif key == ord('\n'):
                    if cursor_y < editor_text_height - 1:
                        new_line = editor_text_lines[cursor_y][cursor_x:]
                        editor_text_lines[cursor_y] = editor_text_lines[cursor_y][:cursor_x]
                        editor_text_lines.insert(cursor_y + 1, new_line)
                        editor_text_height += 1
                        cursor_y += 1
                        cursor_x = 0
                else: # Si no es una tecla de control entonces escribo sobre el contenido de la nota
                    if key >= 0 and key < 256:
                        hasChanges = True
                        character = chr(key)
                        if character.isprintable():
                            editor_text_lines[cursor_y] = editor_text_lines[cursor_y][:cursor_x] + character + editor_text_lines[cursor_y][cursor_x:]
                            if (cursor_x == right_width - 2):
                                if cursor_y < editor_text_height - 1:
                                    new_line = editor_text_lines[cursor_y][cursor_x:]
                                    editor_text_lines[cursor_y] = editor_text_lines[cursor_y][:cursor_x]
                                    editor_text_lines.insert(cursor_y + 1, new_line)
                                    editor_text_height += 1
                                    cursor_y += 1
                                    cursor_x = 1
                            else:
                                cursor_x += 1

                # Actualizo estados footer
                showStatus(footer_win, width, height, footer_height, promt_height, editing, cursor_y, cursor_x)

            if (hasChanges):
                editor_text = '\n'.join(editor_text_lines)
                with open(file_path, "w") as f:
                    f.write(editor_text)

            curses.curs_set(0)

        # Agregar un pequeño retraso para reducir el consumo de recursos del procesador
        # curses.napms(50)

curses.wrapper(main)


