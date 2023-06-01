import json
from web3 import Web3
from contract_abi import Backlog
from contract_abi import Voting
from contract_abi import CommunityFactory
from contract_abi.Backlog import backlog_abi
from contract_abi.CommunityFactory import com_factory_abi
from contract_abi.Voting import voting_abi

API_TOKEN = "t:ok-en"  # Paste your telegram api token here
INFURA_PROVIDER = f"https://sepolia.infura.io/v3/your_infura_id"  # paste your Infura ID here
GANACHE_PROVIDER = "http://127.0.0.1:7545"
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
w3 = Web3(Web3.HTTPProvider(INFURA_PROVIDER)) # you can paste your own provider here

ERC20_BALANCE_ABI = "contract_abi/ERC20Balance.json"
COMMUNITY_FACTORY_ABI = "contract_abi/CommunityFactory.py"
#SEPOLIA
COMMUNITY_FACTORY_ADDRESS = Web3.toChecksumAddress("0x64fE4979598eA35EB8E725FAfeeA1DFA7c11Bea2")
BACKLOG_ADDRESS = Web3.toChecksumAddress("0x16bccDedDDb5a2c412Dc5e269B327Ef34EEfEcA0")
VOTING_ADDRESS = Web3.toChecksumAddress("0xe7D5E1eeb5c1D76408978728d0D5bB0F80647Bd6")


task_created_sig_hash = ""
solution_proposed_sig_hash = ""
task_voting_started_sig_hash = ""
voting_started_sig_hash = ""
voting_results_counted_sig_hash = ""
task_voting_counted_sig_hash = ""
task_rewarded_sig_hash = ""
member_created_sig_hash = ""
member_deleted_sig_hash = ""
com_created_sig_hash = ""
mem_voted_sig_hash = ""
mem_verified_sig_hash = ""
verification_accepted_sig_hash = ""


task_created_event_filter = 0
solution_proposed_event_filter = 0
task_voting_started_event_filter = 0
voting_started_event_filter = 0
voting_results_counted_event_filter = 0
task_voting_counted_event_filter = 0
task_rewarded_event_filter = 0
member_created_event_filter = 0
member_deleted_event_filter = 0
com_created_event_filter = 0
mem_voted_event_filter = 0
mem_verified_event_filter = 0
verification_accepted_event_filter = 0


def init() -> []:
    Backlog.backlog = json.loads(backlog_abi)
    Voting.voting = json.loads(voting_abi)
    CommunityFactory.com_factory = json.loads(com_factory_abi)

    CommunityFactory.cf_contract = w3.eth.contract(address=COMMUNITY_FACTORY_ADDRESS, abi=CommunityFactory.com_factory)
    Backlog.backlog_contract = w3.eth.contract(address=BACKLOG_ADDRESS, abi=Backlog.backlog)
    Voting.voting_contract = w3.eth.contract(address=BACKLOG_ADDRESS, abi=Voting.voting)


    # init sig hashes
    member_created_sig_hash = w3.keccak(text="MemberCreated(address,uint256,address,uint256)").hex()
    member_deleted_sig_hash = w3.keccak(text="MemberDeleted(uint256,address,address,uint256)").hex()
    task_created_sig_hash = w3.keccak(text="TaskCreated(uint256,address,uint256,string,string,uint256,uint256)").hex()
    solution_proposed_sig_hash = w3.keccak(text="SolutionProposed(address,uint256,uint256,uint256,string)").hex()
    task_voting_started_sig_hash = w3.keccak(text="VotingOnTaskStarted(uint256,address,uint256,uint256,string,uint256,uint256,uint256)").hex()
    voting_started_sig_hash = w3.keccak(text="ProposalCreated(address,uint256,uint256,string,uint256,uint256)").hex()
    voting_results_counted_sig_hash = w3.keccak(text="ProposalExecuted(address,uint256,uint256[])").hex()
    task_voting_counted_sig_hash = w3.keccak(text="ResultsCounted(uint256,address,uint256)").hex()
    task_rewarded_sig_hash = w3.keccak(text="TaskClosed(address,uint256)").hex()
    com_created_sig_hash = w3.keccak(text="CommunityCreated(uint256,address,address,uint256,address)").hex()
    mem_voted_sig_hash = w3.keccak(text="MemberVoted(uint256,uint256,uint256)").hex()
    mem_verified_sig_hash = w3.keccak(text="MemberVerified(uint256,uint256)").hex()
    verification_accepted_sig_hash = w3.keccak(text="VerificationAccepted(uint256,uint256,uint256)").hex()

    # init event filters
    filters = []

    task_created_event_filter = w3.eth.filter({
        "address": BACKLOG_ADDRESS,
        "topics": [task_created_sig_hash],
    })
    filters.append(task_created_event_filter)

    solution_proposed_event_filter = w3.eth.filter({
        "address": BACKLOG_ADDRESS,
        "topics": [solution_proposed_sig_hash],
    })
    filters.append(solution_proposed_event_filter)

    task_voting_started_event_filter = w3.eth.filter({
        "address": BACKLOG_ADDRESS,
        "topics": [task_voting_started_sig_hash],
    })
    filters.append(task_voting_started_event_filter)

    voting_started_event_filter = w3.eth.filter({
        "address": VOTING_ADDRESS,
        "topics": [voting_started_sig_hash],
    })
    filters.append(voting_started_event_filter)

    voting_results_counted_event_filter = w3.eth.filter({
        "address": VOTING_ADDRESS,
        "topics": [voting_results_counted_sig_hash],
    })
    filters.append(voting_results_counted_event_filter)

    task_voting_counted_event_filter = w3.eth.filter({
        "address": BACKLOG_ADDRESS,
        "topics": [task_voting_counted_sig_hash],
    })
    filters.append(task_voting_counted_event_filter)

    task_rewarded_event_filter = w3.eth.filter({
        "address": BACKLOG_ADDRESS,
        "topics": [task_rewarded_sig_hash],
    })
    filters.append(task_rewarded_event_filter)

    member_created_event_filter = w3.eth.filter({
        "address": COMMUNITY_FACTORY_ADDRESS,
        "topics": [member_created_sig_hash],
    })
    filters.append(member_created_event_filter)

    member_deleted_event_filter = w3.eth.filter({
        "address": COMMUNITY_FACTORY_ADDRESS,
        "topics": [member_deleted_sig_hash],
    })
    filters.append(member_deleted_event_filter)

    com_created_event_filter = w3.eth.filter({
        "address": COMMUNITY_FACTORY_ADDRESS,
        "topics": [com_created_sig_hash],
    })
    filters.append(com_created_event_filter)

    mem_voted_event_filter = w3.eth.filter({
        "address": VOTING_ADDRESS,
        "topics": [mem_voted_sig_hash],
    })
    filters.append(mem_voted_event_filter)

    mem_verified_event_filter = w3.eth.filter({
        "address": COMMUNITY_FACTORY_ADDRESS,
        "topics": [mem_verified_sig_hash],
    })
    filters.append(mem_verified_event_filter)

    verification_accepted_event_filter = w3.eth.filter({
        "address": COMMUNITY_FACTORY_ADDRESS,
        "topics": [verification_accepted_sig_hash],
    })
    filters.append(verification_accepted_event_filter)

    return filters

