"""
using System;
using static Pizzeria.PizzaSize;

//for unit test
using System.Runtime.CompilerServices;
[assembly: InternalsVisibleTo("PizzaTester")]

namespace Pizzeria;

    public enum PizzaSize { Small, Medium, Large }

    /// <summary>
    /// IPizza implements IProduct adding a Size to the underlying interface's Cost and Description
    /// </summary>
    interface IPizza : IProduct {
        public PizzaSize Size { get; init; }

    }

    // ABC for all concrete pizzas and toppings.
    // Toppings also inherit from this class so that they may
    // have the correct type to be used as decorators.
    // An ABC is used so that a default implementation for Cost and GetDescription can be provided
    public abstract class SizedPizza : IPizza {
        public PizzaSize Size { get; init; } = Medium;

        internal abstract string Description { get; }

        public virtual string GetDescription { get => $"{Size} {Description}"; }

        public virtual decimal Cost() => 0m;

    }

    //The following concrete pizza class could be replaced by a PizzaProvider much
    //along the line of the toppings. However, this could wait until
    //a) there is a proper data provider (database => menu)
    //b) - there is a need - pizza bases probably do not change often
    class DeepPanPizza : SizedPizza {
        internal override string Description { get => "DeepPan Pizza"; }
        public override decimal Cost() =>
            Size switch
            {
                Large => 3.50M,
                Small => 2.00M,
                _ => 2.80M
            };
    }

    class ThinCrustPizza : SizedPizza {
        internal override string Description { get => "ThinCrust Pizza"; }
        public override decimal Cost() =>
            Size switch
            {
                Large => 3.20M,
                Small => 2.00M,
                _ => 2.50M
            };
    }


    /// <summary>
    /// A class for making new toppings
    /// Objects are obtained from the factory method
    /// BuildPizzaTopping(string Description, Func<decimal, decimal> Cost)
    /// Which takes the description of the toppping and a cost method which will
    /// modify the cost of whatever the topping decorates.
    /// There are two public methods:
    /// decimal Cost() which retuns the overall cost of the topped (decorated) object
    /// and string GetDescription() which provides a generated description
    /// </summary>
    class GenericTopping : SizedPizza {
        private readonly IPizza pizza;
        private readonly string description;
        private readonly Func<decimal, decimal> cost;

        internal override string Description => description;

        private GenericTopping(IPizza pizza, string description, Func<decimal, decimal> cost) {
            this.pizza = pizza;
            this.description = description;
            this.cost = cost;
        }

        public override string GetDescription => $"{Description} {pizza.GetDescription}";

        public override decimal Cost() => cost(pizza.Cost());

        public static Func<IPizza, IPizza> BuildPizzaTopping
            (string Description, Func<decimal, decimal> Cost) =>
                (P) => new GenericTopping(P, Description, Cost);

        public override string ToString() => GetDescription;

    }


    // Could use PizzaDecorator in place of Func<IPizza, IPizza>
    // and CostCalculator in place of Func<decimal, decimal> if those seems ugly to you
    //internal delegate IPizza PizzaDecorator(IPizza _);
    //internal delegate decimal CostCalculator(decimal _);
"""

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Callable


class PizzaSize(Enum):
    SMALL = auto
    MEDIUM = auto
    LARGE = auto


class IProduct(ABC):
    @property
    @abstractmethod
    @property
    def cost(self) -> float:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass


class IPizza(IProduct):
    def __init__(self, size: PizzaSize):
        self.size = size


class SizedPizza(IPizza):
    def __init__(self, size: PizzaSize = PizzaSize.MEDIUM):
        super().__init__(size)

    @property
    def description(self) -> str:
        raise NotImplementedError

    def get_description(self) -> str:
        return f"{self.size.name} {self.description}"

    @property
    def cost(self) -> float:
        return 0.0


class DeepPanPizza(SizedPizza):
    @property
    def description(self) -> str:
        return "DeepPan Pizza"

    @property
    def cost(self) -> float:
        return {PizzaSize.LARGE: 3.50, PizzaSize.SMALL: 2.00, PizzaSize.MEDIUM: 2.80}[
            self.size
        ]


class ThinCrustPizza(SizedPizza):

    @property
    def description(self) -> str:
        return "ThinCrust Pizza"

    @property
    def cost(self) -> float:
        return {PizzaSize.LARGE: 3.20, PizzaSize.SMALL: 2.00, PizzaSize.MEDIUM: 2.50}[
            self.size
        ]


class GenericTopping(SizedPizza):
    def __init__(self, pizza: IPizza, description: str, cost: Callable[[float], float]):
        super().__init__(pizza.size)
        self.pizza = pizza
        self._description = description
        self._cost = cost

    @property
    def description(self) -> str:
        return self._description

    def get_description(self) -> str:
        return f"{self.description} {self.pizza.get_description()}"

    @property
    def cost(self) -> float:
        return self._cost(self.pizza.cost())

    @staticmethod
    def build_pizza_topping(
        description: str, cost: Callable[[float], float]
    ) -> Callable[[IPizza], IPizza]:
        return lambda pizza: GenericTopping(pizza, description, cost)

    def __str__(self) -> str:
        return self.get_description()
