import numpy as np
def simplex(tab):
    while np.min(tab[-1, :-1]) < -1e-9:
        pivot_col = np.argmin(tab[-1, :-1])
        ratios = []
        for qq in range(len(tab) - 1):
            if tab[qq, pivot_col] > 1e-9:
                ratios.append(tab[qq, -1] / tab[qq, pivot_col])
            else:
                ratios.append(np.inf)
        if np.all(np.array(ratios) == np.inf):
            return "Unbounded"
        pivot_row = np.argmin(ratios)
        tab[pivot_row, :] /= tab[pivot_row, pivot_col]
        for r in range(len(tab)):
            if r != pivot_row:
                tab[r, :] -= tab[r, pivot_col] * tab[pivot_row, :]
    return tab

with open('input.txt', 'r') as f:
    lines = f.readlines()
c = np.array([float(x) for x in lines[0].split()])
mode = lines[1].strip()
constraints = []
for line in lines[2:]:
    parts = line.split()
    k = [float(x) for x in parts[:-2]]
    op = parts[-2]
    rhs = float(parts[-1])
    constraints.append((k, op, rhs))
M = 1e6
n_vars = len(c)
n_cons = len(constraints)
A = []
obj = list(-c if mode == 'max' else c)
sumIdx = 0
artIdx = 0
nSum = sum(1 for _, op, _ in constraints if op in ['<=', '>='])
nArt = sum(1 for _, op, _ in constraints if op in ['=', '>='])
tableau = np.zeros((n_cons + 1, n_vars + nSum + nArt + 1))
curr_sumFirst = n_vars
curr_art = n_vars + nSum
for i, (k, op, rhs) in enumerate(constraints):
    tableau[i, :n_vars] = k
    tableau[i, -1] = rhs
    if op == '<=':
        tableau[i, curr_sumFirst] = 1
        curr_sumFirst += 1
    elif op == '>=':
        tableau[i, curr_sumFirst] = -1
        tableau[i, curr_art] = 1
        tableau[n_cons, curr_art] = M
        curr_sumFirst += 1
        curr_art += 1
    elif op == '=':
        tableau[i, curr_art] = 1
        tableau[n_cons, curr_art] = M
        curr_art += 1
tableau[n_cons, :n_vars] = obj

for i in range(n_cons):
    for j in range(n_vars + nSum, n_vars + nSum + nArt):
        if tableau[i, j] == 1:
            tableau[n_cons, :] -= M * tableau[i, :]



result_tab = simplex(tableau)
if isinstance(result_tab, str):
    print("Область не ограниченна -- решений нет")
else:
    x = np.zeros(n_vars)
    for j in range(n_vars):
        col = result_tab[:, j]
        if np.sum(col == 1) == 1 and np.sum(col == 0) == len(col) - 1:
            row = np.where(col == 1)[0][0]
            x[j] = result_tab[row, -1]
    z_opt = result_tab[-1, -1] if mode == 'min' else -result_tab[-1, -1]
    print(f"Оптимальная точка: {x}")
    print(f"Значение Z: {-z_opt}")
    print()
    print("Двойственная задача:")
    print("Оптимальные значения двойственных переменных (y):")
    dual_vars = result_tab[-1, n_vars:n_vars + n_cons]
    print(f"y = {np.abs(dual_vars)}")