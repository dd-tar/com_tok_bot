import json
import time

import constants
from constants import w3
from contract_abi.CommunityFactory import cf_contract
from contract_abi.Voting import voting_contract
from contract_abi.Backlog import backlog_contract


async def is_member(com_id, tg_id: int) -> bool:
    mem_addr = cf_contract.functions.getMemberAddress(com_id, tg_id).call()
    is_mem = cf_contract.functions.isMember(com_id, mem_addr).call()
    print(f"is member: {is_mem}")
    return is_mem


async def is_veriied_member(com_id, tg_id: int) -> bool:

    mem_addr = cf_contract.functions.getMemberAddress(com_id, tg_id).call()
    is_verified = cf_contract.functions.isVerifiedMember(com_id, mem_addr).call()
    print(f"is_veriied_member: {is_verified}")
    return is_verified


async def is_com_owner(com_tok, tg_id) -> bool:
    ctr_com_id = await get_ctr_com_id_by_token(com_tok)
    # get member's address by tgId
    mem_addr = cf_contract.functions.getMemberAddress(ctr_com_id, tg_id).call()
    # check isComOwner(comId, member's address)
    is_owner = cf_contract.functions.isComOwner(ctr_com_id, mem_addr).call()
    print(f"is owner: {is_owner}")
    return is_owner


async def com_exists(token_addr: str) -> bool:
    print("com_exists\n")
    exists = cf_contract.functions.communityExists(token_addr).call()
    print(exists)
    return exists


async def get_ctr_com_id_by_token(com_tok) -> int:
    ctr_com_id = cf_contract.functions.getComIdByToken(com_tok).call()
    print("\nctr_com_id: ", ctr_com_id)
    return ctr_com_id


async def get_task_name(ctr_com_id, task_id: int) -> str:
    name = backlog_contract.functions.getTaskName(ctr_com_id, task_id).call()
    # returns "" if there's no such task
    return name


async def get_task_description(ctr_com_id, task_id) -> str:
    descr = backlog_contract.functions.getTaskDescription(ctr_com_id, task_id).call()
    # returns "" if there's no such task
    return descr


async def get_number_of_solutions(ctr_com_id, task_id) -> int:
    n = backlog_contract.functions.getNumberOfSolutions(ctr_com_id, task_id).call()
    # returns "" if there's no such task
    return n


async def get_voting_by_task_id(ctr_com_id, task_id) -> int:
    try:
        n = backlog_contract.functions.getVotingByTaskId(ctr_com_id, task_id).call()
    except Exception as e:
        print(e.args)
        return -1
    # will fall if task is not on voting
    return n


async def get_voting(_bot, ctr_com_id, chat_id, voting_id) -> str:
    creator_id = voting_contract.functions.getVotingCreator(ctr_com_id, voting_id).call()
    descr = voting_contract.functions.getVotingDescription(ctr_com_id, voting_id).call()
    deadline_ts = voting_contract.functions.getVotingDeadline(ctr_com_id, voting_id).call()
    date_time_deadline = time.strftime("%a, %d %b %Y %H:%M:%S MSK", time.localtime(deadline_ts))
    executed = voting_contract.functions.getVotingExecuted(ctr_com_id, voting_id).call()
    n_options = voting_contract.functions.getVotingNumberOfOptions(ctr_com_id, voting_id).call()
    winning_options = voting_contract.functions.getVotingWinningOptions(ctr_com_id, voting_id).call()
    disclaimer = "\nThe description of the options should be presented in the description of the task by its creator."
    try:
        creator = await _bot.get_chat_member(chat_id, creator_id)
        creator_username = creator.user.mention
    except Exception as e:
        creator_username = f"Creator left the chat. Creator Telegram ID: {creator_id}"

    res = f"Voting id: {voting_id}\n" \
          f"Creator Telegram username: {creator_username}\n" \
          f"Proposal description: {descr}\n" \
          f"Voting deadline: {date_time_deadline}\n" \
          f"Option IDs: from 1 to {n_options} inclusive.\n" \
          f"Executed?: {executed}\n" \
          f"Winning options: {winning_options}\n" + disclaimer
    return res


async def get_task(_bot, ctr_com_id, chat_id, task_id) -> str:
    creator_id = backlog_contract.functions.getTaskCreator(ctr_com_id, task_id).call()
    if creator_id == 0:
        return "Task with this ID doesn't exist"
    name = await get_task_name(ctr_com_id, task_id)
    descr = await get_task_description(ctr_com_id, task_id)
    deadline_ts = backlog_contract.functions.getTaskDeadline(ctr_com_id, task_id).call()
    date_time_deadline = time.strftime("%a, %d %b %Y %H:%M:%S MSK", time.localtime(deadline_ts))
    # TODO: REWARD
    status = backlog_contract.functions.getTaskStatus(ctr_com_id, task_id).call()
    n_solutions = backlog_contract.functions.getNumberOfSolutions(ctr_com_id, task_id).call()
    voting_id = await get_voting_by_task_id(ctr_com_id, task_id)
    _voting_id = voting_id
    if voting_id == -1:
        _voting_id = "There's no voting for this task"

    disclaimer = "\nThe description of the task and acceptance criteria must be presented in the description of the task " \
                 "by its creator.\n" \
                 "To get solution description use <code>/get_solution solution_id</code> command in dm with bot\n" \
                 f"IDs of solutions - from 1 to the number of solutions ({n_solutions})."

    try:
        creator = await _bot.get_chat_member(int(chat_id), int(creator_id))
        creator_username = creator.user.mention
    except Exception as e:
        creator_username = f"Creator left the chat. Creator Telegram ID: {creator_id}"

    res = f"Task id: <code>{task_id}</code>\n" \
          f"Name: {name}\n" \
          f"Creator Telegram username: {creator_username}\n" \
          f"Task description: {descr}\n" \
          f"Deadline: {date_time_deadline}\n" \
          f"Status?: {status}\n" \
          f"Current number of solutions: {n_solutions}\n" \
          f"Voting ID: <code>{_voting_id}</code>\n" \
          + disclaimer
    return res


async def get_solution(ctr_com_id, task_id, sol_id) -> str:
    n_solutions = backlog_contract.functions.getNumberOfSolutions(ctr_com_id, task_id).call()
    if sol_id > n_solutions:
        return f"Task ID should be from 1 to {n_solutions} inclusively"
    sol_descr = backlog_contract.functions.getSolutionById(ctr_com_id, task_id, sol_id).call()
    res = f"Solution id: <code>{sol_id}</code>\n" \
          f"Solution description: {sol_descr}"
    return res


async def get_voting_winning_options(ctr_com_id, voting_id):
    try:
        options = voting_contract.functions.getVotingWinningOptions(ctr_com_id, voting_id).call()
    except Exception as e:
        options = []
    return options


async def is_token_owner(user_address, token_address) -> bool:
    with open(constants.ERC20_BALANCE_ABI, 'r') as f:
        _abi = json.load(f)

    erc20_contract = w3.eth.contract(address=token_address, abi=_abi)
    is_owner = erc20_contract.functions.balanceOf(user_address).call()
    print(f"is owner: {is_owner}")
    if is_owner >= 1e18:
        return True
    return False
