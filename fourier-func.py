# import numpy as np

# from numpy import cos, cosh, arccos, sin, sinh, arcsin, tan, tanh, arctan, log, log2, log10, sqrt, pi, exp

# from matplotlib import pyplot as plt
# from scipy import integrate
# from time import sleep

# T = 3
# T1 = 0
# T2 = 2

# print (np.sinc(0))
# # x_func = lambda t: 1

# # x_func = lambda t: -t if t<0 else t

# # x_func = lambda t: np.piecewise (t, [t<-1, t>=-1], [lambda t: 2*t+4, lambda t: -2*t,])

# # x_func = lambda t: np.sin (1/t)

# # x_func = lambda t: t

# x_func = lambda t: np.piecewise (t, [t < 1, np.logical_and (1<=t, t <2), 2 <= t], [lambda t: t, lambda t: 1, lambda t: -t + 3])

# input_function = input ().split ('\n')[0]

# x_func = lambda t: eval (input_function)


# # temp_time = np.linspace (-2, 2, 200)
# # plt.plot (temp_time, x_func (temp_time))
# # plt.show ()
# # plt.grid ()


# exp_func = lambda t, k: np.exp(1j * 2*np.pi*k * t / T)

# ak0 = lambda input_func, T1, T2: 1/T * integrate.fixed_quad (lambda t: input_func(t), T1, T2)[0]
# ak = lambda k, input_func, T1, T2: (1/T) * integrate.fixed_quad (lambda t: input_func(t) * exp_func(-t, k), T1, T2, n=1000)[0]

# xt = lambda t, k: ak0(x_func, T1, T2) +  np.real (sum ([ak(k, x_func, T1, T2) * exp_func(t, k) for k in range (-k, k) if k != 0]))

# time = np.linspace (-5, 5, 200)

# # plt.plot (time, xt (time, harmony))
# # plt.grid ()
# # plt.show ()


# # harmony = 1
# # plt.ion()

# # fig = plt.figure()
# # ax = fig.add_subplot(111)
# # line1, = ax.plot(time, xt (time, harmony), 'r-') # Returns a tuple of line objects, thus the comma
# # plt.ylim ([-3, 3])

# # for k in range (1, 200):
# #     sleep (0.1)
# #     fig.canvas.flush_events()
# #     line1.set_ydata(xt (time, k))
# #     fig.canvas.draw()

# import sys
# harmony = 500

# def on_press(event):
#     print('press', event.key)
#     sys.stdout.flush()
#     global harmony
#     if event.key == 'up':
#         fig.canvas.flush_events ()
#         harmony += 1
#         # ax1.set_ylim ([-harmony, harmony])
#         line1.set_ydata(xt (time, harmony))
#         fig.canvas.draw()
#         sleep (0.01)

#     elif event.key == 'down' and harmony != 1:
#         fig.canvas.flush_events ()
#         if harmony != 1: harmony -= 1
#         line1.set_ydata(xt (time, harmony))
#         fig.canvas.draw()
#         sleep (0.01)


# # Fixing random state for reproducibility
# fig = plt.figure ()
# # plt.subplot (222)
# # plt.subplot (211)
# ax1 = fig.add_subplot (211)
# ax2 = fig.add_subplot (212)
# line1, = ax1.plot(time, xt (time, harmony), 'r-')
# line2, = ax2.plot(time, x_func (time), 'b-')
# # ax1.set_ylim ([-5, 5])
# ax1.grid ()
# ax2.grid ()

# fig.canvas.mpl_connect('key_press_event', on_press)
# plt.show ()

# # print (ak0(x_func, T1, T2), sep='\n\n')
# # print (xt (x_func(0.6)))


# # # for k in range (1, 10): print (f"{k} is {ak (k, x_func):.4f}")

# # # ak = lambda k, x, T1, T2: (1/T) *integrate.quad (lambda t: x (t) * np.exp (-1j * 2*np.pi*k * t / T), T1, T2)[0]
# # ak = lambda k: -2 * ((-1)^k - 1) / (2j * np.pi * k)

# # # fourier_coefficents = lambda k: ak (k, lambda t: 2*t + 4, -2, -1) + ak (k, lambda t: -2*t, -1, 1) + ak (k, lambda t: 2*t - 4, 1, 2)

# # base_func = lambda t, k: np.exp (1j * 2*np.pi*k * t / T)

# # # plt.plot ([k for k in range (-100, 100)], [ak (k) for k in range (-100, 100)])
# # # plt.show ()


# # xt = lambda t: np.real (sum ([base_func (k, t) * ak (k) for k in range (-100, 100) if k != 0]))

# # # for t in range (-2, 2):
# # #     print (xt (t))

# # # print (ak (0))
# # # xt = lambda k: ak (0)[k]* (base_func (1, k) + base_func (1, k))

# # # time = np.linspace (-5, 5, 200)
# # # plt.plot (time, xt (time))
# # # plt.grid ()
# # # plt.show ()
# # # print (xt (time))

# # # for k in range (5):
# # #     # print ((ak (k)[0]))
# # #     sm += ak (k)[0]

# # # print (sm)



# # # print (result)

from re import S
from typing import Any


bonds = ["t<0", "t>0"]
funcs = ["2*t+4", "-2*t","t + 5"]
# [eval(bond) for bond in bonds]
new = list()
# new.append(lambda t: eval(funcs[0]))
# new.append(lambda t: eval(funcs[1]))
n = 0
a = 0
b = 1
s = 0

def po(var):
    global s
    s = var

for i in range(len(funcs)):
    # print(func)
    code = compile("lambda t: "+ funcs[i], "<string>", "eval")
    arg = eval(code)
    new.append(arg)
    print("In loop: ", new[i](25))

    if a == i:
        a = arg
        po(a)
        print(a(25))
    elif b == i:
        b = arg
        print(b(25))

print("a, b, s: ", a(25), b(25), s(25))
print(new[0](25) == new[1](25))
print(new[0](25))
print(new[1](25))
actualFunc = [lambda t: 2*t+4, lambda t: -2*t]

import numpy as np

# for i in range(len(funcs)):
print("after for loop: ", new[0](25), new[1](25))
print("Actual values: ", actualFunc[0](25), actualFunc[1](25))

def output(t):
    return np.piecewise(t, [eval(bond, {}, {"t": t}) for bond in bonds], new)

global t

# n = [eval(bond, {}, {"t": t}) for bond in bonds]

# print(n)

n = lambda t: t>0 and t<1
print(n(1))

# x = lambda t: np.piecewise(t, [eval(bond, {}) for bond in bonds], new)
x = output

print(x(-5))

bonds = ["t<0", "t>0"]
funcs = ["2*t+4", "-2*t"]

# print("Constructed list: ", newlist[0](25), newlist[1](25))

# print(lambda t: np.piecewise (t, [t<0, t>0], actualFunc))