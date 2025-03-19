from ase.atoms import Atoms
from ase.build import bulk as _bulk
from atomistics.workflows import (
    optimize_positions_and_volume as _optimize_positions_and_volume,
)
from atomistics.workflows.evcurve.helper import (
    analyse_structures_helper,
    generate_structures_helper,
)
from atomistics.calculators import (
    evaluate_with_lammpslib as _evaluate_with_lammpslib, 
    get_potential_by_name as _get_potential_by_name,
)
import pandas
from pyiron_workflow import as_function_node


@as_function_node("atoms")
def bulk(name: str, cubic: bool = False) -> Atoms:
    return _bulk(name=name, cubic=cubic)


@as_function_node("potential")
def get_potential_by_name(potential_name: str) -> pandas.Series:
    return _get_potential_by_name(potential_name=potential_name)


@as_function_node("task")
def optimize_positions_and_volume(structure: Atoms) -> dict:
    return _optimize_positions_and_volume(structure=structure)


@as_function_node("result")
def evaluate_with_lammpslib(task_dict: dict, potential_dataframe: pandas.Series) -> dict:
    return _evaluate_with_lammpslib(task_dict=task_dict, potential_dataframe=potential_dataframe)


@as_function_node("task")
def evcurve_generate_structures(structure: dict, vol_range: float, num_points: int) -> dict:
    return {
        "calc_energy": generate_structures_helper(
            structure=structure["structure_with_optimized_positions_and_volume"],
            vol_range=vol_range,
            num_points=num_points,
        ),
    }


@as_function_node("fitdict")
def evcurve_analyse_structures(output_dict: dict, structure_dict: dict, fit_type: str = "polynomial", fit_order: int = 3) -> dict:
    return analyse_structures_helper(
        output_dict=output_dict,
        structure_dict=structure_dict["calc_energy"],
        fit_type=fit_type,
        fit_order=fit_order,
    )

