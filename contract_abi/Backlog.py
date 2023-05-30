import json
from web3 import Web3, HTTPProvider

INFURA_PROVIDER = f"https://sepolia.infura.io/v3/your_api_key" #your api key
GANACHE_PROVIDER = "http://127.0.0.1:7545"
w3 = Web3(HTTPProvider(INFURA_PROVIDER)) # or you can use your own provider

backlog_abi = """
[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_communityFactory",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "communityId",
				"type": "uint256"
			}
		],
		"name": "BacklogCreated",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_comId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_threshold",
				"type": "uint256"
			}
		],
		"name": "changeThresholdForTasks",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_comId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_taskId",
				"type": "uint256"
			}
		],
		"name": "countResults",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_communityId",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_description",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_deadline",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_reward",
				"type": "uint256"
			}
		],
		"name": "createTask",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_votingContract",
				"type": "address"
			}
		],
		"name": "initialize",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "previousOwner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "OwnershipTransferred",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_comId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_taskId",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_solution",
				"type": "string"
			}
		],
		"name": "proposeSolution",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "renounceOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "comId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "address",
				"name": "comToken",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "taskId",
				"type": "uint256"
			}
		],
		"name": "ResultsCounted",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_comId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_taskId",
				"type": "uint256"
			}
		],
		"name": "rewardSolversAndClose",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "address",
				"name": "comToken",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "taskId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "solId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "solver",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "solutionLink",
				"type": "string"
			}
		],
		"name": "SolutionProposed",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_taskId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_comId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_votingDeadline",
				"type": "uint256"
			}
		],
		"name": "startVoting",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "address",
				"name": "comToken",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "taskId",
				"type": "uint256"
			}
		],
		"name": "TaskClosed",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "taskId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "address",
				"name": "comToken",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "creator",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "description",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "deadline",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "reward",
				"type": "uint256"
			}
		],
		"name": "TaskCreated",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "transferOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "comId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "address",
				"name": "comToken",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "taskId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "votingId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "proposal",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "numberOfChoices",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "reward",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "deadline",
				"type": "uint256"
			}
		],
		"name": "VotingOnTaskStarted",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_comId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_taskId",
				"type": "uint256"
			}
		],
		"name": "getNumberOfSolutions",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_comId",
				"type": "uint256"
			}
		],
		"name": "getNumberOfTasks",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_comId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_taskId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_solId",
				"type": "uint256"
			}
		],
		"name": "getSolutionById",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_comId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_taskId",
				"type": "uint256"
			}
		],
		"name": "getTaskCreator",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_comId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_taskId",
				"type": "uint256"
			}
		],
		"name": "getTaskDeadline",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_comId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_taskId",
				"type": "uint256"
			}
		],
		"name": "getTaskDescription",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_comId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_taskId",
				"type": "uint256"
			}
		],
		"name": "getTaskName",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_comId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_taskId",
				"type": "uint256"
			}
		],
		"name": "getTaskReward",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_comId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_taskId",
				"type": "uint256"
			}
		],
		"name": "getTaskStatus",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_comId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_taskId",
				"type": "uint256"
			}
		],
		"name": "getVotingByTaskId",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
"""
BACKLOG_ADDRESS = Web3.toChecksumAddress("0xc69EBA07038E5940117ef1e427a4E12F474eE600")
backlog = json.loads(backlog_abi)
backlog_contract = w3.eth.contract(address=BACKLOG_ADDRESS, abi=backlog)
