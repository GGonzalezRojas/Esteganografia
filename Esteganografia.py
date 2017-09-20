#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####Librerias utilizadas#####
from skimage import io
from time import sleep
import random
import numpy as np
import matplotlib.pyplot as plt
import os
import os.path as path
import sys
##############################
######Definicion de funciones#####
#Mostrar imagen recibe una imagen en formato matriz numpy y la muestra
#mediante la libreria matplotlib
def MostrarImagen(matriz_imagen):
	#print(matriz_imagen)
	plt.figure()
	plt.imshow(matriz_imagen)
	plt.show()

#Definicion del menu de la aplicacion
def Menu():
	#Detecta el sistema operativo y realiza limpieza de pantalla
	if "darwin" in sys.platform:
		os.system("clear")
	elif "win" in sys.platform:
		os.system("cls") 
	print ("Selecciona una opcion")
	print ("\t1 - Codificar mensaje")
	print ("\t2 - Decodificar mensaje")
	print ("\t0 - salir")

#Funcion realiza traspaso de imagen formato .bmp a una matriz tipo numpy
def ImagenMatriz(nombre_archivo):
	matriz_imagen = io.imread(nombre_archivo)
	return matriz_imagen

#Funcion hace el traspaso de string hacia binario
def MensajeBinario(mensaje):
	palabraBin = ""
	for car in mensaje:
		cod = ord(car)
		temp = bin(cod)
		temp = temp[2:]
		largo = len(temp)
		palabraBin = palabraBin + "0" * (8 - largo) + temp
	return palabraBin

#Funcion hace el traspaso desde un int hacia binario
def EnteroBinario(pixel):
	pixelBin = ""
	temp = bin(pixel)
	temp = temp[2:]
	largo = len(temp)
	pixelBin = pixelBin + "0" * (8 - largo) + temp
	return pixelBin

#Verifica la exitencia del archivo imagen a procesar
def VerificarArchivo(nombre_archivo):
	if os.path.exists(nombre_archivo):
		return True

#Comprueba el tamaño del mensaje y lo compara con los pixeles
#con esto lograr ver si la cantidad de bits del mensaje alcanzan
#en la totalidad de pixeles de la imagen
def ComprobarTamaño(mensaje_binario, matriz_imagen):
	bits_binario = len(mensaje_binario)
	#guardaremos un bit por pixel por lo cual :
	nfilas, ncolumnas, _ = matriz_imagen.shape
	pixeles_imagen = nfilas * ncolumnas
	#print(pixeles_imagen)
	if bits_binario < pixeles_imagen:
		return True
	else:
		return False

#Donde ocurre la magia, guarda en el ultimo bit de cada
#componente de color del pixel un bit perteneciente al mensaje
#de esta forma no se altera la imagen ya que es un bit no significativo
#en el color del pixel
def Secreto(binario, bit):
	lsb = binario[:7]+bit
	return lsb

#Transforma cada elemento de la matriz en su respectivo binario
def ImagenBinaria(image, m, n):
	print("#Creando Imagen Binaria 		...[+]")
	text_ext=""
	for x in range (0, m):
		for y in range (0, n):
			for h in range (0,3): 
				text_ext += str(EnteroBinario(image[x,y][h]))[-1]
	return text_ext	

#Almacena el secreto obtenido de la imagen (mensaje) en un txt
#para poder verlo
def MostrarSecreto(dato):
	salida=open("mensaje_deco.txt","w")
	salida.write(dato)
	salida.close()

#Funcion encargada de codificar el mensaje y realizar el almacenado
#de cada bit del mensaje en el ultimo bit de cada componente del pixel
#mediante la funcion antes vista Secreto().
def Codificar(mensaje_binario, matriz_imagen):
	#Se crea una firma la cual perimitira encontrar el mensaje luego de ser
	#escondido en la imagen
	firma = "0111010101110011011000010110001101101000"
	info = mensaje_binario
	bits = len(mensaje_binario)
	#print(bits, EnteroBinario(bits))
	info = EnteroBinario(bits)+firma+info
	nfilas,ncolumnas,_ =  matriz_imagen.shape
	print("#Ocultando datos 			...[+]")
	sleep(2)
	for x in range(0,nfilas):
		for y in range(0,ncolumnas):
			for h in range(0,3):
				if len(info) != 0:
					color_pixel = matriz_imagen[x][y][h]
					color_pixel_binario = EnteroBinario(color_pixel)
					copy = list(matriz_imagen[x][y])
					copy[h] = int(Secreto(color_pixel_binario, info[0]), 2)
					matriz_imagen[x][y] = tuple(copy)
					info = info[1:]
					
				else:
					break
	print("#Guardando imagen procesada 			...[+]")
	sleep(2)
	io.imsave("imagedeco.bmp", matriz_imagen)
	print("#Mensaje guardado en imagen 			...[+]")


def Decodificar(matriz_imagen):
	firma = "0111010101110011011000010110001101101000"
	tamx, tamy, _ = matriz_imagen.shape
	img_bin = ImagenBinaria(matriz_imagen, tamx, tamy)
	search = img_bin.find(firma)
	if search != -1:
			
			print("#Firma Encontrada			...[+]")
			bsize = img_bin[:search]
			size = int(bsize,2)
			img_bin = img_bin[search+len(firma):]
			n = size/8
			salida = ""
			letra = ""
			print("#Extrayendo Datos 			...[+]")
			
			for i in range (0, int(n)):
				letra = img_bin[0:8]
				salida += chr(int(letra,2))
				img_bin=img_bin[8:]
			MostrarSecreto(salida)
			print("#Mensaje guardado en txt 			...[+]")

	else:

			print("#Firma NO Encontrada, se extraera todo	...[+]")
			n=len(img_bin)/8
			size=len(img_bin)
			salida = ""
			letra = ""
			print("#Extrayendo Datos 			...[+]")
			
			for i in range (0, int(n)):
				letra = img_bin[0:8]
				salida += chr(int(letra,2))
				img_bin=img_bin[8:]

			MostrarSecreto(salida)
			print("#Mensaje guardado en txt 			...[+]")

##### Bloque principal ######
while True:
	# Mostramos el Menu
	Menu()
 
	# solicitamos una opcion al usuario
	opcionMenu = input("inserta un numero valor >> ")
 
	if opcionMenu=="1":
		print ("")
		input("Has pulsado la opcion 1...\npulsa enter para continuar")
		nombre_imagen = input("Ingrese nombre de imagen a procesar: ")
		comprobacion = VerificarArchivo(nombre_imagen)
		if comprobacion == True:
			matriz_img = ImagenMatriz(nombre_imagen)
			mensaje = input("Ingresar mensaje: ")
			mensaje_binario = MensajeBinario(mensaje)
			afirmativo = ComprobarTamaño(mensaje_binario, matriz_img)
			if afirmativo == True:
				print("Mensaje puede ser guardado en imagen ")
				sleep(2)
				Codificar(mensaje_binario,matriz_img)
				MostrarImagen(ImagenMatriz("imagedeco.bmp"))
			else:
				print("Mensaje no puede ser guardado en imagen ya que excede el tamano ")
			continuar = input("Presiones Enter para continuar...")
		else:
			print("No existe archivo ingresado")
			continuar = input("Presiones Enter para continuar...")

	elif opcionMenu=="2":
		print ("")
		input("Has pulsado la opcion 2...\npulsa enter para continuar")
		nombre_imagen_deco = input("Ingrese nombre de imagen a decodificar: ")
		comprobacion = VerificarArchivo(nombre_imagen_deco)
		if comprobacion == True:
			matriz_img_deco = ImagenMatriz(nombre_imagen_deco)
			print("#Decodificando 			...[+]")
			sleep(2)
			Decodificar(matriz_img_deco)
			continuar = input("Presiones Enter para continuar...")
		else:
			print("No existe archivo ingresado")
			continuar = input("Presiones Enter para continuar...")

	elif opcionMenu=="0":
		break
	else:
		print ("")
		input("No has pulsado ninguna opcion correcta...\npulsa enter para continuar")



