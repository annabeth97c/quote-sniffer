# quote-sniffer

[![Status](https://img.shields.io/badge/status-in%20development-orange.svg)](https://github.com/annabeth97c/quote-sniffer) [![Version](https://img.shields.io/badge/version-v0.0.1-blue.svg)](https://github.com/annabeth97c/quote-sniffer)

Simple StreamLit and FastApi app to find similar chunks / quotes across documents using Minimum LSH

## Usage

To use QuoteSniffer to find similarities in texts, follow these steps

### 1. Clone repository

Clone repository
```
git clone https://github.com/annabeth97c/quote-sniffer.git
```

Change directory into repository

```
cd quote-sniffer
```

### 2. Set Up Conda Environment

Create conda environment with environment.yml
```
conda env create -f environment.yml
```

Note: This creates an environment with the name quote-sniffer. If you would like an alternative name, please change the environment.yml file.

Activate the conda environment

```
conda activate quote-sniffer
```

### 3. Run QuoteSniffer

#### Running the backend

In a new terminal, with the conda environment activated, navigate to this repository's root folder and run the following command

```
python backend.py
```

#### Running the app

In a new terminal, with the conda environment activated, navigate to this repository's root folder and run the following command

```
streamlit run app.py
```

This should open the app in your default browser, but if it does not, simply visit 

```
http://localhost:8501
```

and you should be able to use the app
