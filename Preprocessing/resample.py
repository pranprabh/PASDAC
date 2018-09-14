import numpy as np
import pandas as pd

def resample_sesnor(data,start,end,newSamplingRate):
	newX = np.arange(start,end,1000/newSamplingRate)
	merged = np.append(data.index.values,newX)
	merged.sort()
	merged = np.unique(merged)
	data = data.reindex(merged)
	data = data.interpolate()
	data = data.reindex(newX)
	return data
