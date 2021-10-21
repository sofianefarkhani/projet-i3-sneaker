from Data.Color import Color

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
import utils
import cv2
import numpy as np


class ColorDetector:
    
    
    
    def detectColorsOf(shoeImage, nomberClusters=2):
        '''Detects the two main colors of the given shoe, and returns them as a tuple.
        
        So far it only returns a dummy values.'''
        # print('Color detector attributed a color to the given image.')
        # return (Color(rgb = [13, 0, 255]), Color(rgb = [255, 71, 50]))

        '''Load image and convert it BGR to RGB cause to show im with matplotlib'''
        image = cv2.cvtColor(shoeImage, cv2.COLOR_BGR2RGB)

        '''Show image'''
        plt.figure()
        plt.axis("off")
        # plt.imshow(image)
        # plt.pause(20)

        '''Reshape and convert image in list of pixel'''
        image = image.reshape((image.shape[0] * image.shape[1], 3))
        #print(image)

        '''Generate number of cluster and regroup pixels'''
        clt = KMeans(n_clusters = nomberClusters)
        clt.fit(image)
        
        '''Give approximatly the same number of pixel for each cluster '''
        hist = ColorDetector.centroid_histogram(clt)
        # print(hist)

        #bar =  ColorDetector.plot_colors(hist, clt, nomberClusters)
        #plt.imshow(bar)

    def centroid_histogram(clt):     
        # saisir le nombre de grappes différentes et créer un histogramme   
        # basé sur le nombre de pixels assignés à chaque classification    
        numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)    
        (hist, _) = np.histogram(clt.labels_, bins = numLabels)   
        # normaliser l’histogramme de façon à ce qu’il ne fasse plus qu’un    
        hist = hist.astype("float")    
        hist /= hist.sum()    
        # retourne à l’histogramme    
        return hist

    def plot_colors(hist, centroids, nomberClusters):    
        # initialise le graphique à barres représentant la fréquence relative
        # de chacune des couleurs
        bar = np.zeros((50, 300, 3), dtype = "uint8")
        startX = 0
        # boucle sur le pourcentage de chaque cluster et la couleur de chaque groupe
        for i in range(max(len(hist),nomberClusters)):
            percent = hist[i]
            color = centroids[i]
            # tracer le pourcentage relatif de chaque groupe        
            endX = startX + (percent * 300)
            cv2.rectangle(bar, (int(startX), 0), (int(endX), 50), color.astype("uint8").tolist(), -1)
            startX = endX
        # renvoie le graphique à barres
        return bar