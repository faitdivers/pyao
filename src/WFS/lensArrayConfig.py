# Lenslet array configuration
# Computers the lenslet centres for a rectangular array
from numpy import *

def lensletCentres(paramsSensor):
    # Unwrap paramsSensor
    lx = paramsSensor['lx'] # Width of the lenslet array in the x-direction [m]
    ly = paramsSensor['ly'] # Width of the lenslet array in the y-direction [m]
    D = paramsSensor['D'] # Lens diameter [m]
    dl = paramsSensor['dl'] # Distance between lenslets [m]
    noApertx = paramsSensor['noApertx'] # number of apertures in the x-direction
    noAperty = paramsSensor['noAperty'] # number of apertures in the y-direction	
    
    # Calculated missing parameters in paramsSensor	
    lensCentx = arange(noApertx)*(dl + D) + D/2 # Centers on x-axis [m]
    lensCenty = arange(noAperty)*(dl + D) + D/2 # Centers on y-axis [m]
    lensCentX, lensCentY = meshgrid(lensCentx, lensCenty) # Create rectangular grids for centres [m]   
    lensCentx = hstack(lensCentX) # Stack the rectangular grids [m]

    lensCenty = hstack(lensCentY) # Stack the rectangular grids [m]
    lCalx = (noApertx - 1.0)*(dl + D) + D # Calculated length of array in x-direction [m]
    lCaly = (noAperty - 1.0)*(dl + D) + D # Calculated length of array in y-direction [m]
	
    # Set supplied array size to calculated array size if supplied array size
    # is smaller then the calculated array size
    if lx < lCalx: 
        print "WARNING: the supplied array size in the x direction will be overwritten. Its size does not accommodate all the lenslets of the system. \nSupplied size: ", lx, "\nCalculated size: ", lCalx
        lx = lCalx
    if ly < lCaly:
        print "WARNING: the supplied array size in the y direction will be overwritten. Its size does not accommodate all the lenslets of the system. \nSupplied size: ", ly, "\nCalculated size: ", lCaly        
        ly = lCaly

    # Normalize lenslet centres
    lensCentx = lensCentx/lx
    lensCenty = lensCenty/ly    
    print("lensCentX:",lx)    
    return lx, ly, lensCentx, lensCenty