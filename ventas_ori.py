import matplotlib.pyplot as plt
#Preparamos los datos
dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
ventas =[120, 85, 150, 200, 170]
#Creamos la gráfica de barras
plt.bar(dias, ventas, color='violet')
#personalizamos la grafica
plt.title('Ventas de la semana')
plt.xlabel('Días de la semana')
plt.ylabel('Cantidad de productos vendidos')
#Mostrar el resultado
plt.show()