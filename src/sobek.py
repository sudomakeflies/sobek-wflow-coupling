import os, subprocess, math, re
import numpy as np
import pandas
import spotpy
from sklearn import metrics

class spot_setup(object):
	"""Calibration general methods for uncertainty analysis in SOBEK hydraulics model"""

	def __init__(self):
		#Cp (mt-cp) friction as a constant in bed-file friction layer for more info please view Sobek 2.4 documentation pag. 757
		self.params = [
			spotpy.parameter.Uniform('cp',0.03, 0.06)
		]

	def parameters(self):
		#Spotpy random generate methods
		return spotpy.parameter.generate(self.params)

	def updateParams(self, vector):
		self.params_ = vector
		os.chdir('C:\Sobek213\MagSect1.lit')
		tabla = open("FRICTION.DAT","r")
		lines = tabla.readlines()
		tabla.close()
		#old regex "cp\s0\s\d\.\d{2}"
		regex = re.compile(r"cp\s0\s*\d{1,3}?\.*\d{1,3}", re.IGNORECASE)
		for i, line in enumerate(lines):
			if re.search("BDFR", line):
				line = regex.sub("cp 0 %s" % self.params_[0], line)
				lines[i] = line
		tabla = open("FRICTION.DAT","w")
		tabla.writelines(lines)
		tabla.close()

	def simulation(self, params):
		self.updateParams(params)
		os.chdir("C:\Sobek213\MagSect1.lit\CMTWORK")
		p = subprocess.check_call(r"call C:\Sobek214\PROGRAMS\simulate.exe simulate.ini", shell=True)
		os.chdir('C:\Sobek213\PROGRAMS\ODS_VIEW')
		p = subprocess.check_call(r"ODS_View.exe C:\Sobek214\MagSect2.lit\4\REACHSEG.HIS /CONVERT:output.csv", shell=True)
		csv = pandas.read_csv("output.csv")
		return [csv.values[:,i] for i in range(1, len(csv.values[0,:]))]

	def evaluation(self):
		observations = pandas.read_excel("calibracion/observations.xlsx",
										 sheetname=3,
										 skiprows=[0,1,2,3,4],
										 header = None
										)
		return [observations.values[:,i] for i in range(3, len(observations.values[0,:]))]

	def objectivefunctionNASH(self,sim,eval):
		return spotpy.objectivefunctions.nashsutcliff(eval, sim)

	def objectivefunctionRV(self,sim,eval):
		vol_sim = [i*24*60*60 for i in sim]
		vol_eval = [i*24*60*60 for i in eval]
		s,e = np.array(vol_sim),np.array(vol_eval)
		return np.abs(np.sum(e - s))/np.sum(e)
		#return spotpy.objectivefunctions.nashsutcliff(eval, sim)

	def clean_nan(self, ev, sim):
		for idx, serie in enumerate(ev):
			v = pandas.Series(ev[idx], index=sim[idx])
			v = v.dropna()
			sim[idx] = v.index.values.tolist()
			ev[idx] = v.values.tolist()
		return ev, sim

	def objectivefunction(self, ev, sim):
		ev, sim = self.clean_nan(ev, sim)
		objfunc = []
		for idx, e in enumerate(ev):
			objfunc.insert(idx, spotpy.objectivefunctions.nashsutcliff(ev[idx], sim[idx]))
		for idx, e in enumerate(ev):
			objfunc.insert(idx + 1 + len(objfunc), self.objectivefunctionRV(ev[idx], sim[idx]))
		return objfunc

#run algorithm in parallel process
#sampler=spotpy.algorithms.mc(spot_setup(), dbname='sobek_calibration', dbformat='csv', parallel='mpi')