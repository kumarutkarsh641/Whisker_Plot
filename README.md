# Whisker_Plot
Whisker_Plot
# Whisker Plot

Whisker Plot is a Python package designed for chain analysis and generating whisker plots. It provides tools for analyzing parameter chains and visualizing the results in a concise and clear manner.

## Installation

To install Whisker Plot, you can use pip:

bash
pip install git+https://github.com/yourusername/Whisker_Plot.git


Replace `yourusername` with your actual GitHub username.

Make Sure The package directory is not in PYTHONPATH: If you're trying to import the module without installing it via pip, ensure the directory containing your package is in the PYTHONPATH environment variable. You can temporarily add it with:

    export PYTHONPATH="${PYTHONPATH}:/path/to/your/package"


## Usage

Here is a simple example of how to use the Whisker Plot package:

python
from Whisker_Plot import ChainAnalysis

Initialize the ChainAnalysis with the base directory and parameters
analysis = ChainAnalysis(base_directory="path/to/base", parameters=["param1", "param2"])
Perform the analysis
analysis.analyze()
Print parameter constraints
analysis.print_parameter_constraints("param1")


## Features

- Chain analysis for parameter estimation
- Generation of whisker plots for visual comparison
- Customizable analysis for different datasets

## Contributing

Contributions to Whisker Plot are welcome! Please refer to the contributing guidelines for more information.

## License

Whisker Plot is released under the MIT License. See the LICENSE file for more details.
