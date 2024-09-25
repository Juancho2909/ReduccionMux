def PedirMinTerms():
    cadena = input("Ingrese la lista de MinTerms (separados por comas): ")
    
    if cadena=="" or cadena==" ":
        print("Ponga una lista válida")
        PedirMinTerms()
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


entrada = PedirMinTerms()
minterms = AlmacenarMinTerms(entrada)
cantidad_variables = CantidadVariables(minterms)


matriz_selectora = MatrizSelectora(cantidad_variables, minterms)

solucion_mux = Solucion(cantidad_variables, minterms)
solucion_final = MostrarSolucion(solucion_mux)
print(f"Matriz Selectora: {matriz_selectora}")
print(f"Solución Final Mux: {solucion_final}")
print(f"Cantidad de Variables: {cantidad_variables}")
