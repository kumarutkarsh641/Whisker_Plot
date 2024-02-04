import os
import logging
from getdist import plots
from natsort import natsorted

class ChainAnalysis:
    def __init__(self, base_directory, parameters, subfolder_name="chains"):
        self.base_directory = base_directory
        self.parameters = parameters
        self.subfolder_name = subfolder_name # Store the name of the subfolder
        self.folder_names = []
        self.folder_paths = []
        self.chains_dict = {}
        self.samples = []
        self.result_dict = {}
        self.suppress_logs()
        self.values_dict = {param: {'means': [], 'uppers': [], 'lowers': [], 'yerr': []} for param in parameters}

    def suppress_logs(self):
        class SuppressSpecificLog(logging.Filter):
            def filter(self, record):
                unwanted_messages = [
                    "fine_bins not large enough to well sample smoothing scale - chi2__CMB",
                    "fine_bins not large enough to well sample smoothing scale - chi2",
                    "fine_bins not large enough to well sample smoothing scale - chi2__planck_2018_highl_plik.TTTEEE",
                    "fine_bins not large enough to well sample smoothing scale - chi2__planck_2018_lensing.clik",
                    "auto bandwidth for chi2 very small or failed",
                    "auto bandwidth for Alens very small or failed",
                ]
                return not any(unwanted_msg in record.msg for unwanted_msg in unwanted_messages)

        logger = logging.getLogger("root")
        logger.addFilter(SuppressSpecificLog())

    def get_folders(self):
        self.folder_paths = [os.path.join(self.base_directory, d) for d in os.listdir(self.base_directory) if os.path.isdir(os.path.join(self.base_directory, d))]
        self.folder_names = [f for f in os.listdir(self.base_directory) if os.path.isdir(os.path.join(self.base_directory, f))]
        self.folder_names = natsorted(self.folder_names)
        self.folder_paths = natsorted(self.folder_paths)

    def get_chains(self):
        for folder in self.folder_names:
            folder_path = os.path.join(self.base_directory, folder)
            chain_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
            
            # If no .txt files are found directly in the folder, look in the subfolder
            if not chain_files:
                subfolder_path = os.path.join(folder_path, self.subfolder_name)
                if os.path.exists(subfolder_path):
                    chain_files = [f for f in os.listdir(subfolder_path) if f.endswith('.txt')]
                else:
                    print(f"No '{self.subfolder_name}' subfolder found in folder: {folder}")
            
            self.chains_dict[folder] = chain_files
            if not chain_files:  # If still no .txt files found, print a message
                print(f"No .txt files found in folder or '{self.subfolder_name}' subfolder: {folder}")

    def get_samples(self):
        for i in range(len(self.folder_names)):
            self.samples.append('S'+ self.folder_names[i])

    def get_results(self):
        for folder in self.folder_names:
            g = plots.get_subplot_plotter(chain_dir=self.folder_paths)
            roots = []
            for i in range(len(self.folder_names)):
                file_name_without_extension = os.path.splitext(self.chains_dict[self.folder_names[i]][0])[0]
                file_name_without_extension1 = os.path.splitext(file_name_without_extension)[0]
                roots.append(file_name_without_extension1)

            for item1, item2 in zip(self.samples, roots):
                self.result_dict[item1] = g.sample_analyser.samples_for_root(item2)
    
    def print_parameter_constraints(self, parameter):
        if parameter in self.values_dict:
            means = self.values_dict[parameter]['means']
            uppers = self.values_dict[parameter]['uppers']
            lowers = self.values_dict[parameter]['lowers']
            yerr = self.values_dict[parameter]['yerr']

            print(f"Parameter: {parameter}")
            for i in range(len(means)):
                print(f"Sample {self.samples[i]}:")
                print(f"Mean: {means[i]}")
                print(f"Upper: {uppers[i]}")
                print(f"Lower: {lowers[i]}")
                print(f"Yerr: {yerr[i]}")
                print()
        else:
            print(f"No constraints found for parameter: {parameter}")

    def get_latex_values(self):
        for param in self.parameters:
            latex_values = [self.result_dict[sample].getLatex(param, limit=1) for sample in self.samples]
            for item in latex_values:
                if "\\pm" in item:
                    parts = item.split('\\pm')
                    mean = float(parts[0].split('=')[1].strip())
                    uncertainty = float(parts[1].strip())
                    self.values_dict[param]['means'].append(mean)
                    self.values_dict[param]['uppers'].append(mean + uncertainty)
                    self.values_dict[param]['lowers'].append(mean - uncertainty)
                elif "^{" in item and "_{" in item and "=" in item:
                    parts = item.split('^{')[0].split('=')
                    if len(parts) > 1:
                        mean_str = parts[1].strip()
                        mean = float(mean_str)
                        upper = float(item.split('^{')[1].split('}')[0].replace('+', ''))
                        lower = float(item.split('_{')[1].split('}')[0].replace('-', ''))
                        self.values_dict[param]['means'].append(mean)
                        self.values_dict[param]['uppers'].append(mean + upper)
                        self.values_dict[param]['lowers'].append(mean - lower)
                elif ">" in item:
                    mean = float(item.split('>')[1].strip())
                    self.values_dict[param]['means'].append(mean)
                    self.values_dict[param]['uppers'].append(0)
                    self.values_dict[param]['lowers'].append(0)
                elif "<" in item:
                    mean = -float(item.split('<')[1].strip())
                    self.values_dict[param]['means'].append(mean)
                    self.values_dict[param]['uppers'].append(0)
                    self.values_dict[param]['lowers'].append(0)
                else:
                    print(f"Pattern mismatch for: {item}")

    def calculate_yerr(self):
        for param in self.parameters:
            self.values_dict[param]['yerr'] = [(mean - lower, upper - mean) for mean, upper, lower in zip(self.values_dict[param]['means'], self.values_dict[param]['uppers'], self.values_dict[param]['lowers'])]

    def analyze(self):
        self.suppress_logs()
        self.get_folders()
        self.get_chains()
        self.get_samples()
        self.get_results()
        self.get_latex_values()
        self.calculate_yerr()