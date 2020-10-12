import random, sys, math, multiprocessing, lzma, hashlib, glob
from multiprocessing.dummy import Pool as ThreadPool
CpuCoreCount = multiprocessing.cpu_count()

def pack(byte): 
	return int(byte, 2)
def unpack(bits):
	dat = str(bin(bits)).split("b")[1]
	dat = ((8-len(dat))*"0")+dat
	return dat
 
def fromfile(byte): 
	bytelen = len(byte)
	if runthreaded:
		with ThreadPool(CpuCoreCount) as pool:
			byte = "".join(pool.map(unpack, byte))
	else:
		bits = ""
		rate = math.ceil(len(byte)/1001)
		for index, i in enumerate(byte):
			dat = str(bin(i)).split("b")[1]
			dat = ((8-len(dat))*"0")+dat
			bits+=dat
		byte = bits			 
	return byte

def tofile(outputData): 
	outputData = [outputData[i*8:i*8+8] for i in range(int(len(outputData)/8))]
	if runthreaded:
		with ThreadPool(CpuCoreCount) as pool:
			outputData = bytes(pool.map(pack, outputData))
	else:
		byte = []
		rate = math.ceil(len(outputData)/1001)
		for index, i in enumerate(outputData):
			byte.append(int(i, 2))
		outputData = bytes(byte)
	return outputData

def runskip(indata,key,gatepos): 
	data = indata
	if gatepos:
		#gate true
		gate = 0
	else:
		gate = 1
	le = len(data)
	for i in range(gate,len(data),2):
		if not(i+key >= le):
			data[i+key], data[i] = data[i], data[i+key]
	return data

def unskip(indata, key, gatepos): 
	data = indata
	if gatepos:
		# gate true
		if ((len(indata)-key)%2 == 1):
			gate = 0
		else:
			gate = 1		
	else:
		if ((len(indata)-key)%2 == 0):
			gate = 0
		else:
			gate = 1
	le = len(data)
	data = data[::-1]
	for i in range(gate,len(data),2):
		if not(i+key >= le):
			data[(i+key)], data[i] = data[i], data[(i+key)]				 
	data = data[::-1]
	return data

def offsetter(data): 
	return (eprintdct[data])
	
def unoffsetter(data): 
	return (dprintdct[data])

def runoffset(data,key1,key2,key3):
	global eprintdct
	data = [data[i:i+8] for i in range(0,len(data),8)]
	printls = [] 
	for i in range(256):
		loop = str(bin(i)).split("b")[1]
		printls.append(((8-len(loop))*"0")+loop)
	printls = runskip(printls, key1, True)
	printls = runskip(printls, key2, False)
	eprintdct = {}
	for i in printls:
		tmpkey = key3
		while printls.index(i)+tmpkey >= len(printls):
			tmpkey -= len(printls)
		eprintdct[i] = printls[printls.index(i)+tmpkey]
	if runthreaded:
		with ThreadPool(CpuCoreCount) as pool:
			data = "".join(pool.map(offsetter, data))
	else:
		out = []
		for index, i in enumerate(data):
			out.append(offsetter(i))
		data = "".join(out)
	return data

def rundeoffset(data,key1,key2,key3):
	global dprintdct
	printls = [] 
	for i in range(256):
		loop = str(bin(i)).split("b")[1]
		printls.append(((8-len(loop))*"0")+loop)
	printls = runskip(printls, key1, True)
	printls = runskip(printls, key2, False)
	data = [data[i:i+8] for i in range(0,len(data),8)]
	dprintdct = {}
	for i in printls:
		tmpkey = key3
		while printls.index(i)-tmpkey < 0:
			tmpkey -= len(printls)
		dprintdct[i] = printls[printls.index(i)-tmpkey] 
	if runthreaded: 
		with ThreadPool(CpuCoreCount) as pool:
			data = "".join(pool.map(unoffsetter, data))
	else:
		out = []
		for index, i in enumerate(data):
			out.append(unoffsetter(i))
		data = "".join(out)
	return data

def skippingencode(data, lkey): 
	lkey = [int("0x"+lkey[i:i+2],0) for i in range(0,len(lkey),2)]
	data = runoffset(data,lkey[4],lkey[2],lkey[3]) 
	data = [i for i in data]
	data = (runskip(data, lkey[0]+lkey[6], True))
	data = (runskip(data, lkey[1], False))
	for i in range(lkey[5]*16):
		data.append(data[random.randint(0,len(data)-1)])
	data = "".join(data)
	data = runoffset(data,lkey[7],lkey[8],lkey[9])
	return (data)

def skippingdecode(data, lkey): 
	lkey = [int("0x"+lkey[i:i+2],0) for i in range(0,len(lkey),2)]
	data = rundeoffset(data,lkey[7],lkey[8],lkey[9])
	data = [i for i in data]
	for i in range(lkey[5]*16):
		del data[-1]
	data = (unskip(data, lkey[1], False))
	data = (unskip(data, lkey[0]+lkey[6], True))
	data = "".join(data)
	data = rundeoffset(data,lkey[4],lkey[2],lkey[3])
	return (data)

def runencode(inputfilename, outputfile, key):
	with open(inputfilename,"rb") as txt:
		inputfile = fromfile(txt.read())
	with open(outputfile, "wb+") as txt:
		txt.write(tofile(skippingencode(inputfile,key)))

def rundecode(inputfilename, outputfile, key):
	with open(inputfilename,"rb") as txt:
		inputfile = fromfile(txt.read())
	with open(outputfile, "wb+") as txt:
		txt.write(tofile(skippingdecode(inputfile,key)))

runthreaded = False


class fileio: # object format fileio wrapper for SKCY11X, includes LZMA compression and sha256 checksumming

	def __enter__(self, filename, password): # with operator init
		self.filename = filename
		prehash = hashlib.sha256(password.encode("utf8")).digest()
		self.password = hex(int.from_bytes(prehash, "big"))[2:22]

	def __init__(self, filename, password): # init data
		self.filename = filename
		prehash = hashlib.sha256(password.encode("utf8")).digest()
		self.password = hex(int.from_bytes(prehash, "big"))[2:22]

	def write(self, towrite: bytes): # writes to file
		writeto = open(self.filename, "wb") 
		compressed = lzma.compress(towrite)
		shahash = hashlib.sha256(compressed).digest()
		encrypted = tofile(skippingencode(fromfile(compressed), self.password))
		writeto.write(b"SKCY11Xof\x00")
		writeto.write(shahash)
		writeto.write(encrypted)
		writeto.close()

	def read(self): # reads from file
		readfrom = open(self.filename, "rb")
		if readfrom.read(10) == b"SKCY11Xof\x00":
			testhash = readfrom.read(32)
			data = tofile(skippingdecode(fromfile(readfrom.read()),self.password))
			readfrom.close()
			if hashlib.sha256(data).digest() == testhash:
				return lzma.decompress(data)
			else:
				raise ValueError("The decrypted data does not match the SHA256 hash")
		else:
			readfrom.close()
			raise TypeError("The requested file is not a supported SKCY11X object format version, or in SKCY11X object format")
	
	def __exit__(self): # with operator deletes obj params
		del self.password
		del self.filename

	def close(self): # deletes obj params
		del self.password
		del self.filename

