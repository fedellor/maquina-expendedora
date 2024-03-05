class Automata:
    def __init__(self, alfabeto, estados, estados_aceptacion, transiciones):
        self.alfabeto = alfabeto
        self.estados = estados
        self.estados_aceptacion = estados_aceptacion
        self.transiciones = transiciones
    
    @staticmethod
    def parse_transition_line(line):
        """
        Método estático que parsea una línea de transición del archivo.
        devuelve Una lista de listas con las transiciones limpias.
        """
        # Elimina los espacios en blanco alrededor de cada estado y divide la línea en partes basadas en los espacios
        cleaned_transition_line = [state.strip().split() for state in line if state.strip()]
        return cleaned_transition_line

    @classmethod
    def from_file(cls, nombre_archivo):
        """
        Método de clase que crea una instancia de la clase Automata a partir de un archivo de definición.
        """
        with open(nombre_archivo, 'r') as file:
            lineas = file.readlines()
        
        # Extrae los estados, estados de aceptación y alfabeto del archivo
        estados_linea = lineas[0].strip('#').split()[1:] # El # es el divisor y se usa el [1:] para coger el primer estado de verdad
        estados_aceptacion_linea = lineas[1].strip('#').split()[1:] # Ya que si se cpge el [0] se cogería el número de estados/de elementos en el alfabeto
        estados_aceptacion = set(estados_aceptacion_linea)
        alfabeto_linea = lineas[2].strip('#').split()[1:]
        
        transiciones = {}
        # Itera sobre las líneas del archivo que contienen las transiciones
        for i in range(4, len(lineas)):
            transition_line = lineas[i].strip().split('#')
            # Llama al método estático para limpiar la línea de transición
            cleaned_transition_line = cls.parse_transition_line(transition_line)
            # Asocia los estados de origen con las transiciones en un diccionario
            transiciones[estados_linea[i-4]] = dict(zip(alfabeto_linea, cleaned_transition_line))
        
        # Retorna una instancia de la clase Automata con los parámetros extraídos del archivo
        return cls(alfabeto_linea, estados_linea, estados_aceptacion, transiciones)

    def procesar_cadena(self, cadena):
        if not set(cadena).issubset(self.alfabeto):
            print("Error: La cadena contiene símbolos que no están en el alfabeto.")
            return
        
        estado_inicial = self.estados[0]  # El primer estado leído en la línea de estados
        
        balance = 0 # El balance empieza en 0
        estado_actual = [estado_inicial]
        camino_transiciones = []
        estados_numericos = [] # Lista para guardar los estados con números para poder calcular el balance
        
        estados_por_cadena = []  # Lista para almacenar los estados visitados en orden
        estados_finales = set()  # Conjunto para almacenar los estados finales
        
        # Se añade el estado inicial a la lista de estados visitados
        estados_por_cadena.append(estado_inicial)
        
        for simbolo in cadena:
            nuevos_estados = set()
            # Itera sobre los estados actuales del autómata
            for estado in estado_actual:
                # Verifica si el estado tiene transiciones definidas
                if estado in self.transiciones:
                    # Obtiene las transiciones del estado actual
                    transiciones_estado_actual = self.transiciones[estado]
                    
                    # Verifica si hay una transición para el símbolo actual
                    if simbolo in transiciones_estado_actual:
                        # Si el símbolo es un espacio en blanco, pasa al siguiente símbolo
                        if simbolo == ' ':
                            continue
                        
                        # Obtiene los posibles estados siguientes para el símbolo actual
                        siguientes_estados = transiciones_estado_actual[simbolo]
                        
                        # Itera sobre los posibles estados siguientes
                        for siguiente_estado in siguientes_estados:
                            # Añade la transición al camino de transiciones
                            camino_transiciones.append((estado, siguiente_estado, simbolo))
                            # Añade el estado siguiente a la lista de nuevos estados
                            nuevos_estados.add(siguiente_estado)
                        
                        # Actualiza el estado siguiente al último estado de la lista de estados siguientes
                        siguiente_estado = siguientes_estados[-1]
                        
                        # Actualiza el balance según el estado al que se transita
                        if siguiente_estado.startswith('q'):
                            nuevo_balance = float(siguiente_estado[1:]) / 10
                            balance = min(nuevo_balance, 3.5)
                        
                        # Si el estado siguiente es numérico, lo añade a la lista de estados numéricos
                        if siguiente_estado[1:].isdigit():
                            estados_numericos.append(siguiente_estado)
                        
                        # Imprime el balance después de la transición
                        print(f"Balance actual después de la transición '{estado}' -> '{siguiente_estado} con {simbolo}': {balance}")
                        
                        # Imprime el producto correspondiente al símbolo
                        if simbolo == 'a':
                            print("Se va a expedir el producto a con un precio de 0.5")
                        elif simbolo == 'b':
                            print("Se va a expedir el producto b con un precio de 1")
                        elif simbolo == 'c':
                            print("Se va a expedir el producto c con un precio de 2")
                        elif simbolo == 'd':
                            print("Devolución del dinero")
            
            # Actualiza el conjunto de estados actuales con los nuevos estados encontrados
            estado_actual = list(nuevos_estados)

            estados_por_cadena.extend(estado_actual)  # Se añaden los nuevos estados visitados a la lista
        
        # Se filtran los estados únicos manteniendo el orden original
        estados_por_cadena = [estado for i, estado in enumerate(estados_por_cadena) if estado not in estados_por_cadena[:i]]
        
        # Se almacenan los estados finales alcanzados después de procesar toda la cadena
        estados_finales.update(estado_actual)
        
        print("Camino de transiciones:")
        print("Estado actual, estado siguiente, símbolo")
        for transicion in camino_transiciones:
            print(transicion)
        
        # Se imprime la lista de estados visitados
        print("Estados por los que pasa la cadena:")
        print(estados_por_cadena)
        
        # Se imprime la lista de estados finales
        print("Últimos estados:")
        print(estados_finales)

automata = Automata.from_file(r'C:\Users\Suare\OneDrive\Documentos\Universidad\segundo año\segundo cuatri\automatas\practicas\boletin 2\definicion.txt')

while True:
    cadena = input("Introduce la cadena a procesar (o 'salir' para terminar): ")
    automata.procesar_cadena(cadena)
    if cadena.lower() == 'salir':
        break


