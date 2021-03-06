# ------------------------------------------------------------------------------
#  @file     +temperamental.py+
#  @brief    +Optimización+
#  @author   +Grupo 4+
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# LIBRARIES
# ------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math as mt

# ------------------------------------------------------------------------------
# FUNCTION DEF
# ------------------------------------------------------------------------------
data = np.loadtxt("temp.txt") 
t=data[:,0]; y=data[:,1]

#Optimización basada el método de gradientes conjugados usando interpolación cuadrática
def minimi(f, Df, x0, tol, maxiter):
    x = x0
    g = -Df(x) # Gradiente

    # Evaluo primero si el gradiente es menor a la tolerancia
    if(np.linalg.norm(g)==0):
        print("X0 es un mínimo")
        return x
    
    # Determinamos un alfa para cada paso de interación usando interpolación cuadrática
    for i in range(maxiter):
        alfa_min = 1
        #H = alfa_min * g 

        a = 0
        fa= f(x+a*g)
        b = 1
        fb= f(x+b*g)
        c = 1/2
        fc= f(x+c*g)
	    #(a,fa) - (c,fc) - (b,fb)	
        k=1
        while 1 :
            if fa > fc:
                #sigue "bajando"
                if fc > fb:
                    c, fc  = b, fb
                    b *= 2
                    fb = f(x+b*g)
                else:
                    break
            else: 
                #está aumentando
                b, fb  = c, fc
                c  /= 2
                fc = f(x+c*g)
            
            #si el intervalo es demasiado chico o demasiado grande, comencemos nuevamente
            if (b < 1e-6) or (b > 1e6) :
                k = k + 1
                if k == 100 :
                    break
                b = np.random.rand(1)
                c /= 2
        
        # Si después de muchas iteraciones, no llegamos a nada, x_n = x
        if k == 100 :
            x_n = x
        else:
            alfa_min = c*((4*fc-fb-3*fa)/(4*fc-2*fb-2*fa))
            x_n = x + alfa_min*g

        if(np.linalg.norm(x_n-x)<tol):
            break
        x = x_n
    return x

f_aux= lambda x: y - (x[0]+x[1]*np.cos(2*np.pi*t/x[3])+x[2]*np.cos(2*np.pi*t/x[4]))
f = lambda x: np.sum(np.square(f_aux(x)))/len(f_aux(x))

def grad(coef):
    # coef = [a, b, c, T1, T2]
    df=np.zeros(len(coef))
    difflocal = f_aux(coef)

    df[0]=-2*np.sum(difflocal)  #d/da
    df[1]=-2*np.sum(difflocal*np.cos(2*np.pi*t/coef[3]))   #d/db 
    df[2]=-2*np.sum(difflocal*np.cos(2*np.pi*t/coef[4]))   #d/dc
    df[3]=-2*np.sum(difflocal*coef[1]*np.pi*2*t*np.sin(2*np.pi*t/coef[3])/(coef[3]**2)) #d/dT1
    df[4]=-2*np.sum(difflocal*coef[2]*np.pi*2*t*np.sin(2*np.pi*t/coef[4])/(coef[4]**2)) #d/dT2
    return df

def temperatura():
    xo=np.array([36.00,-0.6,1.0,24.00,24.00])
    tol=1e-15; max_it=1000
    x = minimi(f, grad, xo, tol, max_it)
    error = f_aux(x) # Error local
    return x, error    

# ------------------------------------------------------------------------------
# TEST
# ------------------------------------------------------------------------------
def temp_test():
    #Evaluamos la función temperatura
    x, error=temperatura()
    print("Coef obtenidos ([a,b,c,T1,T2]): \n", x)
    print("ECM: ", np.sum(np.power(error,2))/len(error))
    print("Error Máximo", np.max(np.abs(error)), "ºC")
    print("Error Relativo medio: ", (np.sum(abs(error/y))/len(error))*100, "%")

    temp = lambda t: (x[0]+x[1]*np.cos(2*np.pi*t/x[3])+x[2]*np.cos(2*np.pi*t/x[4]))

    plt.plot(t, y, 'b', label='Datos')
    plt.plot(t, temp(t), 'r', label='Modelo')
    plt.xlim(0, 250)
    plt.legend()
    plt.show()
    return

esfera = lambda x: x[0]**2+x[1]**2+x[2]**2
gradesfera = lambda x: np.array([2*x[0], 2*x[1], 2*x[2]])

def test():
    tol=1e-15; max_it=1000
    
    print("Funciones de prueba para minimi:\n")
    print("Función esférica: \n")
    x0esf=np.array([-47.5,20,-12.6])
    x1=minimi(esfera, gradesfera, x0esf, tol, max_it)
    print("El mínimo real es: [0,0,0] mientras que el mínimo calculado por minimi con x0=", x0esf, "es: ", x1)
    x0esf=np.array([-47,5,0])
    x1=minimi(esfera, gradesfera, x0esf, tol, max_it)
    print("El mínimo real es: [0,0,0] mientras que el mínimo calculado por minimi con x0=", x0esf, "es: ", x1)
    x0esf=np.array([-1,-5,-60])
    x1=minimi(esfera, gradesfera, x0esf, tol, max_it)
    print("El mínimo real es: [0,0,0] mientras que el mínimo calculado por minimi con x0=", x0esf, "es: ", x1)
    x0esf=np.array([1,1,1])
    x1=minimi(esfera, gradesfera, x0esf, tol, max_it)
    print("El mínimo real es: [0,0,0] mientras que el mínimo calculado por minimi con x0=", x0esf, "es: ", x1)

    print("\n\n")
    
    print("Evaluación de la funcion de temperatura: \n")
    temp_test()
    return
