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

num_bits = 11

import random
secret_a = [random.randint(0, 1) for x in range(num_bits)]

def f(x):
  bstr = ("{" + ":0{}b".format(num_bits) + "}").format(x)
  lx = [int(c) for c in bstr]

  sum = 0
  for i in range(num_bits):
    sum += lx[i] * secret_a[i]
  return sum % 2

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

print("\nSecret A was:")
print(secret_a)


del state
