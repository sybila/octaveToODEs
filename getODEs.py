import sys
import re

"""
Parse parameter from line containing '# fixed'
"""
def getParameter(line):
	id = re.search('\((.*)\)', line).group(1)
	name = line.split(", ")[1]
	return (id, name)

"""
Parse assignment from line containing '# assignment'
"""
def getAssignment(line):
	id = re.search('= x\((.*)\) = ', line).group(1)
	pre = line.split(" = ")[2].split(";")
	equation = pre[0]
	name = pre[1].split(", ")[1].split("  ")[0]
	return (id, name, equation)

"""
Parse ODE from line containing '# reaction'
"""
def getODE(line):
	id = re.search('t\((.*)\) =', line).group(1)
	pre = line.split(" ; ")
	name = pre[1].split(", ")[1]
	equation = pre[0].replace("xdot(" + id + ")", name)
	return (id, name), ' '.join(equation.split())

"""
Replace objects in assignments
"""
def impoveAssignments(assignments, parameters):
	new_assigmets = []
	for assignment in assignments:
		assignment = list(assignment)
		assignment[2] = replaceParameters(assignment[2], parameters)
		new_assigmets.append(tuple(assignment))
	return new_assigmets, parameters

"""
Replace all parameters in a given string
"""
def replaceParameters(value, parameters):
	for param in parameters:
		value = value.replace("x(" + param[0] + ")", param[1])
	return value

"""
Replace parameters in all ODEs
"""
def replaceODEs(ODEs, parameters):
	ODEs = map(lambda ODE: replaceParameters(ODE, parameters), ODEs)
	return ODEs

"""
Print output
"""
def nicePrint(ODEs, assignments):
	print "Ordinary differential equations:"
	print "_" * 100
	print 
	for ODE in ODEs:
		print ODE
		print 
	print "_" * 100
	print "Associated assignments:"
	print 
	for assignment in assignments:
		print assignment[1] + " = " + assignment[2]

##############################################################################
# the body of the script follows:

input_file = sys.argv[-1]
file = open(input_file, "r")

parameters, assignments, ODEs, entities = [], [], [], []

for line in file:
	if re.search("# default values", line):
		break
	line = line.rstrip().replace("\"", "")

	if re.search("# fixed", line):
		parameters.append(getParameter(line))
	if re.search("# assignment", line):
		assignments.append(getAssignment(line))
	if re.search("# reaction", line):
		entity, ODE = getODE(line)
		entities.append(entity)
		ODEs.append(ODE)

parameters += entities
parameters += map(lambda assignment: (assignment[0], assignment[1]), assignments)
assignments, parameters = impoveAssignments(assignments, parameters)
ODEs = replaceODEs(ODEs, parameters)
nicePrint(ODEs, assignments)