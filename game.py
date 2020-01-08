class Game:
	def __init__(self, id = 0):
		self.id = id
		self.ready = False
		self.score = [0, 0]

		self.playerID = []
		self.playerImgNum = []
		self.playerPOS = []
		self.playerLives = []
		self.playerHidden = []
		self.move = [] #(0, 0, 0, 0)上下左右 方向鍵

		self.rockImgNum = []
		self.rockAngle = []
		self.rockScale = []
		self.rockPOS = []

		self.conesAngle = []
		self.conesPOS = []

		self.motoImgNum = []
		self.motoPOS = []
		self.motoSpeedx = []
		self.motoSpeedy = []

		self.gasPOS = []

	def addPlayer(self, ID, imgNum, POS, Lives = 3):
		self.playerID = ID
		self.playerImgNum.append(imgNum)
		self.playerPOS.append(POS)
		self.playerLives.append(Lives)

	def addRock(self, imgNum, POS, angle, scale):
		print('add rock')
		self.rockImgNum.append(imgNum)
		self.rockPOS.append(POS)
		self.rockAngle.append(angle)
		self.rockScale.append(scale)

	def addCones(self, POS, angle):
		self.conesAngle.append(angle)
		self.conesPOS.append(POS)

	def addMoto(self, imgNum, POS, speedy, speedx):
		self.motoImgNum.append(imgNum)
		self.motoPOS.append(POS)
		self.motoSpeedx.append(speedy)
		self.motoSpeedy.append(speedx)

	def addGas(self, POS):
		self.gasPOS = POS

	def delRock(self, n):
		del self.rockImgNum[n]
		del self.rockAngle[n]
		del self.rockScale[n]
		del self.rockPOS[n]

	def delMoto(self, n):
		del self.motoImgNum[n]
		del self.motoPOS[n]
		del self.motoSpeedx[n]
		del self.motoSpeedy[n]

	def delGas(self, n):
		del gasPOS[n]

	def clearPlayer(self):
		self.playerID = []
		self.playerImgNum = []
		self.playerPOS = []
		self.playerLives = []
		self.playerHidden = []
		self.move = [] #(0, 0, 0, 0)上下左右 方向鍵

	def clearRock(self):
		self.rockImgNum = []
		self.rockAngle = []
		self.rockScale = []
		self.rockPOS = []

	def clearCones(self):		
		self.conesAngle = []
		self.conesPOS = []

	def clearMoto(self):
		self.motoImgNum = []
		self.motoPOS = []
		self.motoSpeedx = []
		self.motoSpeedy = []

	def clearGas(self):
		self.gasPOS = []



