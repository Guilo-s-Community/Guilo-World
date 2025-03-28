import math
import numpy as np
from scipy import integrate
from matplotlib import pyplot as plt

plt.style.use('ggplot')

#Constantes
h = 4.136e-15  # Constante de Planck
hm = 6.626e-34  # Constante de Planck para massa
c = 3e8  # Velocidade da luz
me = 9.11e-31  # Massa do elétron
mp = 1.67e-27  # Massa do próton
j = 6.242e18  # Constante de conversão de Joule para eV

#Eletron
def larguraPocoE(A):
    larguraE = 2 / (A**2)
    return larguraE

def numeroQuanticoE(largura, K):
    nE = round((K * largura) / math.pi)
    return nE

def probabilidadeParticulaE(largura, n, X):
    x = x * largura
    probabilidadeE = (2 / largura) * ((math.sin((n * math.pi * X) / largura))**2)
    return probabilidadeE

#Proton
def larguraPocoP(A):
    larguraP = 2 / (A**2)
    return larguraP

def numeroQuanticoP(largura, K):
    nP = round((K * largura) / math.pi)
    return nP

def probabilidadeParticulaP(largura, n, x):
    x = x * largura
    probabilidadep = (2 / largura) * ((math.sin((n * math.pi * x) / largura))**2)
    return probabilidadep


# Função de onda
def funcaoQuanticaInicial(ninicial, largura):
    A =  math.sqrt(2 / largura)
    k1 = (ninicial * math.pi) / largura
    return A, k1

def funcaoQuanticaFinal(nfinal, largura):
    A = math.sqrt(2 / largura)
    k2 = (nfinal * math.pi) / largura
    return A, k2

# Energia

def energiaQuanticaEletron(ninicial, nfinal, L):
    Eij = ((ninicial**2 * hm**2) / (8 * me * L**2))
    Eiv = (Eij * j)
    Efj = (nfinal**2 * hm**2) / (8 * me * L**2)
    Efv = Efj * j
    return Eij, Eiv, Efj, Efv

def energiaQuanticaProton(ninicial, nfinal, L):
    Eij = (((hm**2) / (8 * mp * L**2)) * ninicial**2)
    Eiv = (Eij * j)
    Efj = (((hm**2) / (8 * mp * L**2)) * nfinal**2)
    Efv = (Efj * j)
    return Eij, Eiv, Efj, Efv


# Fóton
def calculoFoton(Eiv, Efv):
    eabsorvido = abs(Efv - Eiv)
    CompOnda = (h * c) / eabsorvido
    f = eabsorvido / h
    return eabsorvido, CompOnda, f


# Velocidade no nivel quantico inicial e final
def velocidadeEletron(Eij, Efj):
    viE = (math.sqrt((2 * Eij) / me))
    vfE = (math.sqrt((2 * Efj) / me))
    return viE, vfE

def velocidadeProton(Eij, Efj):
    viP = (math.sqrt((2 * Eij) / mp))
    vfP = (math.sqrt((2 * Efj) / mp))
    return viP, vfP


# Comprimento de onda de De Broglie

def comprimentoDeBroglieEletron(viE, vfE):
    lambidai = (hm / (me * viE))
    lambidaf = (hm / (me * vfE))
    return lambidai, lambidaf

def comprimentoDeBroglieProton(viP, vfP):
    lambidai = (hm / (mp * viP))
    lambidaf = (hm / (mp * vfP))
    return lambidai, lambidaf



def probabilidadeIntegralNi(A, k1, integralA, integralB):
    integrali =  integrate.quad((lambda x: (A * math.sin(k1 * x)**2)), integralA, integralB)
    porcentagemI = integrali[0] * 100
    return porcentagemI

def probabilidadeIntegralNf(A, k2, integralA, integralB):
    integralf = integrate.quad(lambda x: (A * math.sin(k2 * x)**2), integralA, integralB)
    porcentagemF = integralf[0] * 100
    return porcentagemF

def GraficosOndas(A, k1, k2, ninicial, nfinal, largura):

    def f1(x):
        return A * np.sin(k1 * x)

    def f2(x):
        return A * np.sin(k2 * x)

    x = np.linspace(0, largura, 100)

    try:
        plt.close()
    except:
        pass

    fig, ax = plt.subplots(2,1, figsize=(8, 8))
    fig.tight_layout(pad=5.0)

    ax[0].set(
        title=("Função de Onda da Partícula no nível %d - Inicial" % ninicial),
        xlabel="x (Â)",
        ylabel=("Ψ%d" % ninicial),
    )
    ax[0].axhline(y=0, color="red", linestyle="-", linewidth=0.5)

    yf1 = f1(x)
    ax[0].plot(x, yf1)

    ax[1].set(
        title=("Função de Onda da Partícula no nível %d - Final" % nfinal),
        xlabel="x (Â)",
        ylabel=("Ψ%d" % nfinal),
    )
    ax[1].axhline(y=0, color="red", linestyle="-", linewidth=0.5)

    yf2 = f2(x)
    ax[1].plot(x, yf2)




def GraficosProbabilidade(A, k1, k2, ninicial, nfinal, largura):

    def g1(x):
        return (A * np.sin(k1 * x))**2

    def g2(x):
        return (A * np.sin(k2 * x))**2

    x = np.linspace(0, largura, 100)

    try:
        plt.close()
    except:
        pass

    fig, ax = plt.subplots(2,1, figsize=(8, 8))
    fig.tight_layout(pad=5.0)

    ax[0].set(
        title=("Probabilidade da Partícula no nível %d" % ninicial),
        xlabel="x (Â)",
        ylabel=("|Ψ%d|²" % ninicial),
    )
    ax[0].axhline(y=0, color="red", linestyle="-", linewidth=0.5)

    yg1 = g1(x)
    ax[0].plot(x, yg1)

    ax[1].set(
        title=("Probabilidade da Partícula no nível %d" % nfinal),
        xlabel="x (Â)",
        ylabel=("|Ψ%d|²" % nfinal),
    )
    ax[1].axhline(y=0, color="red", linestyle="-", linewidth=0.5)
    yg2 = g2(x)
    ax[1].plot(x, yg2)
