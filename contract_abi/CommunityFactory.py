import json
from web3 import Web3, HTTPProvider

INFURA_PROVIDER = f"https://sepolia.infura.io/v3/your_infura_id" #your api key
GANACHE_PROVIDER = "http://127.0.0.1:7545"
w3 = Web3(HTTPProvider(INFURA_PROVIDER)) # your provider

com_factory_abi = """
[
	{
		"inputs": [],
		"name": "changeCommunityToken",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "comId",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "changeComOwner",
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
				"name": "_threshold",
				"type": "uint256"
			}
		],
		"name": "changeJoiningTokenThreshold",
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
				"name": "_threshold",
				"type": "uint256"
			}
		],
		"name": "changeVerificationThreshold",
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
				"name": "comWallet",
				"type": "address"
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
				"name": "creatorId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "address",
				"name": "creatorAddress",
				"type": "address"
			}
		],
		"name": "CommunityCreated",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_wallet",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_mainToken",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "creatorTgID",
				"type": "uint256"
			}
		],
		"name": "createCommunity",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "comId",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_symbol",
				"type": "string"
			},
			{
				"internalType": "uint128",
				"name": "_startPrice",
				"type": "uint128"
			},
			{
				"internalType": "address",
				"name": "_communityWallet",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "creatorTgID",
				"type": "uint256"
			}
		],
		"name": "createCommunityWithToken",
		"outputs": [
			{
				"internalType": "address",
				"name": "tokenAddress",
				"type": "address"
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
				"name": "_tgID",
				"type": "uint256"
			}
		],
		"name": "createMember",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_symbol",
				"type": "string"
			},
			{
				"internalType": "uint128",
				"name": "_startPrice",
				"type": "uint128"
			},
			{
				"internalType": "uint256",
				"name": "_comId",
				"type": "uint256"
			}
		],
		"name": "CreateNewToken",
		"outputs": [
			{
				"internalType": "address",
				"name": "tokenAddr",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_mainToken",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_member",
				"type": "address"
			}
		],
		"name": "deleteMember",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_backlog",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_voting",
				"type": "address"
			}
		],
		"name": "initializeFactory",
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
				"name": "_member",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "_tgID",
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
				"name": "_comId",
				"type": "uint256"
			}
		],
		"name": "MemberCreated",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "tgId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "address",
				"name": "_member",
				"type": "address"
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
				"name": "_comId",
				"type": "uint256"
			}
		],
		"name": "MemberDeleted",
		"type": "event"
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
				"name": "memberId",
				"type": "uint256"
			}
		],
		"name": "MemberVerified",
		"type": "event"
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
				"name": "token",
				"type": "address"
			}
		],
		"name": "TokenCreated",
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
				"internalType": "uint256",
				"name": "senderId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "memberId",
				"type": "uint256"
			}
		],
		"name": "VerificationAccepted",
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
				"name": "_tgId",
				"type": "uint256"
			}
		],
		"name": "verifyMember",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_i",
				"type": "uint256"
			}
		],
		"name": "communityAt",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_com_tok",
				"type": "address"
			}
		],
		"name": "communityExists",
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
				"internalType": "address",
				"name": "_communityWallet",
				"type": "address"
			}
		],
		"name": "containsCommunity",
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
				"internalType": "address",
				"name": "_com_tok",
				"type": "address"
			}
		],
		"name": "getComIdByToken",
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
		"name": "getCommunities",
		"outputs": [
			{
				"internalType": "address[]",
				"name": "",
				"type": "address[]"
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
		"name": "getMainCommunityToken",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
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
				"name": "_tgId",
				"type": "uint256"
			}
		],
		"name": "getMemberAddress",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
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
				"internalType": "address",
				"name": "_member",
				"type": "address"
			}
		],
		"name": "getMemberTgId",
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
				"internalType": "address",
				"name": "_comToken",
				"type": "address"
			}
		],
		"name": "getParticipationThreshold",
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
				"internalType": "address",
				"name": "_user",
				"type": "address"
			}
		],
		"name": "isComOwner",
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
				"internalType": "address",
				"name": "_user",
				"type": "address"
			}
		],
		"name": "isMember",
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
				"internalType": "address",
				"name": "_user",
				"type": "address"
			}
		],
		"name": "isVerifiedMember",
		"outputs": [
			{
				"internalType": "bool",
				"name": "isVerified",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "numberOfCommunities",
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
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "tokenToCommunity",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
"""

COMMUNITY_FACTORY_ADDRESS = Web3.toChecksumAddress("0x8b90D81901A3F1566b064d491794b72eE5BEf0B2")
com_factory = json.loads(com_factory_abi)
cf_contract = w3.eth.contract(address=COMMUNITY_FACTORY_ADDRESS, abi=com_factory)
