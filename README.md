# Setup Environment

## Using Anaconda
```sh
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Using Shell/Terminal
```sh
mkdir Analysis-Data_-biker-Sharing_dicoding
cd Analysis-Data_-biker-Sharing_dicoding
pipenv install
pipenv shell
pip install -r requirements.txt
```

# Running the Streamlit App
```sh
streamlit run app.py
