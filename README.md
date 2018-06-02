# Income Class Cluster Evaluator
The ICCE is able to calculate a cluster index for a certain area indicating its degree of income segregation based on census tract data.

## Usage
In order to use the ICCE clone the git repository with `git clone https://github.com/jonaspfab/icce.git`. In order to execute the application run `python app.py` in the root directory of the project.

## Data Sources
The cluster index is calculated based on census tract data fetched from the [Data USA API](https://datausa.io/about/api/). Additionally, adjacent census tracts are determined with the help of a [csv file](https://s4.ad.brown.edu/Projects/Diversity/Researcher/Pooling.htm) from Brown University.

## Methdology
The calculated cluster index represents the likelihood that a census tract is in the same income class as its adjacent census tract. The income class of a census tract is calculated by the following [rule](https://inequality.stanford.edu/income-segregation-maps/6491).