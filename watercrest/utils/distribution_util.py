import json

# TODO: make sympy an optional dependency
from sympy.stats import UniformSum, cdf
from pathlib import Path


class DistributionUtil:
    # dict([(indx, cls.cdf_uniform_sum(indx, 100)) for indx in range(101)])
    true_hit_distribution = json.load(open(Path(__file__).parent.joinpath("resources/true_hit_distribution.json"), "r"))

    @classmethod
    def cdf_uniform_sum(cls, z, maximum_value=2, n=2):
        # TODO: we should just look up the value for known distribution and interpolate
        if maximum_value != n:
            scaling_factor = n / maximum_value
            z = z * scaling_factor
        return float(cdf(UniformSum("x", n), evaluate=True)(z).doit())  # pyright: ignore

    @classmethod
    def get_true_hit_proba(cls, value):
        value_key = str(min(max(round(value), 0), 100))
        return cls.true_hit_distribution[value_key]
