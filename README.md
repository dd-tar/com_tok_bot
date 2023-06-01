# ComTokBot
This repository contains the code of the ComTokBot for Telegram. It is a part of final qualifying paper on the topic
"Tools for building tokenized communities". Telegram bot provides the user interface of the developed system.

See also smart contracts of the system:  
https://github.com/dd-tar/com_tok_contracts

Transaction Signing Site:  
https://github.com/dd-tar/com_tok_tx_provider

##  Main project files
`/contracts_abi` - a folder contains ABI of smart contracts of the system and their instances  
`/db` - a folder for the system's database. It stores only the correspondence of the community chat ID to its token address in the blockchain.  
`constants.py` - stores the main constants used by the bot, such as contract addresses and event signatures  
`server.py` - main project file. Stores bot command handlers and the function to launch the bot  
`event_handlers.py` - contains functions for receiving and processing smart contract system events  
`helpers.py` - some auxiliary functions of the system are implemented here, for example, for checking values or accessing the database  
`contracts_reader.py` - implements functions for reading information stored in smart contracts.


## Launching the bot

In the project directory, you can run:

### `python server.py`

Runs the bot locally.


In order to start the system, you need to ***first fill in some constants***:
1. Insert your Infura API key to the `INFURA_PROVIDER` variable in  
   /contracts_abi/Backlog.py  
   /contracts_abi/CommunityFactory.py  
   /contracts_abi/Voting.py  
   constants.py
2. Insert your Telegram API Token to the `API_TOKEN` variable in the constants.py file*

*If you don't know what it is, here are the instructions:  
https://core.telegram.org/bots/features#botfather

Please note that depending on the usage activity, the bot can make many requests to smart contracts. This means that the number of requests may exceed the limit of the free Infura plan, after which the bot will start receiving "Error 429" in response to requests.

You can also use [Ganache](https://trufflesuite.com/ganache/) to test the system, but in this case, you need to deploy your own instances of smart contracts on it's local network (see the instruction in the [com_tok_contracts repository](https://github.com/dd-tar/com_tok_contracts)).  
In this case, to launch the bot, after you get your contract's adresses:
1. Replace values of `COMMUNITY_FACTORY_ADDRESS`, `BACKLOG_ADDRESS`, `VOTING_ADDRESS` variables with corresponding new addresses in Ganache network  in  the same files:  
   /contracts_abi/Backlog.py  
   /contracts_abi/CommunityFactory.py  
   /contracts_abi/Voting.py  
   constants.py
3. Fill in `GANACHE_PROVIDER` instead of `INFURA_PROVIDER`
4. Insert your Telegram API Token to the `API_TOKEN` variable in the constants.py file  
