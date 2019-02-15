from toobuk.tb import Toobuk

class Debt:
	def __init__(self) :
		self._walker = Toobuk('statist/debt/debt.json')

class DebtClass(Debt) :
	def grumble(self) :
		return self._walker.get('debtClass')


class GovernmentDebtRatio(Debt) :
	def grumble(self) :
		return self._walker.get('governmentDebtRatio')

class DebtCp(Debt) :
	def grumble(self) :
		return self._walker.get('debtCp')
