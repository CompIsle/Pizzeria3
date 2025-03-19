using Microsoft.VisualStudio.TestTools.UnitTesting;
using Pizzeria;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using static Pizzeria.ToppingsProvider.Topping;
using toppingList = System.Collections.Generic.List<Pizzeria.ToppingsProvider.Topping>;

namespace PizzaUnitTests;

record TestPizza {
    public IPizza P { get; init; }
    public toppingList ToppingList { get; init; }
    public string ExpectedDescription { get; init; }
    public decimal ExpectedCost { get; init; }
}

[TestClass]
    public class PizzaUnitTests {


    //Although the test methods are general the specific data being tested needs to accor
    List<TestPizza> TestPizzaData;
    
    [TestInitialize]
    public void TestInitialize() {
        TestPizzaData = new()
        {
            // ADD NEW KNOWN EXAMPLES BELOW AS SHOWN
            new TestPizza()
            {
                P = new DeepPanPizza(),
                ToppingList = new toppingList() { Anchovy, Chilli },
                ExpectedDescription = "Anchovy Chilli Medium DeepPan Pizza",
                ExpectedCost = 4.60M
            },
            new TestPizza()
            {
                P = new ThinCrustPizza() { Size = PizzaSize.Large },
                ToppingList = new toppingList() { Anchovy, Pepperoni },
                ExpectedDescription = "Anchovy Pepperoni Large ThinCrust Pizza",
                ExpectedCost = 4.75M
            },
        };
    }

    //If/when a PizzaProvider class is added, these two tests can be replaced by one
    //that simply checks all known pizzas have a valid description set
    [TestMethod]
        public void TestDeepPanDescription() {
            IPizza P = new DeepPanPizza();
            string s = P.GetDescription;
            //StringAssert.Contains(s, "DeepPan Pizza");
            string re = @".*[Small|Medium|Large]\s+\w+\s+Pizza";
            StringAssert.Matches(s, new Regex(re));
        }

        [TestMethod]
        public void TestThinCrustDescription() {
            IPizza P = new ThinCrustPizza();
            string s = P.GetDescription;
            //StringAssert.Contains(s, "ThinCrust Pizza");
            string re = @".*[Small|Medium|Large]\s+\w+\s+Pizza";
            StringAssert.Matches(s, new Regex(re));
        }

        
        [TestMethod]
        public void TestPizzaSizing() {
            string re = @".*[Small|Medium|Large]\s+\w+\s+Pizza";
            IPizza P = new DeepPanPizza() { Size = PizzaSize.Large};
            StringAssert.Matches(P.GetDescription, new Regex(re));
            P = new DeepPanPizza() { Size = PizzaSize.Medium };
            StringAssert.Matches(P.GetDescription, new Regex(re));
            P = new DeepPanPizza() { Size = PizzaSize.Small };
            StringAssert.Matches(P.GetDescription, new Regex(re));
        }

        [TestMethod]
        public void TestCostBarePizza() {
            IPizza P = new DeepPanPizza();
            decimal cost = P.Cost();
            Assert.AreNotEqual(cost, 0M);
        }

        [TestMethod]
        public void TestKnowValues() {
            ToppingsProvider TP = new();
            foreach (TestPizza test in TestPizzaData) {
                IPizza P = test.P;
                foreach (var T in test.ToppingList) {
                    P = TP[T](P);
                }
                Assert.AreEqual(test.ExpectedCost, P.Cost());
                StringAssert.Equals(test.ExpectedDescription, P.GetDescription);
            };
        }
    }
