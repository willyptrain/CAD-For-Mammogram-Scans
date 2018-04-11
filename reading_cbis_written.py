#get pathology for cbis-mammogram scans

class Case:
	def __init__(self,case_num, pathology):
		self.case_num = case_num
		self.pathology = pathology

#CALCIFICATIONS
f = open('MamImages/Images/calc_case_description_test_set.csv')
calc_case_info = []
calc_cases = []
for line in f:
	calc_case_info.append(line.split(","))

for i in range(0, len(calc_case_info)):
	case = calc_case_info[i][len(calc_case_info[i])-1]
	temp_case = case.split("/")[0]+"/"+case.split("/")[len(case.split("/"))-1]
	temp_path = case[len(case)-6]
	if(temp_case[0] == '"'):
		temp_case = temp_case[1:]
	calc_cases.append(Case(temp_case,temp_path))
	
mass_case_info = []
mass_cases = []
f = open('MamImages/Images/mass_case_description_test_set.csv')
for line in f:
	if(line.split(",") != ['"\r\n']):
		mass_case_info.append(line.split(","))
	
for i in range(0, len(mass_case_info)):
	case = mass_case_info[i][len(mass_case_info[i])-1]
	temp_case = case.split("/")[0]+"/"+case.split("/")[len(case.split("/"))-1]
	temp_path = case[len(case)-6]
	if(temp_case[0] == '"'):
		temp_case = temp_case[1:]
	mass_cases.append(Case(temp_case,temp_path))

print(len(calc_cases))
print(len(mass_cases))

#000001.dcm have longer description for their calc case info as opposed to 000000.dcm
class Case:
	def __init__(self,case_num, pathology):
		self.case_num = case_num
		self.pathology = pathology


