import pandas as pd
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=True, nargs='+', type=str, dest="input")
    parser.add_argument('-o', '--output', required=True, type=str, dest="output")
    args = parser.parse_args()

    df_list = [pd.read_csv(i).groupby(["title", "author", "pub_year"]).size().reset_index() for i in args.input]
    df = pd.concat(df_list)
    df = df.groupby(["title", "author", "pub_year"]).size().reset_index(name='counts')
    df.sort_values(by=["counts", "pub_year"], inplace=True, ascending=False)
    df.to_csv(args.output, index=False)
