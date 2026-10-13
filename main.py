from abc import ABC , abstractmethod


#Represents the central bank ,It stores basic bank information and keeps track of all branches.
class HeadOffice:
    def __init__(self,bankName,address):
        self.bankName=bankName   #The official name of the bank .
        self.address=address     #The physical address of the head office .
        self.branches=[]         #A list storing all Branch objects registered under this head office.

    def add_branch(self,branch):     #Adds a Branch object to the branches list. This registers the branch under this head office.
        self.branches.append(branch)

    def list_branches(self):        #Prints the details of every branch stored in branches .
        for branch in self.branches:
            print(branch)

    def __str__(self):         #Returns a readable string.
        return f"The branches are : {self.branches}"
    


#Represents a physical bank location ,It manages the accounts opened at that branch.
class Branch:
    def __init__(self,address,manager):
        self.address=address    #Address of the branch.
        self.manager=manager    #Full name of the branch manager.
        self.accounts=[]       #A list of all Account objects opened at this branch.


    def open_account(self,account):     #Adds an Account object to the accounts list. Represents opening a new account at this branch.
        self.accounts.append(account)


    def get_account(self,accountNumber):    #Searches accounts for an account matching accountNumber. Returns the Account if found.
        for acc in self.accounts:
            if acc.accountNumber==accountNumber:
              return acc
            return None
    
    def list_accounts(self):       #Prints a summary of every account in accounts.
        for acc in self.accounts:
            print(acc) 

    def __str__(self):
        return f"The accounts are: {self.accounts}"
    


#Represents a bank customer Variable Name Stores personal information only, it does not own accounts directly (accounts reference the customer).
class Customer:
    def __init__(self,name,address):
        self.name=name     #Full name of the customer.
        self.address=address  #Home address of the customer.

    def __str__(self):
        return f"The costomer is : {self.name} , and the home address: {self.address}"   
    


#• The Abstract base class for all account types.
#• It cannot be instantiated on its own. 
#• CurrentAccount and SavingsAccount inherit from this class.
class Account(ABC):
     def __init__(self,accountNumber,balance,branch,customer):
         self.accountNumber=accountNumber  #A unique identifier for the account.
         self.balance=balance              #The current money in the account. Must be ≥ 0 .
         self.branch=branch                #Reference to the Branch where this account was opened.
         self.customer=customer            #Reference to the Customer who owns this account.
         self.transaction=[]               #A list recording all transactions involving this account.

    
     def deposit(self,amount):   
         if amount<=0:           #Adds amount to balance. Raises ValueError if amount ≤ 0 .
             raise ValueError
         if amount>0:
             self.balance+=amount
         else:
             raise ValueError
         
     def add_transaction(self,tx):
         self.transaction.append(tx)
         
     def withdraw(self,amount):
         if amount<=0 :          #Subtracts amount from balance. Raises ValueError if amount ≤ 0 or if balance < amount (insufficient funds) .
             raise ValueError
         if self.balance<amount:
             raise ValueError
         else:
             self.balance-=amount

     def add_transaction(self,tx):
        self.transaction.append(tx)


     @abstractmethod
     def calcCharges(self):     #Abstract method, must be overridden in each subclass. Calculates and returns the applicable fee for this account .
         pass
     
     def __str__(self):
         return f"The acc: {self.accountNumber} , {self.balance} SR"
     


#• A type of account for everyday use 
#• It charges a fixed monthly fee regardless of the balance 
#• The fixed monthly fee is 5.0 SR
class CurrentAccount(Account):
    def __init__(self,accountNumber,balance,branch,customer):
        super().__init__(accountNumber,balance,branch,customer)   #Calls super().__init__(...) to set inherited variables.

    def calcCharges(self):
        return 5.0        #Returns the account monthly charges .
    


#• A type of account designed for saving money .
#• It has a monthly fee of 2.0 SR if balance < 5000.0 SR .
class SavingAccount(Account):
    def __init__(self,accountNumber,balance,branch,customer):
        super().__init__(accountNumber,balance,branch,customer)  #Calls super().__init__(...) to set inherited variables.

    def calcCharges(self):
        return 2.0 if self.balance<5000 else 0.0   #Returns the account monthly charges.
    


#• Records a single money transfer between two accounts .
#• Created by BankService after a successful transfer .
class Transaction:
    def __init__(self,value,debit_from,credit_to):
        self.value=value  #The amount of money transferred (must be > 0).
        self.debit_from=debit_from   #The account that money was taken FROM .
        self.credit_to=credit_to  #The account that money was sent TO.

    def __str__(self):     #Returns a readable string .
        return f"{self.value} , {self.debit_from} , {self.credit_to}"
    


#• A service class that handles the logic for transferring money between accounts safely 
#• It has no variables, it only contains the transfer method 
#• The transfer() method must check ALL of the following: 
   #1) amount must be > 0  →  raise ValueError if not. 
   #2) debit_from and credit_to must be different accounts  →  raise ValueError if same. 
   #3) Call debit_from.withdraw(amount) first — if balance is insufficient, withdraw raises an error automatically. 
   #4) Only if withdraw succeeded: call credit_to.deposit(amount). 
   #5) Create a Transaction object with value=amount, debit_from, credit_to .
   #6) Call add_transaction(tx) on BOTH accounts .
   #7) Return the Transaction object. 
class BankService:
    def transfer(debit_from,credit_to,amount):
        if amount<0 :
            raise ValueError
        
        if debit_from ==credit_to :
            raise ValueError
        

        debit_from.withdraw(amount) 
        credit_to.deposit(amount)

        tx= Transaction(amount,debit_from,credit_to)
        debit_from.add_transaction(tx)
        credit_to.add_transaction(tx)
        return tx
    

#------------------------------------------------------------------------------------------------------------------------------------------------


if __name__=="__main__":

    #creat the bank and branches.
    ho=HeadOffice("UQU Bank","Makkah")
    br1=Branch("Aziziyah","Ahmed")
    ho.add_branch(br1)

    #creat the custemors and accounts.
    c1=Customer("Ali","Street 1")
    c2=Customer("Fajr Alosaimi", "Street 4")
    acc1=CurrentAccount("SA04",10000,br1,c1)
    acc2=CurrentAccount("SA03",20000,br1,c2)
    acc3=SavingAccount("SA08",4000,br1,c1)
    acc4=SavingAccount("SA09",5000,br1,c2)
    
    br1.open_account(acc1)
    br1.open_account(acc2)
    br1.open_account(acc3)
    br1.open_account(acc4)

    #operations execution .
    BankService.transfer(acc1, acc3 , 2000)


    #print 
    print(f"The bank name is: {ho.bankName}")
    
    print(f"The list accounts are : " )
    br1.list_accounts()
    
    print(f" Charges for Acc3: {acc3.calcCharges() } SR")
          

    


    




     



          
         
 
    


    

    
        

        





    
