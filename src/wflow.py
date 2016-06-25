import os, subprocess, math
import numpy as np
import pandas
import spotpy
from sklearn import metrics

class spot_setup(object):
    """
    Calibration general methods for
    uncertainty analysis in WFLOW hydrologic model
    Default folders/filenames: observations.xlsx, single, wflow_0
    """
    
    def __init__(self):
        
        self.default_wflow_name = "wflow_0"
 	"""
	Parameter setted random.
	"""
        self.params = [
            spotpy.parameter.Uniform('N',0.03, 0.09), #1
            spotpy.parameter.Uniform('NRiver',0.02, 0.06),
            spotpy.parameter.Uniform('BetaSeePage_0',0.71, 1.95), #5
            spotpy.parameter.Uniform('BetaSeePage_1',0.71, 1.95),                    
            spotpy.parameter.Uniform('BetaSeePage_2',0.71, 1.95),                                
            spotpy.parameter.Uniform('BetaSeePage_3',0.71, 1.95),                                
            spotpy.parameter.Uniform('BetaSeePage_4',0.71, 1.95),                                
            spotpy.parameter.Uniform('Cflux_0',0.0005,1.639),            
            spotpy.parameter.Uniform('Cflux_1',0.0005,1.639),            
            spotpy.parameter.Uniform('Cflux_2',0.0005,1.639),            
            spotpy.parameter.Uniform('Cflux_3',0.0005,1.639),            
            spotpy.parameter.Uniform('Cflux_4',0.0005,1.639),                        
            spotpy.parameter.Uniform('K0_0',0.002,0.149),
            spotpy.parameter.Uniform('K0_1',0.002,0.149),
            spotpy.parameter.Uniform('K0_2',0.002,0.149),
            spotpy.parameter.Uniform('K0_3',0.002,0.149),
            spotpy.parameter.Uniform('K0_4',0.002,0.149),
            spotpy.parameter.Uniform('K4_0',0.0005, 0.051),
            spotpy.parameter.Uniform('K4_1',0.0005, 0.051),
            spotpy.parameter.Uniform('K4_2',0.0005, 0.051),
            spotpy.parameter.Uniform('K4_3',0.0005, 0.051),
            spotpy.parameter.Uniform('K4_4',0.0005, 0.051),            
            spotpy.parameter.Uniform('KQuickFlow_0',0.001, 0.060),            
            spotpy.parameter.Uniform('KQuickFlow_1',0.001, 0.060),                        
            spotpy.parameter.Uniform('KQuickFlow_2',0.001, 0.060),            
            spotpy.parameter.Uniform('KQuickFlow_3',0.001, 0.060),            
            spotpy.parameter.Uniform('KQuickFlow_4',0.001, 0.060),                        
            spotpy.parameter.Uniform('PERC_0',0.005,3.404),
            spotpy.parameter.Uniform('PERC_1',0.005,3.404),
            spotpy.parameter.Uniform('PERC_2',0.005,3.404),
            spotpy.parameter.Uniform('PERC_3',0.005,3.404),
            spotpy.parameter.Uniform('PERC_4',0.005,3.404),            
            spotpy.parameter.Uniform('SUZ_0',0.5,86.4),            
            spotpy.parameter.Uniform('SUZ_1',0.5,86.4),                        
            spotpy.parameter.Uniform('SUZ_2',0.5,86.4),            
            spotpy.parameter.Uniform('SUZ_3',0.5,86.4),            
            spotpy.parameter.Uniform('SUZ_4',0.5,86.4),            
            spotpy.parameter.Uniform('ICF_0',0.5,5.9),
            spotpy.parameter.Uniform('ICF_1',0.5,5.9),
            spotpy.parameter.Uniform('ICF_2',0.5,5.9),
            spotpy.parameter.Uniform('ICF_3',0.5,5.9),
            spotpy.parameter.Uniform('ICF_4',0.5,5.9),
            spotpy.parameter.Uniform('ICF_5',0.5,5.9),
            spotpy.parameter.Uniform('ICF_6',0.5,5.9),
            spotpy.parameter.Uniform('ICF_7',0.5,5.9),
            spotpy.parameter.Uniform('FC_0',30, 149),
            spotpy.parameter.Uniform('FC_1',30, 149),
            spotpy.parameter.Uniform('FC_2',30, 149),
            spotpy.parameter.Uniform('FC_3',30, 149),
            spotpy.parameter.Uniform('FC_4',30, 149),
            spotpy.parameter.Uniform('FC_5',30, 149),
            spotpy.parameter.Uniform('FC_6',30, 149),
            spotpy.parameter.Uniform('FC_7',30, 149),
            spotpy.parameter.Uniform('FC_8',30, 149),
            spotpy.parameter.Uniform('FC_9',30, 149),
            spotpy.parameter.Uniform('FC_10',30, 149),
            spotpy.parameter.Uniform('FC_11',30, 149),
            spotpy.parameter.Uniform('LP_0',0.17,1.18),
            spotpy.parameter.Uniform('LP_1',0.17,1.18),
            spotpy.parameter.Uniform('LP_2',0.17,1.18),
            spotpy.parameter.Uniform('LP_3',0.17,1.18),
            spotpy.parameter.Uniform('LP_4',0.17,1.18),
            spotpy.parameter.Uniform('LP_5',0.17,1.18),
            spotpy.parameter.Uniform('LP_6',0.17,1.18),
            spotpy.parameter.Uniform('LP_7',0.17,1.18),
            spotpy.parameter.Uniform('LP_8',0.17,1.18),
            spotpy.parameter.Uniform('LP_9',0.17,1.18),
            spotpy.parameter.Uniform('LP_10',0.17,1.18),
            spotpy.parameter.Uniform('LP_11',0.17,1.18),
            spotpy.parameter.Uniform('LP_12',0.17,1.18)
        ]
        
    def updateTablesWflow(self, vector):
	"""
	Random parameter setted before (init) need to be upload into static files in wflow's model
	"""
        self.params_ = vector
        self.tablas = {}        
        from collections import OrderedDict
        fns=OrderedDict()
        fns['N.tbl']=1
        fns['N_River.tbl']=1
        fns['BetaSeepage.tbl']=5
        fns['Cflux.tbl']=5
        fns['K0.tbl']=5
        fns['K4.tbl']=5
        fns['KQuickFlow.tbl']=5
        fns['PERC.tbl']=5
        fns['SUZ.tbl']=5      
        fns['ICF.tbl']=8            
        fns['FC.tbl']=12
        fns['LP.tbl']=13
        #numpara = [1,1,5,5,5,5,5,5,5,8,12,13]
        
        for fn in fns:
            #print fn
            path = "%s/CORMA_data/intbl/"%self.default_wflow_name
            filenamepath  = path + fn
            tabla = open(filenamepath,"r")
            self.tablas[fn] = tabla.readlines()
        
        aux=0
        for tabla in fns:
            filenamepath  = path + tabla
            text = self.tablas[tabla]
            for i in range(fns[tabla]):
                line = text[i].split("\t")
                line[-1]  = str(self.params_[aux])
                #print aux, i, tabla
                text[i] = "\t".join(line) + "\n"
                aux = aux + 1
            self.tablas[tabla] = text
            ntabla = open(filenamepath,"w")
            ntabla.writelines(text)
    
    def parameters(self):
        return spotpy.parameter.generate(self.params)
    
    def simulation(self, params):
	"""
	Run simulations of wflow model
	Return simulations series in a matrix-vector structure
	"""
        self.updateTablesWflow(params)
        p = subprocess.check_call(r'%s/%s/RunModelExecut.bat'%(os.path.abspath("."), self.default_wflow_name), shell=True)
        runTss = pandas.read_table("Wflow/%s/CORMA_data/run0001/run.tss"%self.default_wflow_name,
                                    skiprows=[i for i in range(35)], 
                                    #sep="|\s*", 
                                    #engine="python", 
                                    delim_whitespace=True,
                                    header=None)
        runTss.astype("float")
        return [runTss.values[:,i] for i in range(1, len(runTss.values[0,:]))]
        
    def evaluation(self):
	"""
	Method to read the observations input values
	Input: observations.xls (Own format)
	Return observation like matrix-vector structure.
	"""
        observations = pandas.read_excel("%s/observations.xlsx"%self.default_wflow_name, 
                                         sheetname=3, 
                                         skiprows=[0,1,2,3,4], 
                                         header = None
                                        )
        return [observations.values[:,i] for i in range(3, len(observations.values[0,:]))]
    
    def objectivefunction(self, ev, sim):
	"""
	Method calc objetive functions (Nash, V, AMI)
	"""
        ev, sim = self.clean_nan(ev, sim)
        objfunc = []
        for idx, e in enumerate(ev):
            objfunc.insert(idx, spotpy.objectivefunctions.nashsutcliff(ev[idx], sim[idx]))
        for idx, e in enumerate(ev):
            objfunc.insert(idx + 1 + len(objfunc), self.objectivefunctionRV(ev[idx], sim[idx]))
        for idx, e in enumerate(ev):
            objfunc.insert(idx + 2 + len(objfunc), metrics.adjusted_rand_score(ev[idx], sim[idx]))
        return objfunc

    def objectivefunctionRV(self,sim,eval):
        """
        Own method for calc objetive function Volumen Balance
        """
        vol_sim = [i*24*60*60 for i in sim]
        vol_eval = [i*24*60*60 for i in eval]
        s,e = np.array(vol_sim),np.array(vol_eval)
        return np.abs(np.sum(e - s))/np.sum(e)		

    def clean_nan(self, ev, sim):
        #Remove None a number types into a serie
        for idx, serie in enumerate(ev):
            v = pandas.Series(ev[idx], index=sim[idx])
            v = v.dropna()
            sim[idx] = v.index.values.tolist()
            ev[idx] = v.values.tolist()
        return ev, sim
    
    def single_simulation(self, params):
	"""
	Single simulations of wflow model
	Return single simulation series in a matrix-vector structure
	"""
        self.updateTablesWflow(params)
        p = subprocess.check_call(r'%s/Wflow/%s/RunModelExecut.bat'%(os.path.abspath("."), "single"), shell=True)
        runTss = pandas.read_table("Wflow/single/CORMA_data/run0001/run.tss",
                                    skiprows=[i for i in range(35)], 
                                    #sep="|\s*", 
                                    #engine="python", 
                                    delim_whitespace=True,
                                    header=None)
        runTss.astype("float")
        return [runTss.values[:,i] for i in range(1, len(runTss.values[0,:]))]

#run algorithm in parallel process
#sampler=spotpy.algorithms.mc(spot_setup(), dbname='wflow_calibration', dbformat='csv', parallel='mpi')
