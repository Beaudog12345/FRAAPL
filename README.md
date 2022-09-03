# The F.R.A.A.P.L
The F.R.A.A.P.L, like all good things, is an overly complicated acronym that makes the thing you are talking about sound much more imposing. The F.R.A.A.P.L is the Facial Recognition based Auto-Aiming Pneumatic Launcher.

# The components
The F.R.A.A.P.L at its base is a Raspberry Pi 4 with 4g ram, and the Raspberry Pi camera. It is connected to, through a breadboard, a stepper motor (and controller), a servo, a PIR motion sensor, and an optocoupler powering a pneumatic solenoid. 

# The basic idea
The F.R.A.A.P.L will, upon receiving a signal from the motion detector, snap a photo of the surroundings. It will run this through a facial recognition system and pass the coordinates, if found, to the rest of the code. The code converts the camera coordinates to actual distance, and uses basic trigonometry to determine the stepper and servo angles. It passes these to code that targets the machine, and fires the solenoid.

# The firing mechanism
The F.R.A.A.P.L fires by releasing compressed air behind a foam bullet. The compressed air is from a 3D printed air compressor, because it needs little overall force.

# To Do
Wring
Finish designing, printing and testing compressor
Calibrating
Adding limit switches
Replace code placeholders
Other stuff I forgot

