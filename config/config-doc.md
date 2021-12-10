
# DOCUMENTATION FOR THE CONFIG FILE
## An explanation of the different variables, and how to use them

The config file is the place where the entire application takes the variables to use them everywhere. Changing variables in the config file allows you to change the behaviour of the whole application in one go.
Caution! Changing these variables can also break the application if the rules are not followed.   
Make sure to use the rules of YAML language to write this file, and the additional rules specified below. 


### **The runConfig section**

This section contains general use variables, that are used within the application, not to interact with the exterior. 

Here are the rules to modify these variables: 


> nbProcess: default     

Accepts an integer (strictly positive) or one of the values: 'default'.
Sets the number of processes to the given parameter.
- 'default' calculates for the number of processors you have (One per processor)
-  any strictly positive integer: sets the number of processes to this number.
    
> talkative:

Every option accepts a boolean. 
Activates messages in the terminal. Useful in debug. 
Multiple options are available:
    
- processes: True    
    To see the messages of the processes starting/ending
    
- messages: True    
    To see a print everytime a message is sent/recieved between two processes.

- ias: False    
    To see a message when a blackbox finishes dealing with an image.
    Shows the results of the image dealings. 

- ias-detailed: False    
    To see every single message from inside the blackboxes, IA per IA.

- loader: False     
    To see when the loader loads its images. 

- tensorflow: '4'
    This must be an integer: 0, 1, 2, 3, or 4.
    Refer to tensorflow's 'TF_CPP_MIN_LOG_LEVEL' environment variable for more information.   

> logs

The same as talkative, but for printing in the logs file instead.
There is no logging for the tensorflow debuging messages. 

> gui:

To activate/deactivate graphics components. 

- showImages: True 
    Accepts a boolean.      
    Shows each image when processed by a blackbox. Displaying will stop the Blackbox from processing other images while the image is on display. You can stop the display by closing the window for display, or pressing any key. 
    

### **The output section**

This section concerns the variables used to interact with files and the exterior in general. 

> data: ../out/data.json          

Accepts a Json file path.
This is the output for the application. In this Json file are written the results for each image. 

> testData: ../out/testData.json  

Accepts a Json file path.
An other output file where we dump stuff that does not really matter.

> tempData: ../out/temp

Accepts a directory path. 
A directory where images are stored as a cache file when imported from a distant repository. 


### **The input section**

> trainingImagesFolder: ../img/train/trainingTestImages

Accepts a directory path. 
The home folder for all images used to train our ia. 

> shoeDetectAndExtractTrainData: ../in/trainData.json     

Accepts a json file. 
The data to train the IA that detects the presence of sneakers .

> shoeTypeTrainData: ../in/trainData.json

Accepts a json file. 
The data to train the IA that detects the type of sneaker.


### **The loader section**

Determines how the Loader, that loads images for the application to process, will behave.

> takeFromLocalSource: True

Accepts a boolean. 
Tells the loader to fetch the images from a local directory (when True), or from an FTP server (when False).  
      
> localImgSrc: ../img/test/

Accepts a directory path.
Tells the loader where to fetch images when in local source mode. 

> remoteImgSrc: /resources

Accepts a directory path, for the FTP server. 
Tells the loader where to find its images on the FTP server. 

Accepts a directory path.
Tells the loader where to fetch images when in local source mode. 


> batchSize: 4      

Accepts a strictly positive integer. 
Each time the loader loads images, how many should it load at once? 

> reloadNumber: 2

Accepts a positive integer. 
When we reach this number of loaded images or less, we try to load more.



### **The background section**

Variable that are there. Do NOT touch them. Please. You'll break everything. 


### **The color_detection section**

Variables governing the IA for detecting the color of the shoe. These have been tuned already, so changing them should not be necessary. 

> attemps: 10

Accepts a strictly positive integer. 
Max iteration for the kmeans function.

> margin: 20

Accepts a strictly positive integer.
The margin for pixel detection when calculating the ratios of colors present. 

> seuil: 0.25

Accepts a float in the interval \[0,1].
The threshold below which the preprocessing module will not try to contrast the images more. Contrasting images can be necessary for some images where the shoe has the same color as the background, in order for it to be detected.   


### **The shoeDetection section**

> modelFilePath: ../in/AI/DetectShoes/model.h5

Accepts a .h5 file, representing the (tensorflow) model for the IA that detects shoes. 

> weightsFilePath: ../in/AI/DetectShoes/weights.h5

Accepts a .h5 file, representing the (tensorflow) weights for the IA that detects shoes. 