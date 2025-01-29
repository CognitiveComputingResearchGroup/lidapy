# lidapy

Contributions:

  Katie Killian:
    *Generated PyTesing to include both unit and integration testing. 
    *Generated comments for reference to each modules function
    *Initialized Modules and Functions - Environment (init, reset, step, render, and close)
    *Initialized Modules and Functions - Sensory Memory (init, add_sensory_listener, run_sensors and get_sensory_content), PAM (init, add_associations, retrieve associations)
    *Initialized the Motor-Plan execution Module to include the functions: execute
    *Modification into the Environment to include: assisting the agent to be aware of the surroudning tiles. Such as adding functions within the environment (updating position and get_surrounding_tiles) then adjusted the reset and step functions. 
    *Initialized the Agent class for the frozen lake and started initilizing the modules within, methods to include run.

  Nicole Vadillo:
    *Modified the Environment module to include action_space and step function
    *Modified the Sensory Memory module to include: reference to other modules (PAM and environment) and within functions to include references.
    *Modification wtihin the PAM module to include: aspects within the add & retrieve associations, within the learn function.
    *Initialized the Procedural Memory Module to include the functions: add_scheme and get_action.
    *initialized the Action Selection module and functions: select_action and notify-sensory-motor memory.
    *Modification within the Sensory Motor memory module: in aspects to the functions of the init (referencing to other modules). 
    *After adjustments for surrounding tiles, helped adjust other modules to fit for the adjustments within the enviornment for surrounding tiles information. 
    *Modifiacation of the Agent class to include initializing modules, modification within the various methods.  

  Brian Wachira: 
    *Generate PyTesting
    *Modified the Environment Module to include: randomizing the map, inside the reset function.
    *Modification wtih the Sensory Memory module: within the run_sensors function, get_sensory_content. 
    *Modification within the PAM module to include: aspects within the add & retrieve assocations, within the learn function.
    *Modification within the Action Selection module: aspects within the functions: select action and notify sensory motor memory
    *Initialized the Sensory Motor Memory module and functions: add_sensory_listener, receive action and send action execution command. 
    *Modificaitons within the agent class to include within various methods. 
    
