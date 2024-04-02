import numpy as np

def NewCalc_Area(stiff_by_type, P_thickness, P_Width):
	A_tot = P_Width * P_thickness
	stiff_type_counter=1
	for i in stiff_by_type:
		if stiff_type_counter == 1:
			A_tot +=  (.0015 * .02 * 2 - .0015**2)*i
		if stiff_type_counter == 2:
			A_tot +=  (.002 * .02 * 2 - .002**2)*i
		if stiff_type_counter == 3:
			A_tot +=  (.002 * .015 * 2 - .002**2)*i
		if stiff_type_counter == 4:
			A_tot +=  (.0015 * .015 * 2 - .0015**2)*i
		stiff_type_counter+=1
	return A_tot

def Newcalc_y_mid(stiff_by_type, P_thickness, P_Width):
	Q_tot = 0
	Q_tot += (P_Width*P_thickness) *(P_thickness/2)
	stiff_type_counter=1
	for i in stiff_by_type:
		for j in range(i):
			if stiff_type_counter == 1:
				Q_tot += -(.0015 * .02) * (.0015/2)
			if stiff_type_counter == 2:
				Q_tot += -(.002 * .02) * (.002/2)
			if stiff_type_counter == 3:
				Q_tot += -(.002 * .015) * (.002/2)
			if stiff_type_counter == 4:
				Q_tot += -(.0015 * .015) * (.0015/2)
		stiff_type_counter+=1
	return Q_tot/NewCalc_Area(stiff_by_type, P_thickness, P_Width)

def Newcalc_I2(stiff_by_type, P_thickness, P_Width, y_mid):
	I2 = 0
	I2 += (P_Width * P_thickness**3 / 12) + (P_thickness * P_Width) * (abs(y_mid - P_thickness/2))**2
	stiff_type_counter=1
	for i in stiff_by_type:
		for j in range(i):
			if stiff_type_counter == 1:
				I2 += .02 * .0015**3 / 12 + .02 * .0015 * (abs(-.0015/2-y_mid))**2
			if stiff_type_counter == 2:
				I2 += .02 * .002**3 / 12 + .02 * .002 * (abs(-.002/2-y_mid))**2
			if stiff_type_counter == 3:
				I2 += .015 * .002**3 / 12 + .015 * .002 * (abs(-.002/2-y_mid))**2
			if stiff_type_counter == 4:
				I2 += .015 * .0015**3 / 12 + .015 * .0015 * (abs(-.0015/2-y_mid))**2
		stiff_type_counter+=1
	return I2

class stiffener:
	type = 0
	length = 0
	thickness = 0
	def __init__(self, type):
		if type == 1:
			self.length = .02
			self.thickness = .0015
		if type == 2:
			self.length = .02
			self.thickness = .002
		if type == 3:
			self.length = .015
			self.thickness = .002
		if type == 4:
			self.length = 15e-3
			self.thickness = .0015
		self.type = type


def Calc_Area(P_thickness, P_Width, stiffeners):
	A_tot = P_Width * P_thickness
	for i in stiffeners:
		A_tot +=  (i.thickness * i.length)
		A_tot +=  (i.thickness * (i.length - i.thickness))
	return A_tot

def calc_y_mid(P_thickness, P_Width, stiffeners):
	Q_tot = 0
	Q_tot += (P_Width*P_thickness) *(P_thickness/2)
	A_tot = P_Width * P_thickness

	for i in stiffeners:
		Q_tot += -(i.thickness * i.length) * (i.thickness/2)
		A_tot +=  (i.thickness * i.length)

		Q_tot += -(i.thickness * (i.length - i.thickness)) * (i.thickness + (i.length-i.thickness)/2)
		A_tot +=  (i.thickness * (i.length - i.thickness))

	return Q_tot/A_tot


def calc_I2(P_thickness, P_Width, stiffeners, y_mid):
	I2 = 0
	I2 += (P_Width * P_thickness**3 / 12) + (P_thickness * P_Width) * (abs(y_mid - P_thickness/2))**2
	for i in stiffeners:
		I2 += i.length * i.thickness**3 / 12 + i.length * i.thickness * (abs(-i.thickness/2-y_mid))**2
		I2 += i.thickness * (i.length - i.thickness)**3 / 12 + i.thickness * (i.length - i.thickness) * (abs(-i.thickness -(i.length-i.thickness)/2 - y_mid))**2
		##print(y_mid, -i.thickness, -i.thickness -(i.length-i.thickness)/2)
		##print(-i.thickness/2-y_mid, -i.thickness -(i.length-i.thickness)/2 -y_mid)
	return I2


def sigmacrit(P_thickness, plane_width, K, E):
	sigma_crit = K * E *(P_thickness/plane_width)**2
	return sigma_crit

def minimum_plane_length(P_thickness, K, E, sigma_required):
	len = np.sqrt(K*E/sigma_required) * P_thickness
	return len

def min_rivet_spacing(P_thickness, E, sigma):
	return np.sqrt(.9*2.1*E / sigma) * P_thickness

def stiffen_stiffeners(stiffeners):
	a=[]
	for i in stiffeners:
		a.append(stiffener(i))
	return a

def find_optimal_plane_lengths(p, stiffenerss, K_free, K_hinged):
	K_free = .477
	K_hinged = 3.536
	free_l, hinged_l = p
	return 2*free_l + (len(stiffenerss)-1)*hinged_l - P_Width, K_free/(free_l**2) - K_hinged/(hinged_l**2)

def calc_beam_bending_max_force(P_length, E, I2):
	c=4
	return (c*np.pi**2*E*I2)/(P_length**2)


stiffeners = []

### INPUTS ###
F_dis = 100_000 #N
P_thickness = 0.001 #m ###########################################
P_Width = .400 #m	
P_length = .435 #m
E = 71700 * 10**6 #Pa

K_free = .477
K_hinged = 3.536


Force = F_dis * P_Width


### define stiffeners
# stiffeners.append(stiffener(1))
# stiffeners.append(stiffener(1))
# stiffeners.append(stiffener(1))
# stiffeners.append(stiffener(1))
# stiffeners.append(stiffener(1))
# stiffeners.append(stiffener(1))
# stiffeners.append(stiffener(1))
# stiffeners.append(stiffener(1))

###

load = Force / Calc_Area(P_thickness, P_Width, stiffeners)

#print("load: ", load * 10**-6, "MPa")
free_min_len = minimum_plane_length(P_thickness, K_free, E, load)
hinged_min_len = minimum_plane_length(P_thickness, K_hinged, E, load)

#print("free min length: ", free_min_len*10**3, "mm")
#print("hinged min length: ", hinged_min_len*10**3, "mm")
#print("Area", Calc_Area(P_thickness, P_Width, stiffeners)*10**6, "mm^2")
#print(2*free_min_len + (len(stiffeners)-1)*hinged_min_len)
#print(P_Width < 2*free_min_len + (len(stiffeners)-1)*hinged_min_len)


rivet_space = min_rivet_spacing(P_thickness, E, load)
num_rivet_per_stiff = np.ceil(P_length / rivet_space) - 1
#print("rivet space: ", rivet_space*10**3, "mm", "num rivets per stiffener: ", num_rivet_per_stiff)
#print("total num of rivets:", num_rivet_per_stiff * len(stiffeners))


temp = sigmacrit(P_thickness, 20*10**-3, K_free , E)
##print("free panel: ", temp * 10**-6, "MPa")
temp_2 = sigmacrit(P_thickness, 60*10**-3, K_hinged , E)
##print("hinged panel:", temp_2 * 10**-6, "MPa")



y_mid = calc_y_mid(P_thickness, P_Width, stiffeners)
I2 = calc_I2(P_thickness, P_Width, stiffeners, y_mid)



##print(y_mid*10**3)
##print("second moment of area: ", I2*10**12, "mm^4")
## edge distance < 72.5 mm (desmos graph)

### coefficient >6
