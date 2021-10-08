# -*- coding: utf-8 -*-
"""
@author: kevin.stanton

This function computes active and passive seismic coeffients for a retaining wall. 
The orientation of the acceleration field is determined based on PGA and the ratio
of ha to hv. The script automatically analyzed a range of failure surface angles 
and returns the angle and associated values for the case with the lowest computed
safety factor. 

Parameters
----------
    phi : float
        - effective friction angle (degrees)
    c : float
        - cohesion (kPa)
    PGA : float
        - peak ground acceleration (g)
    gamma : float (optional)
        - unit weight of soil (kN/m^3)
        - Only require if c>0 (default=0)
    H : float (optional)
        - height of cohesive zone (m)
        - default = 0
    beta : float (optional)
        - angle against vertical of the slope of the wall on the backfill side (degrees)
    i : float (optional)
        - angle with horizontal backfill slope (degrees)
        - default = 0
    q : str (optional)
        - surcharge (kPa)
    hvRatio : float (optional)
        - ratio of ha to hv 
        - default = 0
    delta : float (optional)
        - friction angle between soil and wall (degrees)
        - default = (2/3)*phi
    
Returns
-------
    Kae : float
        - active earth pressure coeffient associated with the governing failure surface angle
    alphaFa : float
        - governing failure surface angle for the active case (degrees)
    Kpe : float
        - active earth pressure coeffient associated with the governing failure surface angle
    alphaFp : float
        - governing failure surface angle for the active case (degrees)
    theta : float
        - orientation of the applied acceleration field with respect to horizontal (degrees)
"""



def wall_pressure_coefficients(phi, c, PGA, gamma=0, H=0, beta = 0, i = 0, q = 0, hvRatio = 0, delta = 0):
    
    # Import libraries
    import numpy as np
    
    # Compute parameters from inputs
    kh = PGA/9.81 # horizontal pseudo-static acceleration 
    kv = kh*hvRatio # vertical pseudo-static acceleration
    theta = np.arctan(kh/(1-kv)) # orientation of acceleration field
    
    # Convert degrees to radians
    beta = np.deg2rad(beta)
    i = np.deg2rad(i)
    phi = np.deg2rad(phi)
    delta = np.deg2rad(delta)
    
    if delta == 0:
        delta = 2*phi/3
        
    if c > 0:
        if gamma == 0 or H == 0:
            raise AssertionError("Unit weight and layer depth must be specified for cohesive soils.")
    
    # Find value for critical failure surface (i.e. dKae/d[alpha]=0)   
    Kae = 0
    Kpe = 0
    alphaFa = 0
    alphaFp = 0
    for x in range(30,70):
        
        alpha = np.deg2rad(x)
        
        # Compute the active and passive lateral seismic coefficients 
        Kae1 = np.sin(alpha-phi+theta)*np.cos(alpha-beta)*(np.cos(beta-i)+2*q*np.cos(beta)/(gamma*H*(1-kv)))\
            /((np.cos(beta)**2)*np.cos(theta)*np.sin(alpha-i)*np.cos(alpha-beta-phi-delta))\
            -2*c*np.cos(beta-i)*np.cos(phi)/(gamma*H*(1-kv)*np.cos(beta)*np.sin(alpha-i)*np.cos(alpha-beta-phi-delta))
            
        Kpe1 = np.sin(alpha-phi+theta)*np.cos(alpha-beta)*(np.cos(beta-i)+2*q*np.cos(beta)/(gamma*H*(1-kv)))\
            /((np.cos(beta)**2)*np.cos(theta)*np.sin(alpha-i)*np.cos(alpha-beta-phi-delta))\
            +2*c*np.cos(beta-i)*np.cos(phi)/(gamma*H*(1-kv)*np.cos(beta)*np.sin(alpha-i)*np.cos(alpha-beta-phi-delta))
        
        print((np.cos(beta)**2))
        
        # Keep if value governs
        if Kae1 > Kae:
            Kae = Kae1
            alphaFa = x
            
        if Kpe1 > Kpe:
            Kpe = Kpe1
            alphaFp = x
    
    theta = np.rad2deg(theta)    
    return Kae, alphaFa, Kpe, alphaFp, theta
        
        
  
        
    
    