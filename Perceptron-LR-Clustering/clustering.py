import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines  as mlines
import imageio
from sklearn.cluster import KMeans

def k_means_clus(array, labels, width, height):
    dimension = array.shape[1]
    place = np.zeros((width,height,dimension))
    ind = 0
    for r1 in range(0,width):
        for r2 in range(0, height):
            place[r1][r2] = array[labels[ind]]
            ind += 1
    return place

def clustering():

    img1 = imageio.imread('trees.png', pilmode = 'RGB')
    
    img2 = img1.reshape(-1,3)

    k_means = KMeans(n_clusters=13, random_state=0).fit(img2)
    
    k_means_labels = k_means.predict(img2)

    img3 = img2.reshape(img1.shape)
    
    imageio.imwrite('temporary_image.png', k_means_clus(k_means.cluster_centers_,k_means_labels,img1.shape[0],img1.shape[1]))


if __name__ == "__main__":
    clustering()
