import argparse
# from DataGen.datagen import Datagen
from Data_generation import Datagen

parser = argparse.ArgumentParser(description="Generate data")
parser.add_argument('inputPath', type=str, help='Path to YAML-configuration file')
parser.add_argument('lines', type=int, help='Number of lines in data')
parser.add_argument('outputPath', type=str, help='Path to save CSV-file')
args = parser.parse_args()


def generate():
    df_raw = Datagen(args.inputPath, args.lines).dataframe
    df_raw.to_csv(args.outputPath, index=False)


if __name__ == '__main__':
    generate()
