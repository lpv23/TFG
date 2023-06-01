import matplotlib.pyplot as plt
import numpy as np
import sympy


def graficas_mmp(caso_medio, caso_mejor, caso_peor, limite, tipo):
    xlin = np.linspace(1, limite, 500)
    xsim = sympy.Symbol('x')
    plt.plot(xlin, caso_mejor(xlin), label='Caso mejor' + '\n' + str(caso_mejor(xsim)))
    plt.plot(xlin, caso_medio(xlin), label='Caso medio' + '\n' + str(caso_medio(xsim)))
    plt.plot(xlin, caso_peor(xlin), label='Caso peor' + '\n' + str(caso_peor(xsim)))
    plt.title('Complejidad asintótica')
    plt.xlabel('Tamaño')
    plt.ylabel(tipo)
    plt.legend()
    plt.show()


def graficas_mm(caso_medio, caso_mejor, limite, tipo):
    xlin = np.linspace(1, limite, 500)
    xsim = sympy.Symbol('x')
    plt.plot(xlin, caso_mejor(xlin), label='Caso mejor' + '\n' + str(caso_mejor(xsim)))
    plt.plot(xlin, caso_medio(xlin), label='Caso medio' + '\n' + str(caso_medio(xsim)))
    plt.title('Complejidad asintótica')
    plt.xlabel('Tamaño')
    plt.ylabel(tipo)
    plt.legend()
    plt.show()


def graficas_mp(caso_medio, caso_peor, limite, tipo):
    xlin = np.linspace(1, limite, 1000)
    xsim = sympy.Symbol('x')
    plt.plot(xlin, caso_medio(xlin), label='Caso medio' + '\n' + str(caso_medio(xsim)))
    plt.plot(xlin, caso_peor(xlin), label='Caso peor' + '\n' + str(caso_peor(xsim)))
    plt.title('Complejidad asintótica')
    plt.xlabel('Tamaño')
    plt.ylabel(tipo)
    plt.legend()
    plt.show()


# Ordenación burbuja
# Tiempo
def ord_burb_t(x):
    return 5.56e-8 * x ** 2 - 0.00017


def ord_burb_m_t(x):
    return 4.16e-8 * x ** 2 - 0.00077


def ord_burb_p_t(x):
    return 1.02e-7 * x ** 2 - 0.00065


# graficas_mmp(ord_burb_t, ord_burb_m_t, ord_burb_p_t, 3000, 'Tiempo')


# OE
def ord_burb_oe(x):
    return 1.75 * x ** 2 - 612.84


def ord_burb_m_oe(x):
    return 1.00045 * x ** 2 - 366.63


def ord_burb_p_oe(x):
    return 2.5 * x ** 2 - 237.57


# graficas_mmp(ord_burb_oe, ord_burb_m_oe, ord_burb_p_oe, 3000, 'Operaciones')


# Ordenación inserción
# Tiempo
def ord_ins_t(x):
    return 2.48e-8 * x ** 2 - 0.00044


def ord_ins_m_t(x):
    return 1.1e-8 * x ** 1.21 + 0.00051


def ord_ins_p_t(x):
    return 6.84e-8 * x ** 2 - 0.00072


# graficas_mmp(ord_ins_t, ord_ins_m_t, ord_ins_p_t, 3000, 'Tiempo')


# OE
def ord_ins_oe(x):
    return 0.75 * x ** 2 + 1862.89


def ord_ins_m_oe(x):
    return 5 * x - 3


def ord_ins_p_oe(x):
    return 1.5 * x ** 2 + 843.61


# graficas_mmp(ord_ins_oe, ord_ins_m_oe, ord_ins_p_oe, 3000, 'Operaciones')


# Ordenación selección
# Tiempo
def ord_sel_t(x):
    return 1.82e-8 * x ** 2 - 1.43e-5


def ord_sel_m_t(x):
    return 1.35e-8 * x ** 2 + 0.00048


# graficas_mm(ord_sel_t, ord_sel_m_t, 3000, 'Tiempo')


# OE
def ord_sel_oe(x):
    return 1.01 * x ** 2 + 5049.91


def ord_sel_m_oe(x):
    return 1 * x ** 2 + 1829.15


# graficas_mm(ord_sel_oe, ord_sel_m_oe, 3000, 'Operaciones')

# Ordenación sort
def ord_sort(x):
    return 1.17e-8 * x ** 1.23 + 0.00047


# xlin_ord = np.linspace(1, 3000, 500)
# xsim_ord = sympy.Symbol('x')
# plt.plot(xlin_ord, ord_burb_t(xlin_ord), label='Burbuja' + '\n' + str(ord_burb_t(xsim_ord)))
# plt.plot(xlin_ord, ord_ins_t(xlin_ord), label='Inserción' + '\n' + str(ord_ins_t(xsim_ord)))
# plt.plot(xlin_ord, ord_sel_t(xlin_ord), label='Selección' + '\n' + str(ord_sel_t(xsim_ord)))
# plt.plot(xlin_ord, ord_sort(xlin_ord), label='Sort' + '\n' + str(ord_sort(xsim_ord)))
# plt.title('Complejidad asintótica algoritmos de ordenación')
# plt.xlabel('Tamaño')
# plt.ylabel('Tiempo')
# plt.legend()
# plt.show()


# Búsqueda binaria
def bus_bin_t(x):
    return 1.95e-6 * x ** 0.17 - 2.65e-6


def bus_bin_p_t(x):
    return 2.14e-6 * x ** 0.17 - 2.86e-6


# graficas_mp(bus_bin_t, bus_bin_p_t, 8e6, 'Tiempo')


def bus_bin_oe(x):
    if type(x) == sympy.Symbol:
        return 4.93 * sympy.log(x, 2) + 2.8
    return 4.93 * np.log2(x) + 2.8


def bus_bin_p_oe(x):
    if type(x) == sympy.Symbol:
        return 4.96 * sympy.log(x, 2) + 7.19
    return 4.96 * np.log2(x) + 7.19


# graficas_mp(bus_bin_oe, bus_bin_p_oe, 8e6, 'Operaciones')


# Búsqueda lineal ineficiente
def bus_1a1_inef_t(x):
    return 6.05e-9 * x ** 1.16 - 0.00072


# Búsqueda lineal eficiente
def bus_1a1_efi_t(x):
    return 4.96e-8 * x - 0.00098


def bus_1a1_efi_p_t(x):
    return 5.57e-9 * x ** 1.17 - 0.00068


# graficas_mp(bus_1a1_efi_t, bus_1a1_efi_p_t, 4e6, 'Tiempo')


def bus_1a1_efi_oe(x):
    return 1.59 * x + 2452.15


def bus_1a1_efi_p_oe(x):
    return 2 * x + 2


# graficas_mp(bus_1a1_efi_oe, bus_1a1_efi_p_oe, 4e6, 'Operaciones')


# Búsqueda in
def bus_in(x):
    return 9.71e-9 * x ** 1.09 - 0.00082


xlin_bus = np.linspace(1, 5e6, 1000)
xsim_bus = sympy.Symbol('x')
plt.plot(xlin_bus, bus_bin_t(xlin_bus), label='Binaria' + '\n' + str(bus_bin_t(xsim_bus)))
plt.plot(xlin_bus, bus_1a1_inef_t(xlin_bus), label='Lineal sin parada' + '\n' + str(bus_1a1_inef_t(xsim_bus)))
plt.plot(xlin_bus, bus_1a1_efi_t(xlin_bus), label='Lineal con parada' + '\n' + str(bus_1a1_efi_t(xsim_bus)))
plt.plot(xlin_bus, bus_in(xlin_bus), label='In' + '\n' + str(bus_in(xsim_bus)))
plt.title('Complejidad asintótica algoritmos de búsqueda')
plt.xlabel('Tamaño')
plt.ylabel('Tiempo')
plt.legend()
plt.show()
