namespace Pizzeria; 

interface IProduct {
    public string GetDescription { get; } //might be nicer to return a List<string> to allow higher level
                                          //level methods to choose a formatting strategy
    public decimal Cost();
}
