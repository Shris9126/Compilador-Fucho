import json
import re
import tkinter as tk
from tkinter import scrolledtext
import subprocess
import os


TOKEN_TYPES = {
    'PRINT': r'print',
    'ID': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'STRING': r'"([^"\\]|\\.)*?"',
    'SEMICOLON': r';',
    'PLAYER': r'player',
    'PLAYERC': r'playerC',
}


TOKEN_PATTERN = re.compile('|'.join(f'(?P<{type}>{pattern})' for type, pattern in TOKEN_TYPES.items()))


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


def lexer(code):
    matches = TOKEN_PATTERN.finditer(code)
    for match in matches:
        type = match.lastgroup
        value = match.group()
        yield Token(type, value)


class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CompFu")
        self.root.geometry("1500x800")  

        
        self.left_frame = tk.Frame(root, width=600, height=800, bg='#4CAF50') 
        self.left_frame.pack_propagate(False)  
        self.left_frame.pack(side=tk.LEFT)

        self.code_input = scrolledtext.ScrolledText(self.left_frame, width=50, height=25, bg='#FFFFFF') 
        self.code_input.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        
        self.right_frame = tk.Frame(root, width=250, height=800, bg='#2196F3')  
        self.right_frame.pack_propagate(False)
        self.right_frame.pack(side=tk.RIGHT)

        self.tokens_text = scrolledtext.ScrolledText(self.right_frame, width=80, height=25, bg='#FFFFFF')  
        self.tokens_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        
        self.bottom_frame = tk.Frame(root, width=400, height=200, bg='#803493')  
        self.bottom_frame.pack_propagate(False)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

               
        label_text = tk.Label(self.bottom_frame, text="CompFu - Compilador de Estadísitcas de Fútbol\n Datos sobre la liga española 2023/2024", font=("Helvetica", 16, "bold"), bg='#803493', fg='white')
        label_text.pack(pady=5)

        self.compile_button = tk.Button(self.bottom_frame, text="Compilar", command=self.compile_code, bg='#FFF')  
        self.compile_button.pack(pady=10)

        self.generate_exe_button = tk.Button(self.bottom_frame, text="Generar Ejecutable", command=self.generate_executable, bg='#FFF')  
        self.generate_exe_button.pack(pady=10)

        self.output_text = scrolledtext.ScrolledText(self.bottom_frame, width=120, height=5, bg='#FFFFFF')  
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def compile_code(self):
        code = self.code_input.get("1.0", tk.END)
        tokens = lexer(code)
        self.output_text.delete(1.0, tk.END)
        self.tokens_text.delete(1.0, tk.END)

        player_names = [] 
        for token in tokens:
            self.tokens_text.insert(tk.END, f"Found {token.type} token: {token.value}\n")
            if token.type == 'PRINT':
                
                continue
            elif token.type == 'LPAREN':
                
                continue
            elif token.type == 'STRING':
                
                string_value = token.value[1:-1]  
                self.output_text.insert(tk.END, f"{string_value}\n")
                player_names.append(string_value)  
            elif token.type == 'RPAREN':
                continue
            elif token.type == 'SEMICOLON':
                continue
            elif token.type == 'PLAYER':
                continue
            elif token.type == 'PLAYERC':
                continue

        if player_names:
            if len(player_names) == 1:
                self.print_player_info(player_names[0])
            elif len(player_names) == 2:
                self.compare_players(player_names[0], player_names[1])

    def print_player_info(self, player_name):
        try:
            with open('C:\\Users\\esteb\\Documents\\CompFU (Compilador de Fucho)\\goleadores.json',  encoding='utf-8') as file:
                data = json.load(file)
                jugadores = data.get('jugadores', [])
                for jugador in jugadores:
                    if jugador['name'] == player_name:
                        self.output_text.insert(tk.END, f"Equipo: {jugador['clubname']}\nPosicion: {jugador['position']}\nNacionalidad: {jugador['nationality']}\n")
                        break
        except FileNotFoundError:
            self.tokens_text.insert(tk.END, "Error: No se encontró el archivo 'jugadores.json'\n")
        except json.JSONDecodeError:
            self.tokens_text.insert(tk.END, "Error: Error al decodificar el archivo JSON\n")

    def compare_players(self, player1, player2):
        try:
            with open('C:\\Users\\esteb\\Documents\\CompFU (Compilador de Fucho)\\goleadores.json',  encoding='utf-8') as file:
                data = json.load(file)
                jugadores = data.get('jugadores', [])
                players_info = []
                for jugador in jugadores:
                    if jugador['name'] == player1 or jugador['name'] == player2:
                        players_info.append({
                            'name': jugador['name'],
                            'equipo': jugador['clubname'],
                            'posicion': jugador['position'],
                            'nacionalidad': jugador['nationality'],
                            'Goles': jugador['goals'],
                        })

                if len(players_info) == 2:
                    self.output_text.insert(tk.END, f"\nComparación entre {players_info[0]['name']} y {players_info[1]['name']}:\n")
                    for key in players_info[0].keys():
                        self.output_text.insert(tk.END, f"{key}: {players_info[0][key]} vs {players_info[1][key]}\n")
        except FileNotFoundError:
            self.tokens_text.insert(tk.END, "Error: No se encontró el archivo 'jugadores.json'\n")
        except json.JSONDecodeError:
            self.tokens_text.insert(tk.END, "Error: Error al decodificar el archivo JSON\n")

    def generate_executable(self):
        try:
            with open('temp_script.py', 'w') as temp_file:
                temp_file.write(self.code_input.get("1.0", tk.END))

            with open('temp_script.py', 'a') as temp_file:
                temp_file.write('\n\nif __name__ == "__main__":\n')
                temp_file.write('    try:\n')
                temp_file.write('        input("Presiona Enter para salir")\n')
                temp_file.write('    except EOFError:\n')
                temp_file.write('        pass\n')

            subprocess.run(['pyinstaller', 'temp_script.py', '--onefile', '--hidden-import', 'tkinter', '--hidden-import', 'tkinter.messagebox'], check=True)

            self.output_text.insert(tk.END, "Ejecutable generado con éxito: dist\\temp_script.exe\n")

        except subprocess.CalledProcessError as e:
            self.output_text.insert(tk.END, f"Error generando el ejecutable: {e}\n")

        finally:
            try:
                os.remove('temp_script.py')
            except OSError:
                pass
        try:
            with open('temp_script.py', 'w') as temp_file:
                temp_file.write(self.code_input.get("1.0", tk.END))

            with open('temp_script.py', 'a') as temp_file:
                temp_file.write('\n\ninput("Presiona Enter para salir")\n')

            subprocess.run(['pyinstaller', 'temp_script.py', '--onefile'], check=True)

            self.output_text.insert(tk.END, "Ejecutable generado con éxito: dist\\temp_script.exe\n")

        except subprocess.CalledProcessError as e:
            self.output_text.insert(tk.END, f"Error generando el ejecutable: {e}\n")

        finally:
            try:
                os.remove('temp_script.py')
            except OSError:
                pass


def cargar_jugadores():
    try:
        with open('C:\\Users\\esteb\\Documents\\CompFU (Compilador de Fucho)\\goleadores.json', encoding='utf-8') as file:
            data = json.load(file)
            return data.get('jugadores', [])
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = CompilerGUI(root)

    jugadores = cargar_jugadores()

    root.mainloop()
    input("Presiona Enter para salir")
