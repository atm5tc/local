import os
import numpy as np
import random

	
def gen_add_code(trigger_code,trigger, trigger_time, variable, stuck_value):
	if trigger_code:
		code = trigger_code
	else:
		code = 'if %s>=%s:'%(trigger,trigger_time)
	l = '//%s+=%s' % (variable,stuck_value)
	code = code + l
	return code


def gen_sub_code(trigger_code,trigger, trigger_time, variable, stuck_value,additional_code=''):
	if trigger_code:
		code = trigger_code
	else:
		code = 'if %s>=%s:'%(trigger,trigger_time)
	l = '//%s-=%s' % (variable,stuck_value)
	code = code + l
	return code + additional_code

	
def gen_stuck_code(trigger_code,trigger, trigger_time, variable, stuck_value):
	if trigger_code:
		code = trigger_code
	else:
		code = 'if %s>=%s:'%(trigger,trigger_time)
	l = '//%s=%s' % (variable,stuck_value)
	code = code + l
	return code
	
# def gen_intermittent_code(variable, trigger, trigger_prob, random_value):
# 	#code = 'fault_prob = random.randint(1,100)'
# 	code = 'if %s<=%s:'%(trigger,trigger_prob)
# 	l = '//%s=%s' % (variable,random_value)
# 	code = code + l
# 	return code
	
### Write codes to fault library file
def write_to_file(code, exp_name, target_file, faultLoc):
	if os.path.isdir('fault_library') != True:
		os.makedirs('fault_library')
	fileName = 'fault_library/scenario_'+str(sceneNum)
	out_file = fileName+'.txt'
	#param_file = fileName+'_params.csv'

	with open(out_file, 'w') as outfile:
		#print out_file
		outfile.write('title:' + exp_name + '\n')
		outfile.write('location//' + target_file+ '//'+faultLoc + '\n')
		for i, line in enumerate(code):
			outfile.write('fault ' + str(i+1) + '//' + line + '\n')
		outfile.write('Total number of fault cases: '+str(i+1))

	with open('run_fault_inject_campaign.sh', 'a+') as runFile:
		runFile.write('python run_openAPS.py '+fileName+'\n')

############################################################################

def write_to_file_STPA(code, exp_name, target_file, faultLoc):
	if os.path.isdir('fault_library_STPA') != True:
		os.makedirs('fault_library_STPA')
	fileName = 'fault_library_STPA/scenario_'+str(sceneNum)
	out_file = fileName+'.txt'
	#param_file = fileName+'_params.csv'

	with open(out_file, 'w') as outfile:
		#print out_file
		outfile.write('title:' + exp_name + '\n')
		outfile.write('location//' + target_file+ '//'+faultLoc + '\n')
		for i, line in enumerate(code):
			outfile.write('fault ' + str(i+1) + '//' + line + '\n')
		outfile.write('Total number of fault cases: '+str(i+1))

	with open('run_fault_inject_STPA_campaign.sh', 'a+') as runFile:
		runFile.write('python run_openAPS.py '+fileName+'\n')


		

def gen_belowTarget_noinc_add_rate(sceneNum):
	title = str(sceneNum)+'_belowTarget_noinc_add_rate'
	#faultLibFile = 'fault_library/dRelPlantRad'
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#rate:HOOK#'
	trigger = '_'
	# trigger_time = 10 # 10 is an arbitrary number, I want the fault be injected after 10th iteration
	trigger_code = 'if glucose < bg_target:'
	code = []
	code_STPA=[]
	#param = []
	variable = 'loaded_suggested_data["rate"]'
	deltaRange = np.arange(10,350,10)
	for i in deltaRange:
		# for j in range(10):
		delta = random.randint(i,i+9)
		trigger_time = random.randint(10,200)
		#code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], '//if '+variable[0]+'>=255:'+'//  '+variable[0]+'= 254'))
		code.append(gen_add_code('',trigger, trigger_time, variable, delta/100.0))
		code_STPA.append(gen_add_code(trigger_code,trigger, trigger_time, variable, delta/100.0))
		#param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

	write_to_file(code, title, fileLoc, faultLoc)
	write_to_file_STPA(code_STPA, title, fileLoc, faultLoc)

def gen_belowTarget_inc_stuck_rate(sceneNum):
	title = str(sceneNum)+'_belowTarget_inc_stuck_rate'
	#faultLibFile = 'fault_library/dRelPlantRad'
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#rate:HOOK#'
	trigger = '_'
	# trigger_time = 10 # 10 is an arbitrary number, I want the fault be injected after 10th iteration
	trigger_code = 'if glucose < bg_target:'
	code = []
	code_STPA=[]
	#param = []
	variable = 'loaded_suggested_data["rate"]'
	deltaRange = np.arange(100,350,10)
	for i in deltaRange:
		delta = random.randint(i,i+9)
		trigger_time = random.randint(10,200)
		#code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], '//if '+variable[0]+'>=255:'+'//  '+variable[0]+'= 254'))
		code.append(gen_stuck_code('',trigger, trigger_time, variable, delta/100.0))
		code_STPA.append(gen_stuck_code(trigger_code,trigger, trigger_time, variable, delta/100.0))
		#param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

	write_to_file(code, title, fileLoc, faultLoc)
	write_to_file_STPA(code_STPA, title, fileLoc, faultLoc)

def gen_aboveTarget_nodec_sub_rate(sceneNum):
	title = str(sceneNum)+'_aboveTarget_nodec_sub_rate'
	#faultLibFile = 'fault_library/dRelPlantRad'
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#rate:HOOK#'
	trigger = '_'
	# trigger_time = 10 # 10 is an arbitrary number, I want the fault be injected after 10th iteration
	trigger_code = 'if glucose > bg_target:'
	code = []
	code_STPA=[]
	#param = []
	variable = 'loaded_suggested_data["rate"]'
	deltaRange = np.arange(10,350,10)
	for i in deltaRange:
		# for j in range(10):
		delta = random.randint(i,i+9)
		trigger_time = random.randint(10,200)
		#code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], '//if '+variable[0]+'>=255:'+'//  '+variable[0]+'= 254'))
		code.append(gen_sub_code('',trigger, trigger_time, variable, delta/100.0,'//if '+variable+'<0:'+'//  '+variable+'= 0'))
		code_STPA.append(gen_sub_code(trigger_code,trigger, trigger_time, variable, delta/100.0,'//if '+variable+'<0:'+'//  '+variable+'= 0'))
		#param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

	write_to_file(code, title, fileLoc, faultLoc)
	write_to_file_STPA(code_STPA, title, fileLoc, faultLoc)

def gen_aboveTarget_nodec_stuck_rate(sceneNum):
	title = str(sceneNum)+'_aboveTarget_nodec_stuck_rate'
	#faultLibFile = 'fault_library/dRelPlantRad'
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#rate:HOOK#'
	trigger = '_'
	# trigger_time = 10 # 10 is an arbitrary number, I want the fault be injected after 10th iteration
	trigger_code = 'if glucose > bg_target:'
	code = []
	code_STPA=[]
	#param = []
	variable = 'loaded_suggested_data["rate"]'
	deltaRange = np.arange(0,200,10)
	for i in deltaRange:
		delta = random.randint(i,i+9)
		trigger_time = random.randint(10,200)
		#code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], '//if '+variable[0]+'>=255:'+'//  '+variable[0]+'= 254'))
		code.append(gen_stuck_code('',trigger, trigger_time, variable, delta/1000.0))
		code_STPA.append(gen_stuck_code(trigger_code,trigger, trigger_time, variable, delta/1000.0))
		#param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

	write_to_file(code, title, fileLoc, faultLoc)
	write_to_file_STPA(code_STPA, title, fileLoc, faultLoc)

###############glucose:HOOK#############
def gen_belowTarget_add_glucose(sceneNum):
	title = str(sceneNum)+'_belowTarget_add_glucose'
	#faultLibFile = 'fault_library/dRelPlantRad'
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#glucose:HOOK#'
	trigger = '_'
	# trigger_time = 10 # 10 is an arbitrary number, I want the fault be injected after 10th iteration
	trigger_code = 'if loaded_glucose < 110:'
	code = []
	code_STPA=[]
	#param = []
	variable = 'data_to_prepend["glucose"]'
	deltaRange = np.arange(10,350,10)
	for i in deltaRange:
		# for j in range(10):
		delta = random.randint(i,i+9)
		trigger_time = random.randint(10,200)
		#code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], '//if '+variable[0]+'>=255:'+'//  '+variable[0]+'= 254'))
		code.append(gen_add_code('',trigger, trigger_time, variable, delta))
		code_STPA.append(gen_add_code(trigger_code,trigger, trigger_time, variable, delta))
		#param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

	write_to_file(code, title, fileLoc, faultLoc)
	write_to_file_STPA(code_STPA, title, fileLoc, faultLoc)

def gen_belowTarget_stuck_glucose(sceneNum):
	title = str(sceneNum)+'_belowTarget_stuck_glucose'
	#faultLibFile = 'fault_library/dRelPlantRad'
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#glucose:HOOK#'
	trigger = '_'
	# trigger_time = 10 # 10 is an arbitrary number, I want the fault be injected after 10th iteration
	trigger_code = 'if loaded_glucose < 110:'
	code = []
	code_STPA=[]
	#param = []
	variable = 'data_to_prepend["glucose"]'
	deltaRange = np.arange(120,350,10)
	for i in deltaRange:
		delta = random.randint(i,i+9)
		trigger_time = random.randint(10,200)
		#code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], '//if '+variable[0]+'>=255:'+'//  '+variable[0]+'= 254'))
		code.append(gen_stuck_code('',trigger, trigger_time, variable, delta))
		code_STPA.append(gen_stuck_code(trigger_code,trigger, trigger_time, variable, delta))
		#param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

	write_to_file(code, title, fileLoc, faultLoc)
	write_to_file_STPA(code_STPA, title, fileLoc, faultLoc)

def gen_aboveTarget_sub_glucose(sceneNum):
	title = str(sceneNum)+'_aboveTarget_sub_glucose'
	#faultLibFile = 'fault_library/dRelPlantRad'
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#glucose:HOOK#'
	trigger = '_'
	# trigger_time = 10 # 10 is an arbitrary number, I want the fault be injected after 10th iteration
	trigger_code = 'if loaded_glucose > 120:'
	code = []
	code_STPA=[]
	#param = []
	variable = 'data_to_prepend["glucose"]'
	deltaRange = np.arange(10,350,10)
	for i in deltaRange:
		# for j in range(10):
		delta = random.randint(i,i+9)
		trigger_time = random.randint(10,200)
		#code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], '//if '+variable[0]+'>=255:'+'//  '+variable[0]+'= 254'))
		code.append(gen_sub_code('',trigger, trigger_time, variable, delta,'//if '+variable+'<0:'+'//  '+variable+'= 0'))
		code_STPA.append(gen_sub_code(trigger_code,trigger, trigger_time, variable, delta,'//if '+variable+'<0:'+'//  '+variable+'= 0'))
		#param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

	write_to_file(code, title, fileLoc, faultLoc)
	write_to_file_STPA(code_STPA, title, fileLoc, faultLoc)

def gen_aboveTarget_stuck_glucose(sceneNum):
	title = str(sceneNum)+'_aboveTarget_stuck_glucose'
	#faultLibFile = 'fault_library/dRelPlantRad'
	fileLoc = 'updated_ct_script_iob_based.py'
	faultLoc = '#glucose:HOOK#'
	trigger = '_'
	# trigger_time = 10 # 10 is an arbitrary number, I want the fault be injected after 10th iteration
	trigger_code = 'if loaded_glucose > 120:'
	code = []
	code_STPA=[]
	#param = []
	variable = 'data_to_prepend["glucose"]'
	deltaRange = np.arange(30,70,10)
	for i in deltaRange:
		delta = random.randint(i,i+9)
		trigger_time = random.randint(10,200)
		#code.append(gen_add_code(trigger_code, trigger, t1, t2, variable, [delta], '//if '+variable[0]+'>=255:'+'//  '+variable[0]+'= 254'))
		code.append(gen_stuck_code('',trigger, trigger_time, variable, delta))
		code_STPA.append(gen_stuck_code(trigger_code,trigger, trigger_time, variable, delta))
		#param.append(','.join(['relative distance',str(t1),str(dt),str(delta)]))

	write_to_file(code, title, fileLoc, faultLoc)
	write_to_file_STPA(code_STPA, title, fileLoc, faultLoc)

###_main_###

with open('run_fault_inject_campaign.sh', 'w') as runFile:
    runFile.write('#Usage: python run_openAPS.py fault_library\n')

with open('run_fault_inject_STPA_campaign.sh', 'w') as runFile:
    runFile.write('#Usage: python run_openAPS.py target_fault_library\n')
	
scenarios = {
1 : gen_belowTarget_noinc_add_rate,
2 : gen_belowTarget_inc_stuck_rate,
3 : gen_aboveTarget_nodec_sub_rate,
4 : gen_aboveTarget_nodec_stuck_rate,
5 : gen_belowTarget_add_glucose,
6 : gen_belowTarget_stuck_glucose,
7 : gen_aboveTarget_sub_glucose,
8 : gen_aboveTarget_stuck_glucose,
}

for sceneNum in [1,2,3,4,5,6,7,8]:
	scenarios[sceneNum](sceneNum)

