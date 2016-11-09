'''
Created on Oct 24, 2016

@author: benoit
'''
from jshadobf.transformations.rename_variables import rename_variables
from jshadobf.transformations.add_dummy_variables import add_dummy_variables
from jshadobf.transformations.add_dummy_exprs import add_dummy_exprs
from jshadobf.transformations.add_if_statement import add_if_statement
from jshadobf.transformations.add_if_statement_2 import add_if_statement_2
from jshadobf.transformations.modify_data_flow_1 import modify_data_flow_1
from jshadobf.transformations.modify_data_flow_2 import modify_data_flow_2
from jshadobf.transformations.modify_control_flow_1 import modify_control_flow_1
from jshadobf.transformations.change_str import change_str
from jshadobf.transformations.change_list import change_list
from jshadobf.transformations.aggregate_data import aggregate_data
from jshadobf.transformations.duplicate_function import duplicate_function
from jshadobf.transformations.outlining import outlining
from jshadobf.transformations.evalification import evalification
from jshadobf.transformations.simplify_if import simplify_if
from jshadobf.transformations.remove_empty_statement import remove_empty_statement
TRANSFORMATIONS = [rename_variables,
                   add_dummy_variables,
                   add_dummy_exprs,
                   add_if_statement,
                   add_if_statement_2,
                   modify_data_flow_1,
                   modify_data_flow_2,
                   modify_control_flow_1,
                   change_str,
                   change_list,
                   aggregate_data,
                   duplicate_function,
                   outlining,
                   evalification,

                   simplify_if,
                   remove_empty_statement,
                   ]
