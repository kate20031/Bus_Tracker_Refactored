## @file
#  @brief Factory module for selecting a speed calculation strategy.
#
#  Provides a static factory class to return a specific speed calculation
#  strategy implementation based on a given name.

from Zaliczeniowy_autobusy.BusTracker.data_processing.speed_calculation_strategy import \
    HaversineSpeedCalculationStrategy


## @class SpeedCalculationFactory
#  @brief Factory class for instantiating speed calculation strategies.
#
#  Currently supports the "haversine" strategy, but is designed for easy extension.
class SpeedCalculationFactory:
    ## @brief Returns an instance of a speed calculation strategy based on the given name.
    #
    #  @param strategy_name Name of the strategy to be returned (e.g., "haversine").
    #  @return Instance of a speed calculation strategy.
    #  @throws ValueError if the strategy name is unknown.
    @staticmethod
    def get_strategy(strategy_name: str):
        if strategy_name == "haversine":
            return HaversineSpeedCalculationStrategy()
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")
