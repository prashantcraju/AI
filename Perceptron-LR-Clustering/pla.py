import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from matplotlib import cm
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D
import csv

def visualize_scatter(df, feat1=0, feat2=1, labels=2, weights=[-1, -1, 1],
                      title=''):
    """
        Scatter plot feat1 vs feat2.
        Assumes +/- binary labels.
        Plots first and second columns by default.
        Args:
          - df: dataframe with feat1, feat2, and labels
          - feat1: column name of first feature
          - feat2: column name of second feature
          - labels: column name of labels
          - weights: [w1, w2, b]
    """

    # Draw color-coded scatter plot
    colors = pd.Series(['r' if label > 0 else 'b' for label in df[labels]])
    ax = df.plot(x=feat1, y=feat2, kind='scatter', c=colors)

    # Get scatter plot boundaries to define line boundaries
    xmin, xmax = ax.get_xlim()

    # Compute and draw line. ax + by + c = 0  =>  y = -a/b*x - c/b
    a = weights[0]
    b = weights[1]
    c = weights[2]

    def y(x):
        return (-a/b)*x - c/b

    line_start = (xmin, xmax)
    line_end = (y(xmin), y(xmax))
    line = mlines.Line2D(line_start, line_end, color='red')
    ax.add_line(line)


    if title == '':
        title = 'Scatter of feature %s vs %s' %(str(feat1), str(feat2))
    ax.set_title(title)

    plt.show()

def perceptron(df, outputfile):

    weights = [0,0,0]
    
    convRate = False
    
    csv_file = open(outputfile, 'w', newline='')
    
    writer = csv.writer(csv_file)
    
    wt1 = list()

    while not convRate:
        ind = 0
        for r1 in range(0, len(df)):
            data = [1, df.iloc[r1][0], df.iloc[r1][1]]
            func_of_x = np.array(data)
            dot_product = func_of_x.dot(weights)
            if (df.iloc[r1][2])*dot_product <= 0:
                weights[0] += df.iloc[r1][2]
                weights[1] += (df.iloc[r1][2])*df.iloc[r1][0]
                weights[2] += (df.iloc[r1][2])*df.iloc[r1][1]
                wt1.append([weights[0],weights[1],weights[2]])
            else:
                ind += 1
        if ind == len(df):
            convRate = True
    writer.writerows(wt1)
    csv_file.close()
    wt2 = [weights[0], weights[1], weights[2]]
    return wt2

if __name__ == "__main__":
    #======== INPUT1.CSV =======#
    print("Visualizing input1.csv")
    
    inputfile = sys.argv[1]
    
    outputfile = sys.argv[2]

    # Import input1.csv, without headers for easier indexing
    data = pd.read_csv(inputfile, header=None)
    weight = perceptron(data, outputfile = outputfile)


