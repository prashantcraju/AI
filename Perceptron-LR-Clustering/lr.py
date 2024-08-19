import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from matplotlib import cm
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D
import csv


def visualize_3d(df, lin_reg_weights=[1,1,1], feat1=0, feat2=1, labels=2,
                 xlim=(-1, 1), ylim=(-1, 1), zlim=(0, 3),
                 alpha=0., xlabel='age', ylabel='weight', zlabel='height',
                 title=''):
    """
    3D surface plot.
    Main args:
      - df: dataframe with feat1, feat2, and labels
      - feat1: int/string column name of first feature
      - feat2: int/string column name of second feature
      - labels: int/string column name of labels
      - lin_reg_weights: [b_0, b_1 , b_2] list of float weights in order
    Optional args:
      - x,y,zlim: axes boundaries. Default to -1 to 1 normalized feature values.
      - alpha: step size of this model, for title only
      - x,y,z labels: for display only
      - title: title of plot
    """

    # Setup 3D figure
    ax = plt.figure().gca(projection='3d')

    # Add scatter plot
    ax.scatter(df[feat1], df[feat2], df[labels])

    # Set axes spacings for age, weight, height
    axes1 = np.arange(xlim[0], xlim[1], step=.05)  # age
    axes2 = np.arange(xlim[0], ylim[1], step=.05)  # weight
    axes1, axes2 = np.meshgrid(axes1, axes2)
    axes3 = np.array( [lin_reg_weights[0] +
                       lin_reg_weights[1]*f1 +
                       lin_reg_weights[2]*f2  # height
                       for f1, f2 in zip(axes1, axes2)] )
    plane = ax.plot_surface(axes1, axes2, axes3, cmap=cm.Spectral,
                            antialiased=False, rstride=1, cstride=1)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    ax.set_xlim3d(xlim)
    ax.set_ylim3d(ylim)
    ax.set_zlim3d(zlim)

    if title == '':
        title = 'LinReg Height with Alpha %f' % alpha
    ax.set_title(title)

    plt.show()

def feature(x,weight):
    y = x.dot(weight)
    return y

def emp_risk(df, weight, rBeta):
    
    ind = 0
    
    for r3 in range(0,len(df)):
        data = [1, df.iloc[r3][0], df.iloc[r3][1]]
        x = np.array(data)
        predict_lin_model = feature(x=x, weight=weight)
        y = df.iloc[r3][2]
        
        if rBeta > 0:
            x_base_ij = df.iloc[r3][rBeta-1]
            ind = ind + (predict_lin_model - y)*x_base_ij
        else:
            ind = ind + (predict_lin_model - y)
    return ind

def gradientDescent(df, learning_rates, outputfile, num_iters = 100):

    csv_file = open(outputfile, 'w', newline='')
    writer = csv.writer(csv_file)
    wt1 = list()
    wt2 = list()

    nTerms = len(df)

    for lr in learning_rates:
        weights = [0, 0, 0]
        
        if lr == 0.009:
            num_iters = 130
        
        for r1 in range(0, num_iters):
            dataDerived = [1, 1, 1]
            
            for r2 in range(0, 3):
                dataDerived[r2] = emp_risk(df=df, weight=weights, rBeta=r2)
                dataDerived[r2] = weights[r2] - lr * (1/nTerms) * dataDerived[r2]
                
                weights = [dataDerived[0], dataDerived[1], dataDerived[2]]

        wt1.append([lr,r1+1,weights[0], weights[1], weights[2]])
        
        wt2.append([weights[0], weights[1], weights[2]])
    
    writer.writerows(wt1)
    
    csv_file.close()
    
    return wt2


def scaledFeature(df):
    
    for r1 in range(2):
        
        meanFeat = np.mean(df.loc[:,r1])
        
        stanDevFeat = np.std(df.loc[:,r1])
        
        tp = (df.loc[:,r1] - meanFeat)
        
        df.loc[:,r1] = (df.loc[:,r1] - meanFeat)/stanDevFeat
    
    return df

if __name__ == "__main__":
    #======== INPUT1.CSV =======#
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]

    # Import input1.csv, without headers for easier indexing
    data = pd.read_csv(inputfile, header=None)

    df = scaledFeature(df=data)

    learning_rates = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 0.009]

    # Sample meshgrid using arbitrary linreg weights
    col_names = list(data)
    lin_reg_weights = gradientDescent(df=df, learning_rates=learning_rates, outputfile=outputfile)
    ind = 0



