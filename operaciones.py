#Primero se importan los módulos necesarios para la elaboración de las funciones y las operaciones. 
#Los módulos a importar son: las variables declaradas en el archivo lifestore_file, y el módulo sys que contiene
#funciones de utilidad para poder exportar el análisis en un formato más amigable para el cliente
from lifestore_file import lifestore_products, lifestore_sales, lifestore_searches
import sys

#Se define una función que sirve para definir un elemento determinado de una lista y utilizarlo como divisor, para que todos los elementos más pequeños
#que este, se posicionen a la izquierda, y los elementos mayores, se posicionen a la derecha.
def dividir(arr, low, high, func):

    i = low - 1  
    divisor = arr[high] 

    for j in range(low, high):

        if func(arr[j]) < func(divisor):
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

#Se define una función que implementa una operación para ordernar los elementos de una lista considerando el elemento divisor establecido en la función anterior.
def sort(arr, func, low=0, high=None):
    if high is None:
        high = len(arr) - 1

    if low < high:
        div = dividir(arr, low, high, func)

        sort(arr, func, low, div - 1)
        sort(arr, func, div + 1, high)

#Se calcula el número total de productos contenidos en la variable lifestore_products 
productos_num = len(lifestore_products)

#Se elabora un diccionario que servirá posteriormente para interpretar los meses referidos en las fechas de venta
diccionario_meses = {
    1: 'Enero',
    2: 'Febrero',
    3: 'Marzo',
    4: 'Abril',
    5: 'Mayo',
    6: 'Junio',
    7: 'Julio',
    8: 'Augosto',
    9: 'Septiembre',
    10: 'Octubre',
    11: 'Noviembre',
    12: 'Diciembre'
}

#Se establece una función que es de utilidad para calcular el número de ventas por producto, sin considerar los que son regresados.
#Además, ofrece de retorno una lista de listas con el ID del producto y el total de ventas por producto.
def calcular_ventas_por_producto(refund=False):
    lista_ventas_por_producto = [[i + 1, 0] for i in range(productos_num)]
    for sale in lifestore_sales:
        if refund:
            if sale[4] == 0:
                lista_ventas_por_producto[sale[1] - 1][1] += 1
        else:
            lista_ventas_por_producto[sale[1] - 1][1] += 1
    return lista_ventas_por_producto

#Se establece una función que calcula el número de búsquedas por producto, que ofrece de regreso una lista de listas
#con el ID del producto y el total de búsquedas por producto.
def calcular_busquedas_por_producto():
    lista_busquedas_por_producto = [[i + 1, 0] for i in range(productos_num)]
    for search in lifestore_searches:
        lista_busquedas_por_producto[search[1] - 1][1] += 1
    return lista_busquedas_por_producto

#Se establece una función que calcula el número de ventas por producto y las ordena desde la mejor a la peor
def ordenar_productos_por_ventas():
    lista_ventas_por_producto = calcular_ventas_por_producto()
    sort(lista_ventas_por_producto, lambda x: x[1])
    return lista_ventas_por_producto

#Se establece una función que calcula el número de búsquedas por producto y las ordena desde la mejor a la peor. 
def ordenar_productos_por_busquedass():
    lista_busquedas_por_producto = calcular_busquedas_por_producto()
    sort(lista_busquedas_por_producto, lambda x: x[1])
    return lista_busquedas_por_producto

#Se establece una función que recibe un array con información de cada producto, y retorna una lista que contiene elementos relacionados a la categoría.
def calcular_por_categorias(array):
    for element in array:
        id_producto = element[0]
        categoria_de_producto = lifestore_products[id_producto - 1][3]
        element.append(categoria_de_producto)
    lista_por_categoria = []
    categoria_previa = array[0][2]
    acumulado_por_categoria = 0
    productos_por_categoria = 0
    array.append([0, 0, 'temporal'])
    for product in array:
        categoria = product[2]
        if categoria != categoria_previa:
            lista_por_categoria.append([categoria_previa, acumulado_por_categoria, productos_por_categoria])
            acumulado_por_categoria = 0
            productos_por_categoria = 0

        categoria_previa = categoria
        acumulado_por_categoria += product[1]
        productos_por_categoria += 1
    del array[-1]

    return lista_por_categoria

#Se establece una función que ordena las categorías por número de ventas y retorna una lista de ventas ordenadas por categoría
def ordenar_categorias_por_ventas():
    ventas_por_producto = calcular_ventas_por_producto()
    lista_ventas_por_categoria = calcular_por_categorias(ventas_por_producto)
    sort(lista_ventas_por_categoria, lambda x: x[1])

    return lista_ventas_por_categoria

#Se establece una función que ordena las categorías por número de búsquedas y retorna una lista de búsquedas ordenadas por categoría
def ordenar_categorias_por_busquedas():
    busquedas_por_producto = calcular_busquedas_por_producto()
    lista_busquedas_por_categoria = calcular_por_categorias(busquedas_por_producto)
    sort(lista_busquedas_por_categoria, lambda x: x[1])

    return lista_busquedas_por_categoria

#Se calcula el puntaje promedio por producto obtenido de las reseñas y se ordena de menor a mayor.
def reseñas():
    puntaje_promedio_por_producto = []
    puntaje_acumulado_por_producto = [[i + 1, 0] for i in range(productos_num)]
    lista_ventas_por_producto = calcular_ventas_por_producto()

    for sale in lifestore_sales:
        id_producto = sale[1]
        puntaje_acumulado_por_producto[id_producto - 1][1] += sale[2]

    for puntaje_acumulado in puntaje_acumulado_por_producto:
        id_producto = puntaje_acumulado[0]
        sales = lista_ventas_por_producto[id_producto - 1][1]
        if sales > 0:
            puntaje_promedio = puntaje_acumulado[1] / sales
            puntaje_promedio_por_producto.append([id_producto, puntaje_promedio])

    sort(puntaje_promedio_por_producto, lambda x: x[1])

    return puntaje_promedio_por_producto

#Se establece una variable que considera las ventas por producto, y el precio de cada producto (sin tomar en cuenta los que se regresaron)
#para retornar el ingreso total
def ingresos_totales():
    ingreso = 0
    ventas_por_producto = calcular_ventas_por_producto(refund=True)
    for sales in ventas_por_producto:
        id_producto = sales[0]
        ingreso += lifestore_products[id_producto - 1][2] * sales[1]
    return ingreso

#Se establece una función que crea una lista con los meses y las ventas relacionadas a esos meses, dividiendo la fecha 
#para tomar solo el valor del índice en el que se encuentra el mes, y recopilar únicamente las ventas que no incluyeron la devolución
#del producto
def ingresos_mensuales():
    lista_ventas_mensuales = [[mes, 0] for mes in range(1, 13)]
    ventas_concretadas_total = 0
    for sale in lifestore_sales:
        mes = int(sale[3].split('/')[1])
        if sale[4] == 0:
            lista_ventas_mensuales[mes - 1][1] += 1
            ventas_concretadas_total += 1

    return lista_ventas_mensuales, ventas_concretadas_total

#Se establece una función que imprime los 50 productos más vendidos, los 100 (97, por error de la base de datos) productos más buscados, las categorías con
#menores ventas y menos búsquedas
def opcion1():
    lista_ventas_por_producto = ordenar_productos_por_ventas()
    print('Los 50 productos más vendidos son: ')
    for index in range(1, 51):
        print(
            f'{index}.- {lista_ventas_por_producto[-index][1]} ventas para'
            f' {lifestore_products[lista_ventas_por_producto[-index][0] - 1][1]}')
    print('\n')

    lista_busquedas_por_producto = ordenar_productos_por_busquedass()
    print('Los productos más buscados son: ')
    for index in range(1, 97):
        print(
            f'{index}.- {lista_busquedas_por_producto[-index][1]} busquedas para'
            f' {lifestore_products[lista_busquedas_por_producto[-index][0] - 1][1]}')
    print('\n')

    lista_ventas_por_categoria = ordenar_categorias_por_ventas()
    lista_ventas_por_categoria.reverse()
    print(f'Las ventas por categoría son:')
    for index in range(len(lista_ventas_por_categoria)):
        print(
            f'{index + 1}.- {lista_ventas_por_categoria[index][1]} para {lista_ventas_por_categoria[index][0]} with '
            f'{lista_ventas_por_categoria[index][2]} productos'
        )
    print('\n')

    lista_busquedas_por_categoria = ordenar_categorias_por_busquedas()
    lista_busquedas_por_categoria.reverse()
    print(f'Las busquedas por categoria son:')
    for index in range(len(lista_busquedas_por_categoria)):
        print(
            f'{index + 1}.- {lista_busquedas_por_categoria[index][1]} para {lista_busquedas_por_categoria[index][0]} '
            f'con {lista_busquedas_por_categoria[index][2]} productos'
        )

#Se establece una función que imprime los productos con mejor puntaje de acuerdo a las reseñas, y los productos con menor puntaje
def opcion2():
    puntaje_promedio_por_producto = reseñas()
    print('Los 20 productos con mejores reseñas son: ')
    for index in range(1, 21):
        print(
            f'{index}.- {puntaje_promedio_por_producto[-index][1]:.2f}/5 estrellas para'
            f' {lifestore_products[puntaje_promedio_por_producto[-index][0] - 1][1]}')
    print('\n')
    print('Los 20 productos con peores reseñas son: ')
    for index in range(20):
        print(
            f'{index + 1}.- {puntaje_promedio_por_producto[index][1]:.2f}/5 estrellas para'
            f' {lifestore_products[puntaje_promedio_por_producto[index][0] - 1][1]}')

#Se establece una función que imprime el total de ingresos, los ingresos mensuales, las ventas mensuales y las ventas totales concretadas, sin considerar las devoluciones.
def opcion3():
    ingreso = ingresos_totales()
    lista_ventas_mensuales, ventas_concretadas_total = ingresos_mensuales()
    print(f'El total de ingresos fueron: {ingreso}')
    print(f'El promedio mensual de ingresons fue: {ingreso / 8:.2f}')
    print(f'Las ventas concretadas en el 2020 fueron: {ventas_concretadas_total} \n')
    print(f'Las ventas mensuales fueron:')
    for index, mes in enumerate(lista_ventas_mensuales):
        print(f'{index + 1} .- {mes[1]} ventas concretadas en {diccionario_meses[mes[0]]}')

#Se hace uso del módulo sys, para establecer una función que permita imprimir todo el análisis en un archivo de texto .TXT
def opcion4():
    original_stdout = sys.stdout 

    with open('report4.txt', 'w') as f:
        sys.stdout = f  
        opcion1()
        print('\n')
        opcion2()
        print('\n')
        opcion3()
        sys.stdout = original_stdout  

