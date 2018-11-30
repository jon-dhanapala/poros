import pandas as pd


def read_data(dir):
    iat = pd.read_csv('interarrival_times.csv')
    print(iat)

def main():
    # Run When Script is run

if __name__ == '__main__':
    main()
