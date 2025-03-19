'''
using static System.Console;
using static Pizzeria.PizzaSize; //enum
using static Pizzeria.ToppingsProvider.Topping; //enum

namespace Pizzeria;

    class Program {
        static void Main() {
            const string welcome = "Welcome to the Pizzeria!";
            WriteLine(welcome);
            WriteLine(new String('=', welcome.Length));

            //List the toppings
            foreach (string s in ToppingsProvider.AvailableToppings)
                WriteLine(s);

            //Get a toppings provider
            ToppingsProvider add_topping = new();

            ////
            /// Some examples showing how this is used
            /// The pizza base is constructed using traditional object construction with new()
            /// Pizza are stored in variable of type IPizza
            /// IPizza can be decorated with toppings stored in the ToppingsProvider.Toppings dictionary
            /// returning something also of (base) type IPizza
            /// IPizza types may have their descriptions and costs interrogated
            ///


            ///////////////Pizza One///////////////////
            IPizza thePizza = new DeepPanPizza();
            thePizza = add_topping[Anchovy](thePizza);
            thePizza = add_topping[Pepperoni](thePizza);
            //GetDescription is unnecessary, see following examples
            WriteLine($"{thePizza.GetDescription} which costs {thePizza.Cost()}");

            ////////////////Pizza Two/////////////////
            thePizza = new ThinCrustPizza() { Size = Large };
            thePizza = add_topping[Anchovy](thePizza);
            thePizza = add_topping[Pepperoni](thePizza);
            WriteLine($"{thePizza} which costs {thePizza.Cost()}");

            ///////////////Pizza Three////////////////
            ///// code implicitly allows multiple repeated toppings
            ///// do we want/need to disallow this?
            ///// Topping can be composited, although this may be harder to read
            thePizza = add_topping[Chilli](
                       add_topping[Anchovy](
                       add_topping[Anchovy](
                       new ThinCrustPizza()
                       )));
            WriteLine($"{thePizza} which costs {thePizza.Cost()}");
            //////////////////////////////////////////
        }
    }
'''

from pizza import IPizza, PizzaSize
from toppings_provider import ToppingsProvider

if __name__ == "__main__":
    WELCOME = "Welcome to the Pizzeria!"
    print(WELCOME)
    print("=" * len(WELCOME))

    for topping in ToppingsProvider.AvailableToppings:
        print(topping)

    add_topping = ToppingsProvider()

    # Pizza One
    the_pizza = DeepPanPizza()
    the_pizza = add_topping[ToppingsProvider.Topping.Anchovy](the_pizza)
    the_pizza = add_topping[ToppingsProvider.Topping.Pepperoni](the_pizza)
    print(f"{the_pizza.get_description()} which costs {the_pizza.cost()}")

    # Pizza Two
    the_pizza = ThinCrustPizza()
    the_pizza.size = PizzaSize.Large
    the_pizza = add_topping[ToppingsProvider.Topping.Anchovy](the_pizza)
    the_pizza = add_topping[ToppingsProvider.Topping.Pepperoni](the_pizza)
    print(f"{the_pizza.get_description()} which costs {the_pizza.cost()}")

    # Pizza Three
    the_pizza = add_topping[ToppingsProvider.Topping.Chilli](
                add_topping[ToppingsProvider.Topping.Anchovy](
                add_topping[ToppingsProvider.Topping.Anchovy](
                ThinCrustPizza()
                )))
    print(f"{the_pizza.get_description()} which costs {the_pizza.cost()}")
