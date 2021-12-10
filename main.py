#Se importan tanto las funciones contenidas en el archivo ¨operaciones¨, como las funciones de la libreria getpass.
import operaciones as op
from getpass import getpass

# Se declaran las variables que funcionarán por default para el usuario y contraseña 
usuario = 'juan'
contraseña = 'juan2021'

#Se crea una función de login que servirá para comparar el usuario y contraseña ingresados con los establecidos por default, entonces será True si ambos coinciden; pero, False si no coinciden.

def login():

    usuarioinput = input('Ingresa tu usuario: ')
    contraseñainput = getpass('Ingresa tu contraseña: ')

    if (usuarioinput == usuario) & (contraseñainput == contraseña):
        print(f'Bienvenido de nuevo, {usuarioinput}')
        return True
    else:
        return False

#Se crea una función para que el usuario pueda escoger entre una serie de acciones (opciones) a realizar, definidas en el módulo de operaciones.
def analisis(opcion):
    opciones = {
        1: op.opcion1,
        2: op.opcion2,
        3: op.opcion3,
        4: op.opcion4
    }
    func = opciones.get(opcion)

    return func()

#Se definen las variables asociadas al usuario (si el usuario sigue activo,  es decir, con sus datos ingresados, se define como ¨activo¨; en caso contrario, se le pide ingresar de nuevo sus datos). 
#Asi mismo, se crea una variable que servirá posteriormente para romper el bucle while, esta variable es ¨funalizar¨
activo = login()
finalizar = 'n' or 'N'

#Se crea un bucle while asociado a la funcion analisis, en el que se imprimen las opciones para que el usuario pueda interactuar con ellas y escoger una.
#De la  misma forma, se establece una condicionante dentro del bucle while, conectada con la funcion ¨activo¨, y que permite al usuario ingresar sus datos de nuevo.

while finalizar != ('y' or 'Y'):

    if not activo:
        print('Ingresa de nuevo')
        activo = login()
    else:
        print('''
        Opciones disponibles:
            1. Ver los productos con mayor número de ventas y mayor número de búsquedas.
            2. Productos con mejores y peores reseñas.
            3. Total de ingresos y ventas promedio mensuales, total anual y meses con más ventas al año.
            4. Imprimir el análisis.
        ''')

        analisis(int(input('Escriba la acción que desea realizar: ')))
        finalizar = input('¿Salir? (y/n): ')
