# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 13:32:51 2018

@author: kevin.stanton

Notes:
    phi = effective friction angle
    c = cohesion
    PGA = peak ground acceleration (g)
    alpha = orientation of the failure surface
    beta = slope of the wall on the backfill side (angle with vertical)
    i = backfill slope (angle with horizontal)
    q = surcharge
    hvRatio = ratio of ha to hv
    delta = friction angle between wall and soil
"""



def Kae(phi, c, PGA, gamma=0, H=0, beta = 0, i = 0, q = 0, hvRatio = 0, delta = 0):
    
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
#    theta = np.deg2rad(theta)
    
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
        
        # Compute the active lateral seismic coefficient 
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
        
        
  
        
    
    