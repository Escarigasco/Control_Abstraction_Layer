import numpy as np
import time
import matplotlib.pyplot as plt
import pandas as pd
import csv
_BEGIN_WITH = 0
_FIRST_OF_CLASS = 1
_SECOND_BEST = 2

opening = np.linspace(0, 1, num=100)

# R = 50
Kvs = 1.6
linear_car = lambda  opening : opening
eq_car = lambda  opening : 50 ** (opening - 1)
Kl = 2
DPt = 1
flow_for_distributed_losses = {}

q = lambda v_opening, valve_car, v_Kv, v_Kl: v_Kv * valve_car(v_opening) * (DPt ** 0.5) / (1 + v_Kl * (v_Kv * valve_car(v_opening)) ** 2) ** 0.5
dq_eq = lambda v_opening, valve_car, v_Kv, v_Kl: np.log(50) * v_Kv * valve_car(v_opening) * (DPt ** 0.5) / (1 + v_Kl * (v_Kv * valve_car(v_opening)) ** 2) ** 1.5
dq_lin = lambda v_opening, valve_car, v_Kv, v_Kl: v_Kv * (DPt ** 0.5) / (1 + v_Kl * (v_Kv * valve_car(v_opening)) ** 2) ** 1.5
pump = lambda  n, DPt : (n * 2.35 * 10**(-5)) - (DPt **2) * (6.96 * 10**(-5))
#flow_linear = q(opening, linear_car, Kvs)
flow_eq = q(opening, eq_car, Kvs,1)

flow_for_distributed_losses_linear = {"Kl = 0": [q(opening, linear_car, Kvs, 0), 'gray', 'solid'],
                                      "Kl = 1": [q(opening, linear_car, Kvs, 1), 'r', 'solid'],
                                      "Kl = 2": [q(opening, linear_car, Kvs, 2), 'c', 'solid'],
                                      "Kl = 3": [q(opening, linear_car, Kvs, 3), 'g', 'solid'],
                                      "Kl = 4": [q(opening, linear_car, Kvs, 4), 'm', 'solid'],
                                      "Kl = 5": [q(opening, linear_car, Kvs, 5), 'y', 'solid'],
                                      "Kl = 6": [q(opening, linear_car, Kvs, 6), 'steelblue', 'solid'],
                                      "Ideal": [q(opening, linear_car, Kvs, 0), 'k', 'dotted']
                                      }

flow_for_distributed_losses_equalp = {"Kl = 0": [q(opening, eq_car, Kvs, 0), 'gray', 'solid'],
                                      "Kl = 1": [q(opening, eq_car, Kvs, 1), 'r', 'solid'],
                                      "Kl = 2": [q(opening, eq_car, Kvs, 2), 'c', 'solid'],
                                      "Kl = 3": [q(opening, eq_car, Kvs, 3), 'g', 'solid'],
                                      "Kl = 4": [q(opening, eq_car, Kvs, 4), 'm', 'solid'],
                                      "Kl = 5": [q(opening, eq_car, Kvs, 5), 'y', 'solid'],
                                      "Kl = 6": [q(opening, eq_car, Kvs, 6), 'steelblue', 'solid'],
                                      "Ideal": [q(opening, linear_car, Kvs, 0), 'k', 'dotted']
                                      }

plt.figure(1)
linear = plt.subplot(111)
#linear.set_title("Linear Percentage")
#linear.plot(opening, linear_car(opening), 'k')
#linear.plot(opening, flow_linear / max(flow_linear), 'b')
for Kl in flow_for_distributed_losses_linear.keys():
    linear.plot(opening, flow_for_distributed_losses_linear[Kl][_BEGIN_WITH] / max(flow_for_distributed_losses_linear[Kl][_BEGIN_WITH]),
                flow_for_distributed_losses_linear[Kl][_FIRST_OF_CLASS], label=Kl, ls=flow_for_distributed_losses_linear[Kl][_SECOND_BEST], lw=0.8)
plt.legend()
plt.grid()
plt.xlabel('Fraction of Valve Opening')
plt.ylabel('Fraction of Max Flow Rate')
plt.tight_layout()
plt.savefig('linear.pdf', dpi=1000)

plt.figure(2)
equal = plt.subplot(111)
#equal.set_title("Equal Percentage")
for Kl in flow_for_distributed_losses_equalp.keys():
    equal.plot(opening, flow_for_distributed_losses_equalp[Kl][_BEGIN_WITH] / max(flow_for_distributed_losses_equalp[Kl][_BEGIN_WITH]),
               flow_for_distributed_losses_equalp[Kl][_FIRST_OF_CLASS], label=Kl, ls=flow_for_distributed_losses_linear[Kl][_SECOND_BEST], lw=0.8)
#plt.legend(bbox_to_anchor=(1.02, 1.5), loc=2, borderaxespad=0.)
plt.legend()
plt.grid()
plt.xlabel('Fraction of Valve Opening')
plt.ylabel('Fraction of Max Flow Rate')
plt.tight_layout()
plt.savefig('equal.pdf', dpi=1000)

plt.figure(3)
valve_char = plt.subplot(111)
#valve_char.set_title("Valves Inherent Characteristics")
valve_char.plot(opening, flow_for_distributed_losses_linear["Kl = 0"][_BEGIN_WITH] / max(flow_for_distributed_losses_linear["Kl = 0"][_BEGIN_WITH]), "r", label="Linear Valve", ls='solid', lw=0.8)
valve_char.plot(opening, flow_for_distributed_losses_equalp["Kl = 0"][_BEGIN_WITH] / max(flow_for_distributed_losses_equalp["Kl = 0"][_BEGIN_WITH]), "steelblue", label="Equal Percentage Valve", ls='solid', lw=0.8)
#plt.legend(bbox_to_anchor=(1.02, 1.5), loc=2, borderaxespad=0.)
plt.legend()
plt.grid()
plt.xlabel('Fraction of Valve Opening')
plt.ylabel('Fraction of Flow Rate')
plt.tight_layout()
plt.savefig('inherent.pdf', dpi=1000)

gain_eq = dq_eq(opening, eq_car, Kvs, 3)
plt.figure(4)
valve_char = plt.subplot(111)
#valve_char.set_title("Valves Inherent Characteristics")
valve_char.plot(opening, flow_for_distributed_losses_equalp["Kl = 3"][_BEGIN_WITH] / max(flow_for_distributed_losses_equalp["Kl = 3"][_BEGIN_WITH]), "r", label="Equal Percentage Valve", ls='solid', lw=0.8)
valve_char.plot(opening, gain_eq / max(gain_eq), "steelblue", label="Equal Percentage Valve Gain", ls='solid', lw=0.8)
#plt.legend(bbox_to_anchor=(1.02, 1.5), loc=2, borderaxespad=0.)
plt.legend()
plt.grid()
plt.xlabel('Fraction of Valve Opening')
plt.ylabel('Fraction of Flow Rate')
plt.tight_layout()
plt.savefig('Gain_equal.pdf', dpi=1000)

linear_eq = dq_lin(opening, linear_car, Kvs, 3)
plt.figure(5)
valve_char = plt.subplot(111)
#valve_char.set_title("Valves Inherent Characteristics")
valve_char.plot(opening, flow_for_distributed_losses_linear["Kl = 3"][_BEGIN_WITH] / max(flow_for_distributed_losses_linear["Kl = 3"][_BEGIN_WITH]), "r", label="Linear Percentage Valve", ls='solid', lw=0.8)
valve_char.plot(opening, linear_eq / max(linear_eq), "steelblue", label="Linear Percentage Valve Gain", ls='solid', lw=0.8)
#plt.legend(bbox_to_anchor=(1.02, 1.5), loc=2, borderaxespad=0.)
plt.legend()
plt.grid()
plt.xlabel('Fraction of Valve Opening')
plt.ylabel('Fraction of Flow Rate')
plt.tight_layout()
plt.savefig('Gain_linear.pdf', dpi=1000)


n = np.linspace(1600, 2600, num=10)
#n = 50
DPt = np.linspace(0, 6.5, num=10)
plt.figure(6)
pump_chart = plt.subplot(111)
#valve_char.set_title("Valves Inherent Characteristics")
for rpm in n:
    pump_chart.plot(pump(rpm, DPt), DPt, "r", label="Pump Performance curves", ls='solid', lw=0.8)


#plt.legend(bbox_to_anchor=(1.02, 1.5), loc=2, borderaxespad=0.)
plt.grid()
plt.xlabel('Q')
plt.ylabel('H')
plt.tight_layout()
plt.savefig('Pump_curves.pdf', dpi=1000)


#plt.ion()
plt.show()
