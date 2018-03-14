# Relief

A project developed to implement the machine learning relief algorithm. Uses python 3.x. Will find the feature that contributes least to determining the class of each entry.

### Running It

This section will explain the inputs and outputs of running the code. Use the provided csv to test the code.

#### Inputs

Provide the number of the corresponding csv. Note must be in the local directory.

```
Hello, Welcome to the Relief algorithm.
Please input the key number of the file you wish to open.
(0) Auto MPG.csv
(1) Other
0
```

Common to normalize the data in this algorithm ie put it in a bounded range but not crucial. It's worth noting the results differed significantly depending on this choice.

```
Normalize the data y/n?
y
```

#### Outputs

The following information is the when ran with the provided csv.

```
Working...
Finished Features...
Finished Phrasing...
Finished Normalizing...
Running relief algorithm...

Showing results...
mpg had a weight of -0.0472906
acceleration had a weight of -0.0501759
horsepower had a weight of -0.0507091
weight had a weight of -0.0643411
displacement had a weight of -0.14506
model year had a weight of -0.292712
cylinders had a weight of -0.351224
origin had a weight of -0.956633
```

## Authors

* **Will Irwin** - *Everything* - [Upgwades](https://github.com/Upgwades)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Stackoverflow was very helpful
* [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets.html)
