import asyncio
import time
from datetime import datetime, timedelta, timezone
from aiogram import Bot
import eth_abi
from web3 import Web3
import contracts_reader
import helpers
from constants import w3
import constants

tzdata = timezone(timedelta(hours=3))


def handle_task_created(event):
    print("task created")
    # event args: uint256 taskId, address comToken, uint256 creator, string name, string description, uint deadline, uint reward
    print("Event: ", event)
    data = Web3.toBytes(hexstr=event['data'])
    decoded = eth_abi.decode_abi(['uint256', 'address', 'uint256', 'string', 'string', 'uint256', 'uint256'], data)
    print("\ndecoded args: ", decoded)
    task_id = decoded[0]
    com_tok = w3.toChecksumAddress(decoded[1])
    creator_tg_id = decoded[2]
    name = decoded[3]
    description = decoded[4]
    deadline_ts = decoded[5]
    reward = decoded[6]
    dt_deadline = time.strftime("%a, %d %b %Y %H:%M:%S MSK", time.localtime(deadline_ts))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        send_task_created(task_id, com_tok, creator_tg_id, name, description, dt_deadline, reward)
    )
    loop.close()


async def send_task_created(task_id, com_tok, creator_tg_id, name, description, date_time_deadline, reward):
    # contracts_reader.get_task(ctr_com_id, chat_id, task_id)
    print("\ncom_tok from event: ", com_tok)
    chat_id = await helpers.get_chat_id_by_token(com_tok)
    print("get_chat_id_by_token: ", chat_id)
    #chat_id = chat_id[0]
    disclaimer = "The description of the task and acceptance criteria must be presented in the description of " \
                 "the task by its creator.\n" \
                 f"To propose your solution use <code>/propose_solution {task_id}</code> command." \
                 f"To get solution description use <code>/get_solution {task_id} solution_id</code> command\n" \
                 f"IDs of solutions - from 0 to the number of solutions."
    _bot = Bot(token=constants.API_TOKEN)
    try:
        creator = await _bot.get_chat_member(chat_id, creator_tg_id)
        creator_username = creator.user.mention
    except Exception as e:
        creator_username = f"Creator left the chat. Creator Telegram ID: {creator_tg_id}"

    res = f"Task created!\n" \
          f"Task id: <code>{task_id}</code>\n" \
          f"Name: {name}\n" \
          f"Creator Telegram username: {creator_username}\n" \
          f"Task description: {description}\n" \
          f"Deadline: {date_time_deadline}\n" \
          f"Reward: {reward/1e18} ETH\n\n" \
          + disclaimer + "\n#task"
    await _bot.send_message(chat_id, res, parse_mode="HTML")
    await _bot.session.close()


def handle_solution_proposed(event):
    # event attr: address comToken, uint256 taskId,  uint256 solId, uint256 solver, string solutionLink
    print("solution_proposed")
    print("Event: ", event)
    data = Web3.toBytes(hexstr=event['data'])
    decoded = eth_abi.decode_abi(['address', 'uint256', 'uint256', 'uint256', 'string'], data)
    print("\ndecoded args: ", decoded)
    com_tok = w3.toChecksumAddress(decoded[0])
    task_id = decoded[1]
    sol_id = decoded[2]
    solver = decoded[3]
    sol_descr = decoded[4]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        send_solution_created(com_tok, task_id, sol_id, solver, sol_descr)
    )
    #loop.close()


async def send_solution_created(com_tok, task_id, sol_id, solver, sol_descr):
    chat_id = await helpers.get_chat_id_by_token(com_tok)
    print("get_chat_id_by_token: ", chat_id)
    _bot = Bot(token=constants.API_TOKEN)
    try:
        solver = await _bot.get_chat_member(chat_id, solver)
        solver_username = solver.user.mention
    except Exception as e:
        solver_username = f"Creator left the chat. Creator Telegram ID: {solver}"
    res = f"Solution proposed on Task with id = <code>{task_id}</code>!\n" \
          f"Solution id: <code>{sol_id}</code>\n" \
          f"Solver username: {solver_username}\n" \
          f"Solution description: {sol_descr}\n" \
          f"#solution"
    await _bot.send_message(chat_id, res, parse_mode="HTML")
    await _bot.session.close()


def handle_task_voting_started(event):
    # event args: uint256 comId, address token, uint256 taskId, uint256 votingId,
    # string description, uint256 numberOfChoices, uint256 reward, uint256 deadline)
    # _comId, token, _taskId, votingId, description, numberOfChoices, reward, deadline
    print("task_voting_started")
    data = Web3.toBytes(hexstr=event['data'])
    decoded = eth_abi.decode_abi(['uint256', 'address', 'uint256', 'uint256', 'string', 'uint256', 'uint256', 'uint256'], data)
    print("\ndecoded args: ", decoded)
    ctr_com_id = decoded[0]
    com_tok = w3.toChecksumAddress(decoded[1])
    task_id = decoded[2]
    voting_id = decoded[3]
    # description = decoded[4]
    # numberOfChoices = decoded[5]
    voting_deadline_ts = decoded[7]
    voting_deadline_dt = time.strftime("%a, %d %b %Y %H:%M:%S MSK", time.localtime(voting_deadline_ts))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        send_task_voting_started(ctr_com_id, com_tok, task_id, voting_id, voting_deadline_dt)
    )
    loop.close()


async def send_task_voting_started(ctr_com_id, com_tok, task_id, voting_id, voting_deadline):
    _bot = Bot(token=constants.API_TOKEN)
    chat_id = await helpers.get_chat_id_by_token(com_tok)
    await _bot.send_message(chat_id, f"Voting on Task with ID = <code>{task_id}</code> started!\n"
                                           f"Voting deadline: {voting_deadline}\n"
                                           f"Voting ID: <code>{voting_id}</code>\n"
                                           f"#task_voting", parse_mode="HTML")
    await contracts_reader.get_task(_bot, ctr_com_id, chat_id, task_id)
    await _bot.session.close()



def handle_voting_started(event):
    # ProposalCreated (address comToken, uint256 proposalId, uint256 creator,
    # string proposal, uint256 numberOfOptions, uint256 deadline
    print(Web3.toJSON(event))
    print("voting_started")
    data = Web3.toBytes(hexstr=event['data'])
    decoded = eth_abi.decode_abi(['address', 'uint256', 'uint256', 'string', 'uint256', 'uint256'], data)
    print("\ndecoded args: ", decoded)
    com_tok = w3.toChecksumAddress(decoded[0])
    voting_id = decoded[1]
    creator_tg_id = decoded[2]
    description = decoded[3]
    number_of_options = decoded[4]
    deadline_ts = decoded[5]
    date_time_deadline = time.strftime("%a, %d %b %Y %H:%M:%S MSK", time.localtime(deadline_ts))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        send_voting_started(com_tok, voting_id, number_of_options, creator_tg_id, description, date_time_deadline)
    )
    loop.close()


async def send_voting_started(com_tok, voting_id, number_of_options, creator_tg_id, description, date_time_deadline):
    chat_id = await helpers.get_chat_id_by_token(com_tok)
    disclaimer = "The description of the voting proposal and it's options must be presented in the description of " \
                 "the task by its creator.\n" \
                 f"To vote for an option, use \n<code>/vote {com_tok} {voting_id} option_id</code>\ncommand in direct " \
                 f"messages with bot.\n" \
                 f"IDs of options - from 1 to {number_of_options}."
    _bot = Bot(token=constants.API_TOKEN)
    try:
        creator = await _bot.get_chat_member(chat_id, creator_tg_id)
        creator_username = creator.user.mention
    except Exception as e:
        creator_username = f"Creator left the chat. Creator Telegram ID: <code>{creator_tg_id}</code>"
    time.sleep(2)
    await _bot.send_message(chat_id, f"Voting with ID = <code>{voting_id}</code> created!\n"
                                           f"Creator: {creator_username}\n"
                                           f"Description: {description}\n"
                                           f"Number of options: {number_of_options}\n"
                                           f"Voting deadline: {date_time_deadline}\n" + disclaimer +
                                  f"\n#voting", parse_mode="HTML")
    await _bot.session.close()


def handle_mem_voted(event):
    # event args: MemberVoted(_comId, _propId, member_id)
    print("mem_voted")
    data = Web3.toBytes(hexstr=event['data'])
    decoded = eth_abi.decode_abi(['uint256', 'uint256', 'uint256'], data)
    print("\ndecoded args: ", decoded)
    #ctr_com_id = decoded[0]
    voting_id = decoded[1]
    mem_id = decoded[2]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        send_mem_voted(voting_id, mem_id)
    )


async def send_mem_voted(voting_id, mem_id):
    _bot = Bot(token=constants.API_TOKEN)
    await _bot.send_message(mem_id, f"Your vote is accepted! \n(Voting with ID = {voting_id})\n#voting")
    await _bot.session.close()


def handle_voting_results_counted(event):
    # get_voting
    # winning option id, it's description should be in description
    # event args: ProposalExecuted(address comToken, uint256 proposalId, uint256[] winningOptions)
    print("voting_results_counted")
    data = Web3.toBytes(hexstr=event['data'])
    decoded = eth_abi.decode_abi(['address', 'uint256', 'uint256[]'], data)
    print("\ndecoded args: ", decoded)
    com_tok = w3.toChecksumAddress(decoded[0])
    voting_id = decoded[1]
    winning_options = decoded[2]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        send_voting_results_counted(com_tok, voting_id, winning_options)
    )
    loop.close()


async def send_voting_results_counted(com_tok, voting_id, winning_options):
    _bot = Bot(token=constants.API_TOKEN)
    chat_id = await helpers.get_chat_id_by_token(com_tok)
    #l = len(winning_options)
    #options = ""
    #for i in range(l):
    #    options += f"[{winning_options[i]}]  "

    ctr_com_id = await contracts_reader.get_ctr_com_id_by_token(com_tok)
    voting = await contracts_reader.get_voting(_bot, ctr_com_id, chat_id, voting_id)

    await _bot.send_message(chat_id, f"The voting results have been summed up!\n" +
                                     f"{voting}\n#voting", parse_mode="HTML")
    await _bot.session.close()


def handle_task_voting_counted(event):
    # winning solution id
    # get its description and creator
    # event args: ResultsCounted(_comId, token, _taskId)
    print("task_voting_counted")
    data = Web3.toBytes(hexstr=event['data'])
    decoded = eth_abi.decode_abi(['uint256', 'address', 'uint256'], data)
    print("\ndecoded args: ", decoded)
    ctr_com_id = decoded[0] # todo test
    com_tok = w3.toChecksumAddress(decoded[1])
    task_id = decoded[2]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        send_task_voting_results_counted(ctr_com_id, com_tok, task_id)
    )
    #loop.close()


async def send_task_voting_results_counted(ctr_com_id, com_tok, task_id):
    _bot = Bot(token=constants.API_TOKEN)
    chat_id = await helpers.get_chat_id_by_token(com_tok)
    voting_id = await contracts_reader.get_voting_by_task_id(ctr_com_id, task_id)
    winning_solutions = await contracts_reader.get_voting_winning_options(ctr_com_id, voting_id)

    l = len(winning_solutions)
    solutions = ""
    for i in range(l):
        solution = await contracts_reader.get_solution(ctr_com_id, task_id, winning_solutions[i])
        solutions += f"\n{solution}  \n\n"

    if l == 0:
        await _bot.send_message(chat_id, f"The results of the voting on the task with id = <code>{task_id}</code> have been "
                                      f"calculated.\nBut none of the options received enough votes (threshold)",
                                      parse_mode="HTML")
    else:
        notification = f"\nTo reward solvers, use <code>/reward_solvers {task_id}</code> command."
        await _bot.send_message(chat_id, f"The results of the voting on the task with id = <code>{task_id}</code> have been "
                                           f"calculated!\n\nWinning solutions: {solutions}\n" 
                                           f"To get task description, use <code>/get_task {task_id}</code>\n" + notification +
                                           f"\n#task_voting", parse_mode="HTML")
    await _bot.session.close()


def handle_task_rewarded(event):
    # rewards sent to winners
    # event: TaskClosed(_comToken, _taskId)
    print("task_rewarded")
    print("Event: ", event)
    data = Web3.toBytes(hexstr=event['data'])
    decoded = eth_abi.decode_abi(['address', 'uint256'], data)
    print("\ndecoded args: ", decoded)
    com_tok = w3.toChecksumAddress(decoded[0])
    task_id = decoded[1]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        send_rewarded(com_tok, task_id)
    )
    #loop.close()


async def send_rewarded(com_tok, task_id):
    _bot = Bot(token=constants.API_TOKEN)
    chat_id = await helpers.get_chat_id_by_token(com_tok)
    await _bot.send_message(chat_id, f"The solver(s) of the task with id = <code>{task_id}</code> were rewarded!",
                            parse_mode="HTML")
    await _bot.session.close()


def handle_mem_verified(event):
    # event: TaskClosed(_comToken, _taskId)
    print("mem_verified")
    print("Event: ", event)
    data = Web3.toBytes(hexstr=event['data'])
    decoded = eth_abi.decode_abi(['uint256', 'uint256'], data)
    print("\ndecoded args: ", decoded)
    #ctr_com_id = decoded[0]
    member_id = decoded[1]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        send_mem_verified(member_id)
    )


async def send_mem_verified(member_id):
    _bot = Bot(token=constants.API_TOKEN)
    await _bot.send_message(member_id, "Congratulations, you have been verified by a sufficient number of "
                                             "community members. Now you are a verified member and can participate in "
                                             "voting, as well as create and solve tasks.")
    await _bot.session.close()


def handle_verification_accepted(event):
    print("verification_accepted")
    print("Event: ", event)
    data = Web3.toBytes(hexstr=event['data'])
    decoded = eth_abi.decode_abi(['uint256', 'uint256', 'uint256'], data)
    print("\ndecoded args: ", decoded)
    # ctr_com_id = decoded[0]
    sender_id = decoded[1]
    new_mem_id = decoded[2]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        send_verification_accepted(sender_id, new_mem_id)
    )


async def send_verification_accepted(sender_id, new_mem_id):
    _bot = Bot(token=constants.API_TOKEN)
    await _bot.send_message(sender_id, f"Your verification of {new_mem_id} member accepted!")
    await _bot.session.close()


def handle_member_created(event):
    # event args: address _member, _tgID, comToken, ctr_com_id
    # MemberCreated(address _member, uint256 _tgID, address comToken, uint256 _comId)
    print("handle_member_created")
    print("Event: ", event)
    data = Web3.toBytes(hexstr=event['data'])
    decoded = eth_abi.decode_abi(['address', 'uint256', 'address', 'uint256'], data)
    print("\ndecoded args: ", decoded)

    user_tg_id = decoded[1]
    com_tok = w3.toChecksumAddress(decoded[2])
    user_addr = w3.toChecksumAddress(decoded[0])

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        send_join_link(user_tg_id, com_tok, user_addr)
    )
    #loop.close()


async def send_join_link(user_id, com_tok, user_addr):
    _bot = Bot(token=constants.API_TOKEN)
    chat_id = await helpers.get_chat_id_by_token(com_tok)
    expire_date = datetime.now() + timedelta(minutes=2)
    link = await _bot.create_chat_invite_link(chat_id, expire_date, 1)
    await _bot.send_message(user_id,
                                  f"The check has been successfully passed!\nYou're registered with \n"
                                  f"Telegram ID: <code>{user_id}</code>\n"
                                  f"Address: <code>{user_addr}</code>\n"
                                  f"This is your link to join the chat:"
                                  f"{link.invite_link} \nBe careful: the link will expire in two minutes.\n\n"
                                  f"Note: in order to participate in votng, create and solve tasks, you need to get "
                                  f"verification from other, already verified community members. In addition, if your "
                                  f"community token balance becomes less than threshold, you will be removed from the chat.",
                                  parse_mode="HTML")
    await _bot.session.close()


def handle_member_deleted(event):
    # kick from group
    # event args: tg_id, member_address, com_tok, ctr_com_id
    print("Event: ", event)
    data = Web3.toBytes(hexstr=event['data'])
    decoded = eth_abi.decode_abi(['uint256', 'address', 'address', 'uint256'], data)
    print("\ndecoded args: ", decoded)
    member_tg_id = decoded[0]
    member_address = w3.toChecksumAddress(decoded[1])
    com_tok = w3.toChecksumAddress(decoded[2])

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        kick(com_tok, member_tg_id, member_address)
    )
    #loop.close()


async def kick(com_tok, member_tg_id, member_address):
    _bot = Bot(token=constants.API_TOKEN)
    chat_id = await helpers.get_chat_id_by_token(com_tok)
    try:
        member = await _bot.get_chat_member(chat_id, member_tg_id)
        member_username = "@" + member.user.username
    except Exception as e:
        member_username = f"with TgID = {member_tg_id}"
    try:
        await _bot.kick_chat_member(chat_id, member_tg_id)
    except Exception as e:
        await _bot.send_message(chat_id,
                           f"The user {member_username} lost membership because the balance of community "
                           f"tokens on his address (<code>{member_address}</code>) is less than the threshold.")
        return
    await _bot.send_message(chat_id, f"The user {member_username} was kicked out of the chat because the balance of "
                                     f"community tokens on his address (<code>{member_address}</code>) is less than the"
                                     f" threshold.", parse_mode="HTML")
    await _bot.send_message(member_tg_id, "You were kicked from the community chat because the balance of "
                                                f"community tokens on address (<code>{member_address}</code>) "
                                                f"became less than the threshold.", parse_mode="HTML")
    await _bot.session.close()


def handle_com_created(event):
    # write to com owner
    # event args: CommunityCreated(comId, comWallet, mainToken, creatorTgID, msg.sender)
    print("com_created")
    data = Web3.toBytes(hexstr=event['data'])
    decoded = eth_abi.decode_abi(['uint256', 'address', 'address', 'uint256', 'address'], data)
    print("\ndecoded args: ", decoded)
    ctr_com_id = decoded[0]
    community_wallet = decoded[1]
    com_tok = w3.toChecksumAddress(decoded[2])
    creator_tg_id = decoded[3]
    creator_address = decoded[4]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        send_com_created(ctr_com_id, community_wallet, com_tok, creator_tg_id, creator_address)
    )
    #loop.close()


async def send_com_created(ctr_com_id, community_wallet, com_tok, creator_tg_id, creator_address):
    _bot = Bot(token=constants.API_TOKEN)
    await _bot.send_message(creator_tg_id,
                                  f"The community created successfully\!\nYou're registered as it's creator and a "
                                  f"verified member\. Now you can create a chat for your community, add bot to the chat "
                                  f"and use \n`/add\_community\_token {com_tok}`\n to enable the verification of new participants"
                                  f" for the presence of a token and use the rest of the bot's functionality\. \n\n"
                                  f"You're registered as member with the following parameters:\n"
                                  f"Telegram ID: {creator_tg_id}\n"
                                  f"Address: `{creator_address}`\n\n"
                                  f"Community parameters:\n"
                                  f"Main community token: `{com_tok}`\n"
                                  f"Community wallet: `{community_wallet}`\n"
                                  f"Community ID \(in contracts\): `{ctr_com_id}`\n\n"
                                  f"\nNotice: you need to verify new members after they're getting some community tokens"
                                  f" and joining community chat\. In addition, if their community token balance becomes "
                                  f"less than threshold, they will be removed from the chat\.", parse_mode="MarkdownV2")
    await _bot.session.close()


def handle_event2(event):
    print("Event: ", event)
    data = Web3.toBytes(hexstr=event['data'])
    decoded = eth_abi.decode_abi(['string', 'uint256'], data)
    print("\ndecoded args: ", decoded)


def switch_events(marker, event):
    match marker:
        case 0:
            handle_task_created(event)
        case 1:
            handle_solution_proposed(event)
        case 2:
            handle_task_voting_started(event)
        case 3:
            handle_voting_started(event)
        case 4:
            handle_voting_results_counted(event)
        case 5:
            handle_task_voting_counted(event)
        case 6:
            handle_task_rewarded(event)
        case 7:
            handle_member_created(event)
        case 8:
            handle_member_deleted(event)
        case 9:
            handle_com_created(event)
        case 10:
            handle_mem_voted(event)
        case 11:
            handle_mem_verified(event)
        case 12:
            handle_verification_accepted(event)

        case _:
            print(f'Something\'s wrong, I can feel it\n'
                  f'Event: {event}')


def log_loop(event_filter, poll_interval, marker):
    while True:
        for event in event_filter.get_new_entries():
            switch_events(marker, event)
            print(marker)
            print('\n')
        time.sleep(poll_interval)
