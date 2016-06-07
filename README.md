# Huemovie
Set the mood with this Python script that changes the colour of your Philips Hue globes to match the scene of whatever you're watching on your Mac.

## Requirements
This script requires Python 2.6+, but at this stage won't work with 3+. All dependencies are included in requirements.txt. To install, simply run:
```pip install -r requirements.txt```

## Configuration
Change these variables to suit your requirements.
```
sample_rate = 5                             # Frames per Second. Philips Hue documentation recommends no more than 10 requests per second, so try and stay below 10.
sample_size = 50                            # Resize the screenshot to this size
brightness_threshold = 5                    # Turn the lights off completely when brightness below this value (max 255)
density_threshold = 0.01                    # Ignore colours below a certain density
num_globes = 3                              # Number of hue globes to update
```

This script looks for environment variables called HUE_BRIDGE_IP and HUE_USERNAME.
```
ip = os.environ['HUE_BRIDGE_IP']            # IP of your Hue Bridge. nano ~/.bash_profile and add: export HUE_BRIDGE_IP="XXX.XXX.XXX.XXX"
username = os.environ['HUE_USERNAME']       # Username set up on your Hue Bridge.
```

## How it works
Huemovie works by taking a screenshot multiple times a second. It converts the screenshot to an adaptive RGB palette that's the size of the number of globes you own. It then loops through this palette and sends that colour to the globe.

## Running
Simply load of Netflix or your favourite player, open bash and type:
```python huemovie.py```

The script will run on a loop until you cancel it.
