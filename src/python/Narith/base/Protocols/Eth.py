'''
[Narith]
File:   Eth.py
Author: Saad Talaat
Date:   15th July 2013
brief:  Structure to hold Ethernet info
'''
from Exceptions.Exceptions import *
class Eth(object):

	# FLAGS
	
	#type of data rep of input
	ISSTRING = False
	
	__protocols = {	'\x80\x06' : 'arp',
			'\x80\x00' : 'ip'
			}
		
	def __init__(self, dst, src, t):

		# Check if in binary stream format or seperated format
		if(type(dst) == str):
			try:
				assert len(dst.split(":")) == 6 
				assert len(src.split(":")) == 6
				self.__sdst__ = dst
				self.__ssrc__ = src
				self.ISSTRING = True
				self.rawDstSrc()
			except:
				if(len(dst) != 6) or (len(src) != 6):
					raise MacAddrError,"Invalid Source or Desination Address"
				self.__dst__ = dst
				self.__src__ = src
				pass

		# if not then assign them to raw variables
		# and conduct string initalization
		assert t in self.__protocols.keys(),"Unsupported protocol"
		self.__type__ = t
		self.strDstSrc()

	def rawDstSrc(self):
		self.__dst__ = "".join([chr(j) for j in  [int(c,base=16) for c in self.__sdst__.split(":")]])
		self.__src__ = "".join([chr(j) for j in  [int(c,base=16) for c in self.__ssrc__.split(":")]])
		return (self.__dst__, self.__src__)


	#return pair or (dst,src) in seperated representation
	def strDstSrc(self):
		if self.ISSTRING:
			return (self.__sdst__, self.__ssrc__)
		dst = ""
		src = ""
		for c in self.__dst__:
			dst += c.encode('hex')
			dst += ":"
		dst = dst[:len(dst)-1]
		for c in self.__src__:
			src += c.encode('hex')
			src += ":"
		src = src[:len(src)-1]
		self.__sdst__ = dst
		self.__ssrc__ = src
		self.ISSTRING = True
		return (dst,src)

	############################
	# Boolean Packet type checks
	def isIP(self):
		return self.__protocols[self.__type__] == 'ip'
	def isARP(self):
		return self.__protocols[self.__type__] == 'arp'


	############################
	# Properties
	@property
	def dst(self):
		return self.__sdst__
	@dst.setter
	def dst(self,val):
		if type(val) != str:
			raise ValueError,"Malformed Value"
		elif len(val.split(":")) != 6:
			raise ValueError,"Malformed Value"
		self.__sdst__ = val
		self.__dst__ = "".join([chr(j) for j in  [int(c,base=16) for c in self.__sdst__.split(":")]])

	@property
	def src(self):
		return self.__ssrc__

	@src.setter
	def src(self,val):
		if type(val) != str:
			raise ValueError,"Malformed Value"
		elif len(val.split(":")) != 6:
			raise ValueError, "Malformed Value"
		self.__ssrc__ = val
		self.__src__ = "".join([chr(j) for j in  [int(c,base=16) for c in self.__ssrc__.split(":")]])

	@property
	def protocol(self):
		return self.__protocols[self.__type__]
	@protocol.setter
	def protocol(self,value):
		if( value not in self.__protocols.values()):
			raise ValueError,"Unsupported protocol"
		for k,v in self.__protocols.iteritems():
			if v == value:
				self.__type__ = k
