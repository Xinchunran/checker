from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
import argparse
import numpy as np
import sys
sc = StandardScaler()

def get_args():
    desc = "get input files"
    try:
        parser = argparse.ArgumentParser(
            description=desc, formatter_class=argparse.RawTextHelpFormatter
        )
        parser.add_argument(
            "dih",
            action="store",
            help="File of dih data file",
        )
        parser.add_argument(
            "rmsd",
            action="store",
            help="input rmsd data file",
        )
        parser.add_argument(
            "output",
            action="store",
            help='output the files',
        )
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            exit(1)
    except:
        sys.stderr.write(
            "An exception occurred with argument parsing. Check your provided options.\n"
        )

    return parser.parse_args()


def pca_analysis(xs: float, componets: int):
    pca = PCA(componets)
    xs_pca =  pca.fit_transform(xs)
    explained_variance = pca.explained_variance_ratio_
    return xs_pca, explained_variance

def fig_pca(xs_data: float, ys_data: float, fig_name: str):
    fig_dims = (7, 6)
    fig, ax = plt.subplots(figsize=fig_dims)
    sc = ax.scatter(xs_data[:,0], xs_data[:,1], c=ys_data, marker='.')
    ax.set_xlabel('PCA first principal component')
    ax.set_ylabel('PCA second principal component')
    plt.colorbar(sc, label='two components')
    plt.savefig(f"{fig_name}.pdf", format="pdf")
    return print("analyzing done")

def save_csv(Values:list, filename:str):
    with open("expln_var_"+filename+".txt", 'a') as f:
        f.write(','.join(map(str, Values)) + '\n')


def main():
    args = get_args()
    dihs, rmsds, outputs = args.dih, args.rmsd, args.output
    data = pd.read_csv(dihs, sep="\s+")
    values = pd.read_csv(rmsds, sep="\s+")
    Xs = data.iloc[:,1:]
    #X_scale = sc.fit_transform(Xs)
    print(Xs.shape)
    ys = values.iloc[:, -1]
    y = np.array(ys)
    pca_xs, expln = pca_analysis(Xs, int(Xs.shape[-1]))
    fig_pca(pca_xs, y, outputs)
    save_csv(expln, outputs)


if __name__ == "__main__":
    main()
