from typing import Tuple

import cplex
from cplex.exceptions import CplexSolverError


class Base():

    def linear_model(self, num_decision_var: int, dummy: list, A: list,
                     b: list, c: list,
                     constraint_types: list, p_id: int, sense="minimize") -> Tuple[list, int]:
        # create cplex model
        model = cplex.Cplex()
        model.parameters.mip.tolerances.integrality.set(0)

        num_dummy_var = len(dummy)
        num_constraints = len(constraint_types)
        num_total_var = num_dummy_var + num_decision_var

        # add the decision variables
        # obs: lower bound is 0.0 by default
        model.variables.add(names=["x" + str(i)
                            for i in range(0, num_total_var)], types=[model.variables.type.integer] * num_total_var)

        # add the objective function
        model.objective.set_linear([(i, c[i]) for i in range(0, num_total_var)])

        # add the constrains related to dummy variables
        for i in range(num_dummy_var):
            model.linear_constraints.add(
                lin_expr=[cplex.SparsePair(
                    ind=[dummy[i][0]], val=[1])],
                rhs=[dummy[i][1]],
                names=['c' + str(i + 1)],
                senses=[dummy[i][2]]
            )

        # add the constrains related to decision variables
        for i in range(num_constraints):
            model.linear_constraints.add(
                lin_expr=[cplex.SparsePair(
                    ind=[j for j in range(num_dummy_var, num_total_var)], val=A[i])],
                rhs=[b[i]],
                names=['c' + str(num_dummy_var + i + 1)],
                senses=[constraint_types[i]]
            )

        # set sense of the problem
        if sense == "minimize":
            model.objective.set_sense(model.objective.sense.minimize)
        else:
            model.objective.set_sense(model.objective.sense.maximize)

        model.set_log_stream(None)
        model.set_warning_stream(None)
        model.set_results_stream(None)

        model.write("teste"+str(p_id)+'.lp')
        
        try:
            model.solve()
            return model.solution.get_values(), model.solution.get_objective_value()
        except CplexSolverError:
            return None, None
