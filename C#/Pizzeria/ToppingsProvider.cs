
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

