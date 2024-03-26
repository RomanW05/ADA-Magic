####MINTING####
'''	We want to create an NFT and charge a fee for it.
	in the process we need to specifically identify the policyID, NFTName and NFTID to tell which 
	metadata exactly we refer to based upon those unique conditions.
	
	Steps to follow:
	-Load wallet status
	-Receive and clean output from shell
	-Strip and select txins that have ADAs so we can make the mint = transactionGatherer()
		-If there is not enough money we will try looking for money in the minted transactions
			-If there is no money: Return not enough funds
			-If there is enough money, send NFT to oneself with minimun ADA to split the transaction

