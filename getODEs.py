import sys
import re

"""
Parse parameter from line containing '# fixed'
"""
def getParameter(line):
	id = re.search('\((.*)\)', line).group(1)				# searching for '(<num>)' where num is my id
	name = line.split(", ")[1]								# splits by ', ' and takes 2nd part of it
	return (id, name)

"""
Parse assignment from line containing '# assignment'
"""
def getAssignment(line):
	id = re.search('= x\((.*)\) = ', line).group(1)			# searching for '= x(<num>) = ' where num is my id
	pre = line.split(" = ")[2].split(";")					# splits by ' = ' and then splits 3rd part of it by ';'
	equation = pre[0]
	name = pre[1].split(", ")[1].split("  ")[0]				# splits by ', ' and then splits 2nd part of it by '  '
	return [id, name, equation]

"""
Parse ODE from line containing '# reaction'
"""
def getODE(line):
	id = re.search('t\((.*)\) =', line).group(1)			# searching for 't(<num>) =' where num is my id
	pre = line.split(" ; ")									# splits by ' ; '
	name = pre[1].split(", ")[1]							# splits by ', ' and takes 2nd part of it
	equation = pre[0].replace("xdot(" + id + ")", name)		# replaces 'xdot(<num>)' with appropriate entity name
	return (id, name), ' '.join(equation.split())			# removes redundant whitespaces

"""
Replace parameters in assignments
"""
def impoveAssignments(assignments, parameters):
	return map(lambda assignment: assignment[:-1] + [replaceParameters(assignment[2], parameters)], assignments)

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
	return map(lambda ODE: replaceParameters(ODE, parameters), ODEs)

"""
Print output
"""
def nicePrint(ODEs, assignments):
	print "Ordinary differential equations:" + "\n" + "_" * 80 + "\n"
	for ODE in ODEs:
		print ODE + "\n"
	print "\n" + "_" * 80
	print "Associated assignments:" + "\n"
	for assignment in assignments:
		print assignment[1] + " = " + assignment[2]

##############################################################################
# the body of the script follows:

input_file = sys.argv[-1]
file = open(input_file, "r")

parameters, assignments, ODEs = [], [], []

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
		parameters.append(entity)
		ODEs.append(ODE)

parameters += map(lambda assignment: (assignment[0], assignment[1]), assignments)
ODEs = replaceODEs(ODEs, parameters)
nicePrint(ODEs, impoveAssignments(assignments, parameters))