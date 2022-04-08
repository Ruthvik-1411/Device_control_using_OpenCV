# Device_control_using_OpenCV

The aim of this project is to control home appliances or random devices using simple gestures. In this case the appliances are controlled using a show a fingers. For instance if the user wants to control 4 devices such as a fan, light, AC and a TV. Each device is assigned a number, if you want to ON the first device say a fan, then the user can show a single finger towards the camera or the region in which the camera processes the data. The number of fingers shown by the user is detected and a control signal is sent to the relay or any switch that is connected to the controller. The number of fingers shown decides what appliance should be currently working. The same number of fingers can be shown again to switch OFF the device if its alredy working.  

There will be two modules working in parallel, one module indicates the number of fingers the user is holding and the other switches ON/OFF the devices. 
The working looks similar to this:<br><br>
<img src='https://github.com/Ruthvik-1411/Device_control_using_OpenCV/blob/main/Using_contours/dco_moment_01.jpg?raw=true'><br><br>
In the above image first 4 fingers are shown and 4 th device is switched ON. Later 2 fingers are shown. The implementation video can be found in the folder using_counters. To switch OFF all devices the user can show a closed palm indicating 0 fingers.
