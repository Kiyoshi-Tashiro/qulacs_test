# -*- coding: utf-8 -*-

from qulacs import QuantumState
from qulacs.gate import X, Z, H, DenseMatrix
import numpy as np
import math


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

num_bits = 4

import random
secret_a = random.randint(0, 2 ** num_bits - 1)

def f(x):
  if x == secret_a:
    return 1
  return 0

cu_mat = np.zeros((2 ** (num_bits + 1), 2 ** (num_bits + 1)), np.int8)
for x in range(2 ** num_bits):
  crow = x * 2 + f(x)
  cu_mat[x*2][crow] = 1
  cu_mat[x*2+1][crow // 2 * 4 + 1 - crow] = 1

m = 2 ** num_bits
dist_mat = np.full((m, m), .5 / m)
for x in range(m):
  dist_mat[x][x] = -1 + .5 / m

if num_bits < 6:
  print("CU Gate Matrix:")
  for i in range(2 ** (num_bits + 1)):
    print(''.join([str(b) for b in cu_mat[i]]))
  print("Dist Gate Matrix:")
  for i in range(2 ** num_bits):
    print(''.join(["{:>6.2}".format(b) for b in dist_mat[i]]))

state = QuantumState(num_bits + 1)
state.set_computational_basis(0)
x_gate = X(0)
x_gate.update_quantum_state(state)

print("\nInitial State:")
show_quantum_state(state)

for i in range(0, num_bits + 1):
  h_gate = H(i)
  h_gate.update_quantum_state(state)

print("\nAfter H Gate:")
show_quantum_state(state)

ite = int(math.pow(2., num_bits * .5))

cu_gate = DenseMatrix(tuple(range(num_bits + 1)), cu_mat)
dist_gate = DenseMatrix(tuple(range(1, num_bits + 1)), dist_mat)

for t in range(ite):
  cu_gate.update_quantum_state(state)

  print("\nAfter CU Gate:")
  show_quantum_state(state)

  dist_gate.update_quantum_state(state)

  print("\nAfter Dist Gate:")
  show_quantum_state(state)

form = "{" + ":0{}b".format(num_bits) + "}"

print("\nProbabilities:")
for x in range(2 ** num_bits):
  testval = [int(b) for b in form.format(x)]
  testval.append(2)
  val = state.get_marginal_probability(testval[::-1])
  print((form + " {}").format(x, val))

print("\nSecret A was:")
print(("{} (" + form + ")").format(secret_a, secret_a))


del state
