import Compression_Panel as cp
import numpy as np
from scipy.optimize import fsolve

### Constant Constants
E = 70_700e6
P_Width = 400e-3
P_length = 435e-3

F_dis = 100_000
Force = F_dis * P_Width

K_free = .477
K_hinged = 3.536

### Variables

#plate
P_thickness = 1e-3

#stiffeners
stiffeners = [4,4,4,4,4,4,4,4]
stiffeners = cp.stiffen_stiffeners(stiffeners)

### Calculations
P_thickness=0
load = Force / cp.Calc_Area(P_thickness, P_Width, stiffeners)
print("load", load * 10**-6, "MPa")
print("Area", cp.Calc_Area(P_thickness, P_Width, stiffeners)*10**6, "mm^2")
y_mid = cp.calc_y_mid(P_thickness,P_Width, stiffeners)
#print(y_mid*10**3, "mm")
I2 = cp.calc_I2(P_thickness,P_Width, stiffeners,y_mid)
print("Maximum force: ",4*np.pi**2*I2*E/P_length**2)


### plate buckling stability validation
free_min_len = cp.minimum_plane_length(P_thickness, K_free, E, load)
hinged_min_len = cp.minimum_plane_length(P_thickness, K_hinged, E, load)

print("maximum length btwn free stiffenerrs: ", free_min_len 	* 10**3, "mm")
print("maximum length btwn hinged stiffenerrs: ", hinged_min_len * 10**3, "mm")

#validate design
print(P_Width < 2*free_min_len + (len(stiffeners)-1)*hinged_min_len, ", free_space:", (2*free_min_len + (len(stiffeners)-1)*hinged_min_len - P_Width)*10**3, "mm")

###rivet spacing:
rivet_space = cp.min_rivet_spacing(P_thickness, E, load)
num_rivet_per_stiff = np.ceil(P_length / rivet_space) - 1





print("num of rivets: ", num_rivet_per_stiff*len(stiffeners))


### optimal plate stuff
free_l, hinged_l = fsolve(cp.find_optimal_plane_lengths,(free_min_len, hinged_min_len), args=(stiffeners, K_free, K_hinged))

print(free_l *10**3, hinged_l*10**3)

crit_load_thin_sheet = cp.sigmacrit(P_thickness,free_l,K_free, E)
print(cp.sigmacrit(P_thickness,free_l,K_free, E))
print(cp.sigmacrit(P_thickness,hinged_l,K_hinged, E))
print(crit_load_thin_sheet/load)




### 
y_mid = cp.calc_y_mid(P_thickness,P_Width, stiffeners)
#print(y_mid*10**3, "mm")
I2 = cp.calc_I2(P_thickness,P_Width, stiffeners,y_mid)
print(I2*10**12, "mm^4")



#print(cp.Newcalc_I2([0,0,0,8], P_thickness, P_Width, cp.Newcalc_y_mid([0,0,0,8],P_thickness, P_Width))*10**12, "mm^4")

force = cp.calc_beam_bending_max_force(P_length, E, I2)
print(force*10**-3, "kN")


print(cp.Calc_Area(P_thickness, P_Width, stiffeners)*10**6, "mm^2")
print(cp.NewCalc_Area([0,0,0,8], P_thickness, P_Width)*10**6, "mm^2")