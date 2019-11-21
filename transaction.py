class Transaction:
  def __init__(self, fromAddress, toAddress, value, gas, gasPrice, transactionHash):
    self.fromAddress = fromAddress
    self.toAddress = toAddress
    self.value = value
    self.gas = gas
    self.gasPrice = gasPrice
    self.transactionHash = transactionHash

  def __repr__(self):
    return f' hash: {self.transactionHash}, fromAddress: {self.fromAddress}, toAddress: {self.toAddress}, value: {self.value}'
  
  def __eq__(self, other):
    """Overrides the default implementation"""
    if isinstance(other, self.__class__):
        return (self.fromAddress == other.fromAddress and self.toAddress == other.toAddress and self.value == other.value 
                and self.gas == other.gas and self.gasPrice == other.gasPrice and self.transactionHash == other.transactionHash)
    return False

  def __ne__(self, other):
    return not self.__eq__(other)

  def __hash__(self):
      return hash((self.fromAddress, self.toAddress, self.value, self.gas, self.gasPrice, self.transactionHash))