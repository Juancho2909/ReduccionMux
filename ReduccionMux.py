import tkinter as tk
from tkinter import messagebox

# Funciones del cálculo (ya conocidas)

def PedirMinTerms():
    cadena = minterms_entry.get()
    
    if cadena == "" or cadena == " ":
        messagebox.showerror("Error", "Por favor, ingrese una lista válida de MinTerms.")
        return None
    else:
        return cadena

def AlmacenarMinTerms(cadena_ejemplo):
    numeros = []  
    numero_temporal = ""  

    for caracter in cadena_ejemplo:
        if caracter.isdigit():
            numero_temporal += caracter  
        else:
            if numero_temporal:  
                numeros.append(int(numero_temporal))  
                numero_temporal = "" 

    if numero_temporal:  
        numeros.append(int(numero_temporal))

    return numeros

def CantidadVariables(cadena_ejemplo2):
    if not cadena_ejemplo2:  
        return 0

    numero = max(cadena_ejemplo2)  
    variables = 0
    exponente = 1 
    
    while exponente <= numero:
        variables += 1  
        exponente *= 2  

    return variables

def MatrizSelectora(cantidad_variables, arreglo_ejemplo2):
    variables_mux = 2 * (2 ** (cantidad_variables - 1))
    matriz_ceros = [[0 for _ in range(2)] for _ in range(variables_mux)]
    
    for contador in range(variables_mux):
        if contador < (variables_mux / 2):
            matriz_ceros[contador][0] = 0
        else:
            matriz_ceros[contador][0] = 1

    for contador in range(len(arreglo_ejemplo2)):
        matriz_ceros[arreglo_ejemplo2[contador]][1] = 1
            
    return matriz_ceros

def Solucion(variables_totales, arreglo_numerico):
    variables_mux = 2 ** variables_totales
    arreglo = [0] * variables_mux  
    longitud = len(arreglo_numerico)
    arreglo_nuevo_mux = [0] * (variables_mux // 2)
    
    for i in range(variables_mux):
        arreglo[i] = i

    for i in range(longitud):
        if arreglo_numerico[i] < variables_mux:  
            arreglo[arreglo_numerico[i]] = -1  
    
    for i in range(variables_mux // 2):
        if arreglo[i] == arreglo[i + ((variables_mux // 2))]:
            arreglo_nuevo_mux[i] = 1
        else:
            if arreglo[i + ((variables_mux // 2))] == -1:
                arreglo_nuevo_mux[i] = 2
            else:
                if arreglo[i] == -1:
                    arreglo_nuevo_mux[i] = 3
                else:
                    arreglo_nuevo_mux[i] = 0
            
    return arreglo_nuevo_mux

def MostrarSolucion(arreglo):
    longitud = len(arreglo)
    resultado = []  
    resultado.append('[')
    for i in range(longitud):
        if arreglo[i] == 2:
            resultado.append('A')  
            resultado.append(' ')
        elif arreglo[i] == 3:
            resultado.append('~A')
            resultado.append(' ')
        else:
            resultado.append(str(arreglo[i]))  
            resultado.append(' ')
    resultado.append(']')       
    return ''.join(resultado)  

def calcular_solucion():
    entrada = PedirMinTerms()
    if entrada:
        minterms = AlmacenarMinTerms(entrada)
        cantidad_variables = CantidadVariables(minterms)

        matriz_selectora = MatrizSelectora(cantidad_variables, minterms)
        solucion_mux = Solucion(cantidad_variables, minterms)
        solucion_final = MostrarSolucion(solucion_mux)
        
        matriz_texto = "\n".join([str(fila) for fila in matriz_selectora])
        
        # Mostrar la matriz selectora con scrollbar
        matriz_output.config(state='normal')
        matriz_output.delete("1.0", tk.END)
        matriz_output.insert(tk.END, matriz_texto)
        matriz_output.config(state='disabled')
        
        # Mostrar la solución final con scrollbar
        solucion_output.config(state='normal')
        solucion_output.delete("1.0", tk.END)
        solucion_output.insert(tk.END, solucion_final)
        solucion_output.config(state='disabled')
        
        variables_output.config(text=str(cantidad_variables))
        
        # Abrir ventana para mostrar el MUX gráficamente
        mostrar_mux_grafico(cantidad_variables, solucion_mux)

def mostrar_mux_grafico(cantidad_variables, solucion_mux):
    mux_window = tk.Toplevel(root)
    mux_window.title("MUX Gráfico")

    canvas = tk.Canvas(mux_window, width=600, height=600, bg="white")
    canvas.pack()

    # Dibujar el multiplexor con entradas, selectores y salida
    mux_width = 200
    mux_height = 150
    mux_x = 150
    mux_y = 200

    # Dibujar el rectángulo del MUX
    canvas.create_rectangle(mux_x, mux_y, mux_x + mux_width, mux_y + mux_height, fill="lightgray")

    # Dibujar las entradas del MUX
    num_inputs = 2 ** cantidad_variables
    spacing = mux_height / num_inputs
    input_positions = []
    
    for i in range(num_inputs):
        input_y = mux_y + i * spacing + spacing / 2
        input_positions.append((mux_x - 50, input_y))
        canvas.create_line(mux_x - 50, input_y, mux_x, input_y)  # Línea de entrada
        canvas.create_text(mux_x - 60, input_y, text=f"I{i}")  # Etiqueta de entrada

    # Dibujar la salida del MUX
    output_y = mux_y + mux_height / 2
    canvas.create_line(mux_x + mux_width, output_y, mux_x + mux_width + 50, output_y)  # Línea de salida
    canvas.create_text(mux_x + mux_width + 60, output_y, text="Salida")  # Etiqueta de salida

    # Dibujar selectores debajo de las entradas
    selector_spacing = 50
    selector_y = mux_y + mux_height + 20
    
    for i in range(cantidad_variables):
        selector_x = mux_x + (i + 1) * (mux_width / (cantidad_variables + 1))
        canvas.create_line(selector_x, selector_y, selector_x, mux_y)  # Línea del selector
        canvas.create_text(selector_x, selector_y + 20, text=f"Sel{i}")  # Etiqueta del selector

    # Dibujar las conexiones de las entradas según la solución
    for i, val in enumerate(solucion_mux):
        if val == 1:
            canvas.create_line(mux_x - 50, input_positions[i][1], mux_x + mux_width, output_y, fill="green", width=2)

# Crear la ventana principal
root = tk.Tk()
root.title("Calculadora de MinTerms")
root.geometry("600x600")
root.resizable(True, True)

# Entrada de MinTerms
tk.Label(root, text="Ingrese la lista de MinTerms (separados por comas):").pack(pady=10)
minterms_entry = tk.Entry(root, width=50)
minterms_entry.pack(pady=10)

# Botón para calcular
calcular_button = tk.Button(root, text="Calcular", command=calcular_solucion)
calcular_button.pack(pady=20)

# Frame con scrollbar para la matriz selectora
matriz_frame = tk.Frame(root)
matriz_frame.pack(pady=10, fill='both', expand=True)

scrollbar_matriz = tk.Scrollbar(matriz_frame)
scrollbar_matriz.pack(side=tk.RIGHT, fill=tk.Y)

tk.Label(matriz_frame, text="Matriz Selectora:").pack()

matriz_output = tk.Text(matriz_frame, width=40, height=10, yscrollcommand=scrollbar_matriz.set, state='disabled')
matriz_output.pack(fill='both', expand=True)
scrollbar_matriz.config(command=matriz_output.yview)

# Frame con scrollbar para la solución final
solucion_frame = tk.Frame(root)
solucion_frame.pack(pady=10, fill='both', expand=True)

scrollbar_solucion = tk.Scrollbar(solucion_frame)
scrollbar_solucion.pack(side=tk.RIGHT, fill=tk.Y)

tk.Label(solucion_frame, text="Solución Final Mux:").pack()

solucion_output = tk.Text(solucion_frame, width=40, height=10, yscrollcommand=scrollbar_solucion.set, state='disabled')
solucion_output.pack(fill='both', expand=True)
scrollbar_solucion.config(command=solucion_output.yview)

# Mostrar la cantidad de variables
tk.Label(root, text="Cantidad de Variables:").pack()
variables_output = tk.Label(root, text="0")
variables_output.pack()

root.mainloop()
