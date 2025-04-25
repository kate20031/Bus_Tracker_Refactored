## @file
#  @brief Factory module for creating SpeedViolationChecker instances using specific strategies.
#
#  This module provides a factory class to create SpeedViolationChecker objects
#  with different speed calculation strategies.

from Zaliczeniowy_autobusy.BusTracker.data_processing.speed_calculation_factory import SpeedCalculationFactory
from Zaliczeniowy_autobusy.BusTracker.data_processing.speed_violation_checker import SpeedViolationChecker


## @class SpeedViolationCheckerFactory
#  @brief Factory class for creating SpeedViolationChecker instances.
#
#  This factory uses a named strategy to generate an appropriate SpeedViolationChecker.
class SpeedViolationCheckerFactory:
    ## @brief Creates a SpeedViolationChecker with the given strategy.
    #
    #  @param max_speed Maximum allowed speed for comparison.
    #  @param strategy_name Name of the speed calculation strategy to use (e.g. "haversine").
    #  @return SpeedViolationChecker instance using the specified strategy.
    @staticmethod
    def create_speed_violation_checker(max_speed: float, strategy_name: str) -> SpeedViolationChecker:
        strategy = SpeedCalculationFactory().get_strategy(strategy_name)
        return SpeedViolationChecker(max_speed, strategy)
