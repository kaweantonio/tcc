import cplex

num_variables = 3
num_constrains = 1

A = [
    [30, 40, 60]
]

b = [130]

c = [30, 42, 66]

constrains_types = ["L"]

model = cplex.Cplex()

model.variables.add(obj=c, names=["x" + str(i)
                                  for i in range(1, num_variables + 1)])

model.variables.set_types([(i, model.variables.type.integer)
                           for i in range(0, num_variables)])

for i in range(num_constrains):
    model.linear_constraints.add(
        lin_expr=[cplex.SparsePair(
            ind=[j for j in range(num_variables)], val=A[i])],
        rhs=[b[i]],
        names=['c' + str(i + 1)],
        senses=[constrains_types[i]]
    )

model.objective.set_sense(model.objective.sense.maximize)

model.solve()
print(model.solution.get_objective_value())
print(model.solution.get_values())
