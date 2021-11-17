using Microsoft.VisualStudio.TestTools.UnitTesting;
using Pizzeria;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using static Pizzeria.ToppingsProvider.Topping;
using toppingList = System.Collections.Generic.List<Pizzeria.ToppingsProvider.Topping>;

namespace TP5 {
    [TestClass]
    public class UnitTest1 {
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


        Dictionary<(IPizza, toppingList),(string,decimal)> TestPizzas = new()
        {
            {
                (new ThinCrustPizza() {Size = PizzaSize.Medium},
                new toppingList() { Anchovy, Chilli} ),
                ("Pepperoni Anchovy Large ThinCrust Pizza", 4.30M)
            },
            {
                (new DeepPanPizza() {Size = PizzaSize.Medium},
                new toppingList() { Anchovy, Pepperoni} ),
                ("Anchovy Pepperoni Medium DeepPan Pizza", 4.35M)
            }

        };

        [TestMethod]
        public void TestTestDictionary() {
            ToppingsProvider TP = new();

            foreach (
                KeyValuePair<(IPizza, toppingList), (string, decimal)> KV in TestPizzas) {
                (IPizza P, toppingList TS) = KV.Key;
                foreach (ToppingsProvider.Topping thisTopping in TS)
                    P = TP[thisTopping](P);

                (string s, decimal c) = (P.GetDescription, P.Cost());
                (string expected_s, decimal expected_c) = KV.Value;

                Assert.AreEqual(expected_c, c);
                StringAssert.Equals(expected_s, s);
            }

        }
    }
}