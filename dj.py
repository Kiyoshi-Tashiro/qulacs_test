# -*- coding: utf-8 -*-

from qulacs import QuantumState
from qulacs.gate import X, Z, H, DenseMatrix
import numpy as np


def show_quantum_state(state, eps = 1e-10, round_digit=3):
  vector = state.get_vector()
  state_str = ""
  qubit_count = int( np.log2(len(vector)+eps))
  binary_format = "{" + ":0{}b".format(qubit_count) + "}"
  for ind in range(len(vector)):
    if abs(vector[ind]) > 1e-10:
      if len(state_str) > 0:
        state_str += " + "
      state_str += ("{} |" + binary_format + ">").format(round(vector[ind],round_digit ),ind)
  print(state_str)

num_bits = 12

import random

if random.randint(0, 1):
  y = random.randint(0, 1)
  def f(x):
    return y
  fx_type = 'constant'
else:
  y_dict = {}
  for i in range(2 ** num_bits):
    y_dict[i] = 0
  for i in range(2 ** (num_bits - 1)):
    while True:
      p = random.randint(0, 2 ** num_bits - 1)
      if y_dict[p] == 0:
        y_dict[p] = 1
        break
  def f(x):
    return y_dict[x]
  fx_type = 'balanced'
    

cu_mat = np.zeros((2 ** (num_bits + 1), 2 ** (num_bits + 1)), np.int8)
for x in range(2 ** num_bits):
  crow = x * 2 + f(x)
  cu_mat[x*2][crow] = 1
  cu_mat[x*2+1][crow // 2 * 4 + 1 - crow] = 1

if num_bits < 6:
  print("CU Gate Matrix:")
  for i in range(2 ** (num_bits + 1)):
    print(''.join([str(b) for b in cu_mat[i]]))

state = QuantumState(num_bits + 1)
state.set_computational_basis(0)

print("\nInitial State:")
show_quantum_state(state)

for i in range(1, num_bits + 1):
  h_gate = H(i)
  h_gate.update_quantum_state(state)

print("\nAfter H Gate:")
show_quantum_state(state)

cu_gate = DenseMatrix(tuple(range(num_bits + 1)), cu_mat)
cu_gate.update_quantum_state(state)

print("\nAfter CU Gate:")
show_quantum_state(state)

z_gate = Z(0)
z_gate.update_quantum_state(state)

print("\nAfter Z Gate:")
show_quantum_state(state)

cu_gate = DenseMatrix(tuple(range(num_bits + 1)), cu_mat)
cu_gate.update_quantum_state(state)

print("\nAfter CU Gate:")
show_quantum_state(state)

for i in range(1, num_bits + 1):
  h_gate = H(i)
  h_gate.update_quantum_state(state)

print("\nAfter H Gate:")
show_quantum_state(state)

print("\ntype of f(x) was:")
print(fx_type)


del state
