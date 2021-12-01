
# DOCUMENTATION FOR THE CONFIG FILE
## An explanation of the different variables, and how to use them

The config file is the place where the entire application takes the variables to use them everywhere. Changing variables in the config file allows you to change the behaviour of the whole application in one go.
Caution! Changing these variables can also break the application if the rules are not followed.   
Make sure to use the rules of YAML language to write this file, and the additional rules specified below. 


### **The runConfig section**

This section contains general use variables, that are used within the application, not to interact with the exterior. 

Here are the rules to modify these variables: 


> stopsAtEnd: True

Accepts a boolean (True or False).
Tells the application what to do when it has dealt with all of the images in the database. 
Setting to true will stop the application completely. Setting to false will keep the application on the lookout for more images. 

> nbProcess: default     

Accepts an integer (strictly positive) or one of the values: 'default', 'auto'.
Sets the number of processes to the given parameter.
- 'default' calculates for the number of processors you have (One per processor)
- 'auto' will auto adjusts the number of processes in accordance with the number of pending tasks
-  any strictly positive integer: sets the number of processes to this number.
    
> talkative:

Activates messages in the terminal. Useful in debug. 
Multiple options are available, and they all accept a boolean. 
    
- processes: True    
    To see the messages of the processes starting/ending
    
- messages: True    
    To see a message everytime a message is sent/recieved between two processes.

- ias: False    
    To see a message when a blackbox finishes dealing with an image.

- ias-detailed: False    
    To see every single message from inside the blackboxes, IA per IA.

- loader: False     
    To see when the loader loads its images. 
    
> gui:

To activate/deactivate graphics components. 

- showImages: True 
    Accepts a boolean.      
    Shows each image when processed by a blackbox. Displaying will stop the Blackbox from processing other images while the image is on display. You can stop the display by closing the window for display, or pressing any key. 
    
> dynamicConfig: False        

Accepts a boolean.
Setting to True reloads the configuration from the config file at each loop of the BlackBox and of the main.  
This allows you to change the config while the application is running and see the effects in live.      
/!\ Loading values from a file frequently has an impact on the running time of the app (not much, but still). 

/!\ If you want to set it to True, you NEED TO SET IT BEFORE RUNNING THE APPLICATION. 


### **The output section**

This section concerns the variables used to interact with files and the exterior in general. 

> data: ../out/data.json          

Accepts a Json file path.
This is the output for the application. In this Json file are written the results for each image. 

> testData: ../out/testData.json  

Accepts a Json file path.
An other output file where we dump stuff that does not really matter.


### **The loader section**

Determines how the Loader, that loads images for the application to process, will behave.

> takeFromLocalSource: True

Accepts a boolean. 
Tells the loader to fetch the images from a local directory, set in the next variable. 
      
> localImgSrc: ../img/test/

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