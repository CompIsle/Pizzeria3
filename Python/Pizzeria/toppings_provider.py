'''
using System;
using System.Collections.Generic;
using static Pizzeria.GenericTopping;
using static Pizzeria.ToppingsProvider.Topping;

namespace Pizzeria;

    class ToppingsProvider {
        internal enum Topping { Chilli, Anchovy, Pepperoni }
        private readonly Dictionary<Topping, Func<IPizza, IPizza>> Toppings = new()
        {
            { Chilli, BuildPizzaTopping("Extra Chillis", c => c + 1.00M) },
            { Anchovy, BuildPizzaTopping("Anchovy", c => c + 0.80M) },
            { Pepperoni, BuildPizzaTopping("Spicy Pepperoni", c => c + 0.75M) }

        };
        public Func<IPizza, IPizza> this[Topping T] => Toppings[T];

        public static string[] AvailableToppings => Enum.GetNames(typeof(Topping));
    }
'''

from enum import StrEnum
from typing import Callable, Dict
from pizza import IPizza


class Topping(StrEnum):
    CHILLI = "Chilli"
    ANCHOVY = "Anchovy"
    PEPPERONI = "Pepperoni"

class ToppingsProvider:
    def __init__(self):
        self.toppings: Dict[Topping, Callable[[IPizza], IPizza]] = {
            Topping.CHILLI: self.build_pizza_topping("Extra Chillis", lambda c: c + 1.00),
            Topping.ANCHOVY: self.build_pizza_topping("Anchovy", lambda c: c + 0.80),
            Topping.PEPPERONI: self.build_pizza_topping("Spicy Pepperoni", lambda c: c + 0.75)
        }

    def __getitem__(self, topping: Topping) -> Callable[[IPizza], IPizza]:
        return self.toppings[topping]

    @staticmethod
    def build_pizza_topping(name: str, cost_func: Callable[[float], float]) -> Callable[[IPizza], IPizza]:
        def topping(pizza: IPizza) -> IPizza:
            pizza.add_topping(name, cost_func)
            return pizza
        return topping

    @staticmethod
    def available_toppings() -> list:
        return [topping.value for topping in Topping]
