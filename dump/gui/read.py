#base class for reading external files. 
#to be extended for for different file types

class Read(object):
	def __init__(self, _file):
		pass
		
	def readFile(self):
		pass
		
class segyRead(Read):
	def __init__(self, _file):
		pass
		
def read_traces(_file, ns, chunksize=0.01): 
	#assuming ibm floats for now
	#chunksize in Gb
	ibmtype = np.dtype(segy_trace_header_dtype.descr + [('data', ('<i4',ns))])
	ftype = np.dtype(segy_trace_header_dtype.descr + [('data', ('<f4',ns))])
	with open(_file, 'rb') as f:
		#some trickery to calculate filesize
		f.seek(0, os.SEEK_END)
		filesize = f.tell() #filesize in bytes
		#caculate size of traces
		tracesize = 240+ns*4.0
		ntraces = (filesize-3600)/tracesize
		
		chunks = min(filesize, np.floor(filesize/(chunksize*1.0e9)))
		tracesPerChunk = min(ntraces, np.floor(chunksize*1.0e9/tracesize))
		chunksize = tracesPerChunk*tracesize
		remainder = divmod(filesize-3600, chunksize)	
			f.seek(3600)    #start at end of binary header block
		for n in range(int(chunks+1)):
			if n ==int(chunks+1): chunksize = remainder #last chunk
			data = np.fromfile(f, dtype=ftype, count=int(chunksize))
			data['data'] = ibm2ieee(data['data'].astype(np.int32))
			yield data


if __name__== '__main__':
	test = segyRead("test")