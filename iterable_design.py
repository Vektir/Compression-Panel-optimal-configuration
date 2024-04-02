import Compression_Panel as cp
import iteratorrrr
import numpy as np
from scipy.optimize import fsolve
import pandas as pd


# import Compression_Panel as cp
# import numpy as np
# from scipy.optimize import fsolve

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
P_thicknessesssssss=[1e-3,.8e-3]

#stiffeners
possible_stiffeners = iteratorrrr.getstuff()
possible_stiffeners2 = []
for stiffeners in possible_stiffeners:
	b=[]
	for i in stiffeners:
		b.append(cp.stiffener(i))
	possible_stiffeners2.append(b)

viable_designs=[]
viabledesigns2_but_not_df=[]
viable_design2={"stiffeners":[], "plate thickness":[],  "area":[], "load":[],"plate safety_factor":[] }

for P_thickness in P_thicknessesssssss:
	print("waaa")
	for stiffeners in possible_stiffeners2:
		load = Force / cp.Calc_Area(P_thickness, P_Width, stiffeners)

		free_min_len = cp.minimum_plane_length(P_thickness, K_free, E, load)
		hinged_min_len = cp.minimum_plane_length(P_thickness, K_hinged, E, load)
		
		if P_Width > 2*free_min_len + (len(stiffeners)-1)*hinged_min_len:
			continue
		
		free_l, hinged_l = fsolve(cp.find_optimal_plane_lengths,(free_min_len, hinged_min_len), args=(stiffeners, K_free, K_hinged))
		crit_load_thin_sheet = cp.sigmacrit(P_thickness,free_l,K_free, E)

		safety_factor = crit_load_thin_sheet/load

		area=cp.Calc_Area(P_thickness, P_Width, stiffeners)
		
		


		if safety_factor > 1.2:
			#print(area * 10**6, "mm^2", safety_factor, "safety factor")
			#print([i.type for i in stiffeners])
			
			#viable_design2["stiffeners"].append([i.type for i in stiffeners])
			#viable_design2["plate thickness"].append(P_thickness)
			#viable_design2["area"].append(area)
			#viable_design2["load"].append(load)
			#viable_design2["plate safety_factor"].append(safety_factor)

			viabledesigns2_but_not_df.append([ [i.type for i in stiffeners], P_thickness*10**3, area *(10**6),load / 10**6, safety_factor])

			viable_designs.append([area *10**6, [i.type for i in stiffeners], safety_factor, P_thickness*10**3])
		if safety_factor >1.7 and safety_factor <1.8 :
			print(free_l, hinged_l)

sorteddesigns=sorted(viable_designs, key=lambda x: x[0])
print(sorteddesigns[:10])


viable_design2= pd.DataFrame(viabledesigns2_but_not_df, columns = ["stiffeners", "plate thickness (mm)", "area (mm^2)", "load (MPa)", "plate safety factor"]) 

viable_design2= viable_design2.sort_values(by="area (mm^2)")
viable_design2.to_csv("viable_designs.csv")
#print(viable_design2[:10])

# for i in sorteddesigns:
# 	if len(i[1])==6:
# 		print(i)