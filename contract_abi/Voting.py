import json
from web3 import Web3, HTTPProvider

INFURA_PROVIDER = f"https://sepolia.infura.io/v3/your_api_key" # paste your Infura API key here
GANACHE_PROVIDER = "http://127.0.0.1:7545"
w3 = Web3(HTTPProvider(INFURA_PROVIDER))  # your provider

voting_abi = """
[
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_comId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_newThreshold",
				"type": "uint256"
			}
		],
		"name": "changeVotingThreshold",
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
				"internalType": "address",
				"name": "_newVotingToken",
				"type": "address"
			}
		],
		"name": "changeVotingToken",
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
				"internalType": "string",
				"name": "_proposal",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_numberOfOptions",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_deadline",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "creator",
				"type": "address"
			}
		],
		"name": "createProposal",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "votingID",
				"type": "uint256"
			}
		],
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
				"name": "_proposalId",
				"type": "uint256"
			}
		],
		"name": "executeVoting",
		"outputs": [
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_communityFactory",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_backlog",
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
				"name": "comId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "proposalId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "member",
				"type": "uint256"
			}
		],
		"name": "MemberVoted",
		"type": "event"
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
				"name": "proposalId",
				"type": "uint256"
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
				"name": "proposal",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "numberOfOptions",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "deadline",
				"type": "uint256"
			}
		],
		"name": "ProposalCreated",
		"type": "event"
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
				"name": "proposalId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256[]",
				"name": "winningOptions",
				"type": "uint256[]"
			}
		],
		"name": "ProposalExecuted",
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
				"name": "_propId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_choice",
				"type": "uint256"
			}
		],
		"name": "vote",
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
			}
		],
		"name": "getNumberOfVotings",
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
				"name": "_propId",
				"type": "uint256"
			}
		],
		"name": "getVotingCreator",
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
				"name": "_propId",
				"type": "uint256"
			}
		],
		"name": "getVotingDeadline",
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
				"name": "_propId",
				"type": "uint256"
			}
		],
		"name": "getVotingDescription",
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
				"name": "_propId",
				"type": "uint256"
			}
		],
		"name": "getVotingExecuted",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
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
				"name": "_propId",
				"type": "uint256"
			}
		],
		"name": "getVotingNumberOfOptions",
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
				"name": "_propId",
				"type": "uint256"
			}
		],
		"name": "getVotingWinningOptions",
		"outputs": [
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
"""

VOTING_ADDRESS = Web3.toChecksumAddress("0xb153209ea928D55415a52A5e0dfaCd917311CA32")
voting = json.loads(voting_abi)
voting_contract = w3.eth.contract(address=VOTING_ADDRESS, abi=voting)
