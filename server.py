import platform
import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ChatType, ContentType, Message
from aiogram.utils.deep_linking import get_start_link, decode_payload
from aiogram.utils.markdown import hlink
from web3 import Web3

import constants
from constants import w3
import contracts_reader
import helpers
import event_handlers
from welcome import welcome_text
from threading import Thread

logging.basicConfig(level=logging.INFO)
bot = Bot(token=constants.API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
client_loop = dp.loop


@dp.message_handler(commands=['start', 'help'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP, ChatType.PRIVATE])
async def send_welcome(message: types.Message):
    """Sends welcome/help msg and handles join & mint deeplinks"""

    args = message.get_args()
    print("args:")
    print(args)
    payload = decode_payload(args).split(" ")
    print("payload:")
    print(payload)
    if payload[0] == '':
        await bot.send_message(
            chat_id=message.chat.id,
            text=welcome_text,
            parse_mode="HTML"
        )
        return

    # /mint and /join_group deeplinks:
    if len(payload) == 3:
        print("len payload == 3")
        if payload[0] == "m":
            msg = f"/mint_tokens {payload[1]} {payload[2]}"
            print("throwing to mint_tokens")
            msg1 = message
            msg1.text = msg
            await mint_tokens(msg1)
            return

    if len(payload) == 2:
        if payload[0] == "j":
            msg = f"/join_group {payload[1]}"
            print("throwing to join_group_by_token")
            msg1 = message
            msg1.text = msg
            await join_group_by_token(msg1)
            return


@dp.message_handler(commands=['create_community_with_token'], chat_type=ChatType.PRIVATE)
async def create_community_with_token(
        message: Message):
    """Returns a link to sign the transaction of community+token creation with given params
         in the MetaMask extension"""
    # params: name, symbol, price, (creator.id)
    print("started create")
    if not message.chat.type == ChatType.PRIVATE:
        await bot.send_message(message.chat.id, "This command can only be used in direct messages with bot.")
        return

    params = str.split(message.text, ' ')
    if len(params) != 5:
        await bot.send_message(message.from_user.id, "Invalid number of arguments.")
    else:

        if not (await helpers.check_string(params[1]) and (await helpers.check_string(params[2]))):
            await bot.send_message(message.from_user.id, "Wrong arguments: Token name and symbol should contain "
                                                         "latin letters, numbers and underscore characters only")
        else:
            is_price = await helpers.is_float(params[3])
            if is_price:
                _name = params[1]
                _symbol = params[2]
                _price = params[3]
                _com_wallet = params[4]
                _tg_id = message.from_user.id
                link = await helpers.get_create_community_with_token_link(_name, _symbol, _price, _com_wallet, _tg_id)
                answer_message = hlink(f'Tap to sign the {_name} ({_symbol}) token creation transaction for your community.\n'
                                       f'Starting {_symbol} price will be set to {_price} native tokens of the network',
                                       link)
                await bot.send_message(message.from_user.id, answer_message)
            else:
                await bot.send_message(message.from_user.id, "Wrong arguments: price should be a number")


@dp.message_handler(commands=['create_community_custom_token'], chat_type=ChatType.PRIVATE)
async def create_community_with_custom_token(
        message: Message):
    """Returns a link to sign the transaction of community+token creation with given params
         in the MetaMask extension"""
    # params: name, symbol, price, (creator.id)
    print("started create with custom")
    params = str.split(message.text, ' ')
    if len(params) != 3:
        await bot.send_message(message.from_user.id, "Invalid number of arguments.")
    else:
        if not (await helpers.is_address(params[1]) and (await helpers.is_address(params[2]))):
            await bot.send_message(message.from_user.id, "Wrong arguments: Wallet address and token address should be "
                                                         "valid blockchain addresses")
            return
        com_wallet = params[1]
        com_tok = params[2]
        _tg_id = message.from_user.id
        link = await helpers.get_create_community_with_custom(com_tok, com_wallet, _tg_id)
        answer_message = hlink(f'Tap to sign the community creation transaction.\n'
                               f'Please note that the system may work differently with your token\'s custom '
                               f'implementation.', link)
        await bot.send_message(message.from_user.id, answer_message)


@dp.message_handler(commands=['mint_tokens'], chat_type=ChatType.PRIVATE)
async def mint_tokens(message: Message):
    """Returns a link to sign the transaction of token mint with given params
        in the MetaMask extension"""
    # params: token_address, amount
    print("mint_tokens")
    print("params:" + message.text)

    params = str.split(message.text, ' ')
    print(len(params))
    if len(params) != 3:
        await bot.send_message(message.from_user.id, "Invalid number of arguments.")
    else:
        is_addr = False
        try:
            is_addr = await helpers.is_address(params[1])
        except Exception as e:
            await bot.send_message(message.from_user.id, "Wrong address: " + e.args[0])

        if is_addr:
            if await helpers.is_float(params[2]):
                _token_address = params[1]
                _amount = params[2]

                is_int = await helpers.is_int(_amount)
                if not is_int:
                    await bot.send_message(message.from_user.id, "The amount of tokens should be an integer number.")
                    return

                link = await helpers.get_mint_token_link(_token_address, _amount)

                answer_message = hlink(f'Tap to mint {_amount} tokens of {_token_address} token contract', link)

                await bot.send_message(message.from_user.id, answer_message)
            else:
                await bot.send_message(message.from_user.id, "Wrong amount: amount should be a number.")


@dp.message_handler(commands=['change_token_price'], chat_type=ChatType.PRIVATE)
async def change_token_price(message: Message):  # todo only INTEGERS
    """Returns a link to sign the transaction of token mint with given params
        in the MetaMask extension"""
    # params: token_address, amount
    params = str.split(message.text, ' ')
    print("change_price")
    if len(params) != 3:
        await bot.send_message(message.from_user.id, "Invalid number of arguments")
        print("len")
        return

    try:
        is_addr = await helpers.is_address(params[1])
        _token_address = w3.toChecksumAddress(params[1])
    except Exception as e:
        await bot.send_message(message.from_user.id, "Invalid address")
        return

    if is_addr:
        flt = await helpers.is_float(params[2])
        if not flt:
            await bot.send_message(message.from_user.id, f"Price should be a number")
            return

        _new_price = params[2]

        if not (await contracts_reader.com_exists(_token_address)):
            await bot.send_message(message.from_user.id, f"A community with the {_token_address} token does not exist.")
            return

        link = await helpers.get_change_price_link(_token_address, _new_price)

        answer_message = hlink(f'Tap to sign the transaction to change the price of the {_token_address} token '
                                   f'to {_new_price}', link)

        await bot.send_message(message.from_user.id, answer_message)



@dp.message_handler(commands=['add_community_token'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def add_community_token(message: Message):  # TODO set created community with token
    """
    This handler will add address of the token to db in association with chat_id
    """
    # params: token_address
    params = str.split(message.text, ' ')
    print("add_group_token")
    if len(params) != 2:
        await bot.send_message(message.chat.id, "Invalid number of arguments.")
        return

    chat = message.chat.id
    token_addr = params[1]
    print("token addr params:", token_addr)
    if await helpers.check_group_token_exists_by_id(chat):
        await bot.send_message(chat, "Main token is already set  for your community")
        return

    try:
        is_addr = await helpers.is_address(token_addr)  # todo to checksum
    except Exception as e:
        await bot.send_message(chat, "Wrong address: " + e.args[0])
        return

    if is_addr:
        token_addr = w3.toChecksumAddress(token_addr)
        print("token to checksum:", token_addr)
        caller = await bot.get_chat_member(chat, message.from_user.id)
        is_admin = caller.is_chat_admin() or caller.is_chat_owner()

        # check that community with this token address exists [contracts]
        if not (await contracts_reader.com_exists(token_addr)):
            await bot.send_message(chat, f"A community with the {token_addr} token does not exist.\nUse "
                                         f"/create_community_custom_token in DM with bot to create new community with"
                                         f" custom token and then try again.")
            return

        if not (is_admin and (await contracts_reader.is_com_owner(token_addr, message.from_user.id))):
            await bot.send_message(chat, "Only the chat administrator and community owner can set the token")
        else:
            inserted = await helpers.add_community_token(token_addr, chat)
            await bot.send_message(chat, f"A community token with the address `{inserted}` "
                                         f"is set for this group", parse_mode="MarkdownV2")


@dp.message_handler(commands=['delete_community_token'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def delete_comm_token(message: Message):  # TODO remove created community with token from the chat (DB)
    params = str.split(message.text, ' ')
    print("delete_token")
    if len(params) != 1:
        await bot.send_message(message.chat.id, "Invalid number of arguments.")
        print("len")
    else:
        chat = message.chat.id
        caller = await bot.get_chat_member(chat, message.from_user.id)
        is_admin = caller.is_chat_admin() or caller.is_chat_owner()

        if not is_admin:
            await bot.send_message(chat, "Only the chat administrator or owner can delete community token")
        else:
            # check if community actually has a token
            if not await helpers.check_group_token_exists_by_id(chat):
                await bot.send_message(chat, "Token is not set  for your community")
            else:
                delete = await helpers.delete_group_token(chat)
                await bot.send_message(chat, "Community token was successfully deleted")


@dp.message_handler(commands=['get_community_token_address'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def get_token(message: Message):
    params = str.split(message.text, ' ')
    print("get_token")
    if len(params) != 1:
        await bot.send_message(message.chat.id, "Invalid number of arguments.")
        print(len(params))
    else:
        chat = message.chat.id
        if not await helpers.check_group_token_exists_by_id(chat):
            await bot.send_message(chat, "Token is not set for your community")
        else:
            group_token = await helpers.get_group_token(chat)
            await bot.send_message(chat, f"Your community token address: `{group_token}`", parse_mode="MarkdownV2")


@dp.message_handler(commands=['join_group'], chat_type=ChatType.PRIVATE)
async def join_group_by_token(message: Message):
    # params: main_com_token
    # todo check if you are a member or creating a member if you have enough tokens

    params = str.split(message.text, ' ')
    print("join_group")
    user_id = message.from_user.id
    if len(params) != 2:
        await bot.send_message(user_id, "Invalid number of arguments.")
        return

    try:
        is_addr = await helpers.is_address(params[1])
        com_tok = params[1]
    except Exception as e:
        await bot.send_message(user_id, "Wrong address: " + e.args[0])
        return

    if not is_addr:
        await bot.send_message(user_id, "Address is not valid")
        return

    if com_tok == constants.ZERO_ADDRESS:
        await bot.send_message(user_id, f"_Please use the main community token address instead of zero address\._",
                               parse_mode="MarkdownV2")
        return

    # todo check if bot has this group in db and return chat_id if it does
    chat_id = await helpers.get_chat_id_by_token(com_tok)
    print(f"chat id: {chat_id}")

    if chat_id == -1:
        await bot.send_message(user_id, "Chat with this token is not registered.")
        return

    member = await bot.get_chat_member(chat_id, user_id)

    if not (member.status == "left"):
        print(member)
        # chat = await bot.get_chat(chat_id)
        # print(chat)
        await bot.send_message(user_id, "You are already a member of this group")
        return
    print("is not member")

    # get _comId[contracts] by token
    ctr_com_id = await contracts_reader.get_ctr_com_id_by_token(com_tok)
    # check if member already exist in contracts
    already_a_member = await contracts_reader.is_member(ctr_com_id, user_id)
    if already_a_member:
        expire_date = datetime.now() + timedelta(minutes=2)
        link = await bot.create_chat_invite_link(chat_id, expire_date, 1)
        await bot.send_message(user_id,
                               f"The check has been successfully passed!\n This is your link to join the group:"
                               f"{link.invite_link} \n\nBe careful: the link will expire in two minutes.",
                               parse_mode="HTML")
    else:
        link = await helpers.get_create_member_link(ctr_com_id, user_id)  # todo create member[contracts-site]
        answer_message = hlink(f'In order to link your blockchain address to your Telegram account and to confirm that you have enough tokens'
                               f' to participate, please tap this text to sign the confirmation. \n', link)
        await bot.send_message(user_id, answer_message)


@dp.message_handler(content_types=ContentType.NEW_CHAT_MEMBERS)
async def check_new_member(message: Message):  # todo check in contracts that he is registered when he join chat (check_new_member)
    print("check_new_member")
    new_member = message.new_chat_members[0]
    print(1)
    if not await helpers.check_group_token_exists_by_id(message.chat.id):
        await bot.send_message(message.chat.id, "Token is not set for your community. Can't check new member.")
        return
    com_tok = await helpers.get_group_token(message.chat.id)
    print("com tok from db: ", com_tok[1])
    com_tok = w3.toChecksumAddress(com_tok)
    print("to checksum: ", com_tok)
    ctr_com_id = await contracts_reader.get_ctr_com_id_by_token(com_tok) #here
    is_member = await contracts_reader.is_member(ctr_com_id, new_member.id)
    print(2)
    if not is_member:
        f_name = await bot.get_chat_member(message.chat.id, new_member.id)
        f_name = f_name.user.full_name
        await bot.kick_chat_member(message.chat.id, new_member.id)
        await bot.send_message(message.chat.id, f"{f_name} was removed from the chat due to the fact that it was not a "
                                                f"member of the community.")
    else:
        verify_command = f"<code>/verify_member {com_tok} {new_member.id}</code>"
        await bot.send_message(message.chat.id,
                               f"Member allowed. Welcome {new_member.get_mention()}!\n Please, don't forget to verify "
                               f"new member using <code>{verify_command}</code> in dm with bot. Otherwise, {new_member.first_name}"
                               f" will not be able to vote, create tasks, and so on. \n(Or don't confirm if it's an"
                               f" impostor.)", parse_mode="HTML")


@dp.message_handler(commands=['verify_member'], chat_type=[ChatType.PRIVATE])
async def verify_member(message: Message):
    # TODO stopped here
    # todo parse args: _com_id, user_id - are integers
    params = str.split(message.text, ' ')
    print("verify_member")
    user_id = message.from_user.id
    if len(params) != 3:
        await bot.send_message(user_id, "Invalid number of arguments.")
        return

    try:
        is_addr = await helpers.is_address(params[1])
        com_tok = params[1]
    except Exception as e:
        await bot.send_message(user_id, "Invalid address")
        return

    if not is_addr:
        await bot.send_message(user_id, "Address is not valid")
        return

    if not await helpers.check_group_token_exists(com_tok):
        await bot.send_message(message.from_user.id, "There's no registered community chats with this token.")
        return

    try:
        new_member_id = int(params[2])
        is_int = new_member_id == params[2]
    except Exception as e:
        await bot.send_message(user_id, "Wrong user id: " + e.args[0])
        return

    chat_id = await helpers.get_chat_id_by_token(com_tok)
    if chat_id == -1:
        await bot.send_message(message.from_user.id, "Invalid token address.")
        return

    # check new_member exists in the community chat
    try:
        new_member = await bot.get_chat_member(chat_id, new_member_id)
    except Exception as e:
        await bot.send_message(user_id, "The user is not in the community chat: " + e.args[0])
        return

    new_member_username = new_member.user.username
    new_member_name = new_member.user.full_name

    ctr_com_id = await contracts_reader.get_ctr_com_id_by_token(com_tok)
    link = await helpers.get_verify_member_link(ctr_com_id, new_member_id)
    answer_message = hlink(f'Please, make sure that {new_member_username} with Telegram ID = {new_member_id} is a '
                           f'trusted community member. \nIf {new_member_name} '
                           f'won\'t get threshold of verifications, he will not be allowed to vote, create and solve '
                           f'tasks, etc.\nTap this text to give your verification.', link)
    await bot.send_message(message.chat.id, answer_message)


@dp.message_handler(commands=['get_mint_deeplink'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def get_mint_deeplink(message: types.Message):
    params = str.split(message.text, ' ')
    print("get_mint_deeplink")
    if len(params) != 2:
        await bot.send_message(message.chat.id, "Invalid number of arguments.")
        return

    if not await helpers.check_group_token_exists_by_id(message.chat.id):
        await bot.send_message(message.chat.id, "Token is not set for your community")
        return
    try:
        token_address = await helpers.get_group_token(message.chat.id)
    except:
        await bot.send_message(message.chat.id, "Invalid arguments.")
        return

    link = await get_start_link(f"m {token_address} {params[1]}", encode=True)
    await bot.send_message(message.chat.id, "Send this deeplink to invite people to mint your token: \n" + link)
    return


@dp.message_handler(commands=['get_join_deeplink'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def get_join_deeplink(message: types.Message):
    params = str.split(message.text, ' ')
    print("join_group")
    if len(params) != 1:
        await bot.send_message(message.chat.id, "Invalid number of arguments.")
        return

    print("get_join_deeplink")
    # check bot is admin
    bt = await bot.get_chat_member(message.chat.id, bot.id)
    is_admin = bt.is_chat_admin()
    if not is_admin:
        await bot.send_message(message.chat.id, "Please, promote me to admin. I need permission to invite users "
                                                "to create this deeplink.")
        return
    if not bt['can_invite_users']:
        await bot.send_message(message.chat.id, "Please, give me a permission to invite users.\n"
                                                "Otherwise I won't be able to create a link to join the chat.")
        return
    params = str.split(message.text, ' ')

    if len(params) != 1:
        await bot.send_message(message.chat.id, "Invalid number of arguments.")
        return

    # check that chat has a comm token
    if not await helpers.check_group_token_exists_by_id(message.chat.id):
        await bot.send_message(message.chat.id, "Token is not set for your community")
        return

    token_address = await helpers.get_group_token(message.chat.id)

    link = await get_start_link(f"j {token_address}", encode=True)
    await bot.send_message(message.chat.id, "Send this link to invite the user to pass a token check "
                                            "and join this chat: \n" + link)
    return


@dp.message_handler(commands=['create_task'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def create_task(message: types.Message):
    # [contracts] Backlog.createTask: _communityId, uint _deadline, uint _reward
    # _name, _description, - SITE
    # args: com_token, task_name, task_description, deadline for solution proposals, reward

    params = str.split(message.text, ' ')
    print("create_task")
    if len(params) != 3:
        await bot.send_message(message.chat.id, "Invalid number of arguments.")
        return
    deadline = params[1]  # uint (hours)
    reward = params[2]  # uint
    if not await helpers.check_group_token_exists_by_id(message.chat.id):
        await bot.send_message(message.chat.id, "Token is not set for your community")
        return
    com_token = await helpers.get_group_token(message.chat.id)
    com_token = Web3.toChecksumAddress(com_token)

    ctr_com_id = await contracts_reader.get_ctr_com_id_by_token(com_token)

    link = await helpers.get_link_to_create_task(ctr_com_id, deadline, reward)
    await bot.send_message(message.chat.id, "Use the following link to create a task (you can add link to the "
                                            "description on the site): \n" + link)


@dp.message_handler(commands=['create_voting'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def create_voting(message: types.Message):
    # [contracts] Voting.createProposal
    # _comId,
    # _proposal, - link field on the site
    # _numberOfOptions, _deadline, creator

    params = str.split(message.text, ' ')
    print("create_voting")
    if len(params) != 3:
        await bot.send_message(message.chat.id, "Invalid number of arguments.")
        return
    if not await helpers.check_group_token_exists_by_id(message.chat.id):
        await bot.send_message(message.chat.id, "Token is not set for your community")
        return
    com_token = await helpers.get_group_token(message.chat.id)
    com_token = Web3.toChecksumAddress(com_token)
    n_of_options = params[1]
    deadline = params[2]  # uint (hours)

    ctr_com_id = await contracts_reader.get_ctr_com_id_by_token(com_token)

    link = await helpers.get_create_voting_link(ctr_com_id, n_of_options, deadline)
    await bot.send_message(message.chat.id, "Use the following link to create a voting (you can add link to "
                                            "the voting options description on the site): \n" + link)


@dp.message_handler(commands=['propose_solution'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def propose_solution(message: types.Message):
    # [contracts] uint256 _comId, uint256 _taskId, string memory _solution - SITE
    params = str.split(message.text, ' ')
    print("propose_solution")
    if len(params) != 2:
        await bot.send_message(message.chat.id, "Invalid number of arguments.")
        return
    if not await helpers.check_group_token_exists_by_id(message.chat.id):
        await bot.send_message(message.chat.id, "Token is not set for your community")
        return
    com_token = await helpers.get_group_token(message.chat.id)
    com_token = Web3.toChecksumAddress(com_token)
    try:
        task_id = int(params[1])
        ctr_com_id = await contracts_reader.get_ctr_com_id_by_token(com_token)
        task_name = await contracts_reader.get_task_name(ctr_com_id, task_id)
        task_description = await contracts_reader.get_task_description(ctr_com_id, task_id)
    except Exception as e:
        await bot.send_message(message.chat.id, "Invalid task ID value")
        return

    link = await helpers.get_link_to_propose_solution(ctr_com_id, task_id)
    await bot.send_message(message.chat.id, f"To propose your solution for the {task_id} task with"
                                            f"\nTask name: {task_name} \n"
                                            f"Task description: {task_description}\n"
                                            "\nUse the following link (you can add link to the solution on the site): \n"
                           + link)


@dp.message_handler(commands=['start_voting_on_solutions'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def start_voting_on_solutions(message: types.Message):
    # [contracts] uint _taskId, uint _comId, uint256 _voteDeadline
    params = str.split(message.text, ' ')
    print("create_task")
    if len(params) != 3:
        await bot.send_message(message.chat.id, "Invalid number of arguments.")
        return

    if not await helpers.check_group_token_exists_by_id(message.chat.id):
        await bot.send_message(message.chat.id, "Token is not set for your community")
        return
    com_tok = await helpers.get_group_token(message.chat.id)
    com_tok = Web3.toChecksumAddress(com_tok)

    try:
        task_id = int(params[1])
        voting_deadline = int(params[2])  # uint (hours)
        ctr_com_id = await contracts_reader.get_ctr_com_id_by_token(com_tok)
        task_name = await contracts_reader.get_task_name(ctr_com_id, task_id)
    except Exception as e:
        await bot.send_message(message.chat.id, "Task ID and the deadline should be integer values. The deadline "
                                                "parameter should be an integer number of hours allocated for providing votes.")
        return

    task_description = await contracts_reader.get_task_description(ctr_com_id, task_id)
    number_of_solutions = await contracts_reader.get_number_of_solutions(ctr_com_id, task_id)

    voting_command = f"<code>/vote {com_tok} voting_id solution_id</code>"
    link = await helpers.get_start_task_voting_link(ctr_com_id, task_id, voting_deadline)
    await bot.send_message(message.chat.id, f"To start voting for a solution of <code>{task_id}</code> task with the "
                                            f"following parameters:\nTask name: {task_name}\n"
                                            f"Task description: {task_description}\n\n"
                                            f"Use the link: " + link +
                           f"\n\nUse {voting_command} in dm with bot to vote for one of "
                           f"{number_of_solutions} proposed solutions.", parse_mode="HTML")


@dp.message_handler(commands=['vote'], chat_type=[ChatType.PRIVATE])
async def vote(message: types.Message):  # both for tasks and votings (proposals)
    # Voting.vote [contracts]
    # uint256 _comId, uint256 _propId, uint256 _choice
    params = str.split(message.text, ' ')
    print("vote")
    if len(params) != 4:
        await bot.send_message(message.chat.id, "Invalid number of arguments.")
        return
    # TODO some checks

    try:
        com_tok = Web3.toChecksumAddress(params[1])
        voting_id = int(params[2])
        option = int(params[3])
        ctr_com_id = await contracts_reader.get_ctr_com_id_by_token(com_tok)
    except Exception as e:
        await bot.send_message(message.chat.id, "Invalid arguments")
        return

    # TODO GET VOTING BY ID

    link = await helpers.get_vote_link(ctr_com_id, voting_id, option)
    await bot.send_message(message.chat.id, f"Use the following link to vote for {option} option of {voting_id} "
                                            f"voting\n" + link)


@dp.message_handler(commands=['get_voting'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def get_voting(message: types.Message):
    params = str.split(message.text, ' ')
    print("get_voting")
    if len(params) != 2:
        await bot.send_message(message.chat.id, "Invalid number of arguments")
        return

    if not await helpers.check_group_token_exists_by_id(message.chat.id):
        await bot.send_message(message.chat.id, "Token is not set for your community")
        return
    com_tok = await helpers.get_group_token(message.chat.id)
    com_tok = Web3.toChecksumAddress(com_tok)

    try:
        voting_id = int(params[1])
        ctr_com_id = await contracts_reader.get_ctr_com_id_by_token(com_tok)
        chat_id = await helpers.get_chat_id_by_token(com_tok)
        voting = await contracts_reader.get_voting(bot, ctr_com_id, chat_id, voting_id)
    except Exception as e:
        await bot.send_message(message.chat.id, "Invalid voting ID")
        return

    await bot.send_message(message.chat.id, voting)


@dp.message_handler(commands=['get_solution'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def get_solution(message: types.Message):
    params = str.split(message.text, ' ')
    print("get_solution")
    if len(params) != 3:
        await bot.send_message(message.chat.id, "Invalid number of arguments.")
        return

    if not await helpers.check_group_token_exists_by_id(message.chat.id):
        await bot.send_message(message.chat.id, "Token is not set for your community")
        return
    com_tok = await helpers.get_group_token(message.chat.id)
    com_tok = Web3.toChecksumAddress(com_tok)

    try:
        task_id = int(params[1])
        sol_id = int(params[2])
    except Exception as e:
        await bot.send_message(message.chat.id, "Task and solution IDs should be integers.")
        return

    if sol_id == 0:
        await bot.send_message(message.chat.id, "Task IDs are integers from 1 to number of solutions.")
        return

    ctr_com_id = await contracts_reader.get_ctr_com_id_by_token(com_tok)

    sol = await contracts_reader.get_solution(ctr_com_id, task_id, sol_id)
    await bot.send_message(message.chat.id, sol)


@dp.message_handler(commands=['get_task'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def get_task(message: types.Message):
    params = str.split(message.text, ' ')
    print("get_task")
    if len(params) != 2:
        await bot.send_message(message.chat.id, "Invalid number of arguments.")
        return

    if not await helpers.check_group_token_exists_by_id(message.chat.id):
        await bot.send_message(message.chat.id, "Token is not set for your community")
        return
    com_tok = await helpers.get_group_token(message.chat.id)
    com_tok = Web3.toChecksumAddress(com_tok)

    try:
        task_id = int(params[1])
    except Exception as e:
        await bot.send_message(message.chat.id, "Task ID should be an integer.")
        return

    ctr_com_id = await contracts_reader.get_ctr_com_id_by_token(com_tok)

    tsk = await contracts_reader.get_task(bot, ctr_com_id, message.chat.id, task_id)
    await bot.send_message(message.chat.id, tsk)


@dp.message_handler(commands=['count_voting_results'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def count_voting_results(message: types.Message):
    # [contracts] Voting.executeVoting
    # uint256 _comId,
    # uint256 _proposalId
    params = str.split(message.text, ' ')
    print("count_voting_results")
    if len(params) != 2:
        await bot.send_message(message.chat.id, "Invalid number of arguments.")
        return

    if not await helpers.check_group_token_exists_by_id(message.chat.id):
        await bot.send_message(message.chat.id, "Token is not set for your community")
        return
    com_tok = await helpers.get_group_token(message.chat.id)
    com_tok = Web3.toChecksumAddress(com_tok)

    try:
        voting_id = int(params[1])
    except Exception as e:
        await bot.send_message(message.chat.id, "Voting ID should be an integer.")
        return

    ctr_com_id = await contracts_reader.get_ctr_com_id_by_token(com_tok)

    link = await helpers.get_voting_results_link(ctr_com_id, voting_id)
    await bot.send_message(message.chat.id, f"Use the following link to to summarize the voting results for "
                                            f"{voting_id} voting\n" + link)


@dp.message_handler(commands=['count_task_voting_results'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def get_winning_task_solutions(message: types.Message):
    # [contracts] Backlog.countResults
    # uint256 _comId, uint256 _taskId
    params = str.split(message.text, ' ')
    print("get_winning_task_solutions")
    if len(params) != 2:
        await bot.send_message(message.chat.id, "Invalid number of arguments.")
        return

    if not await helpers.check_group_token_exists_by_id(message.chat.id):
        await bot.send_message(message.chat.id, "Token is not set for your community")
        return
    com_tok = await helpers.get_group_token(message.chat.id)
    com_tok = Web3.toChecksumAddress(com_tok)

    try:
        task_id = int(params[1])
    except Exception as e:
        await bot.send_message(message.chat.id, "Invalid task ID")
        return

    ctr_com_id = await contracts_reader.get_ctr_com_id_by_token(com_tok)

    link = await helpers.get_task_results_link(ctr_com_id, task_id)
    await bot.send_message(message.chat.id, f"Use the following link to summarize the voting results for "
                                            f"{task_id} task.\n You can use /reward_solvers command after that.\n" + link)


@dp.message_handler(commands=['reward_solvers'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def reward_task_solvers(message: types.Message):
    # [contracts] Backlog.rewardSolversAndClose
    # uint256 _comId, uint256 _taskId
    params = str.split(message.text, ' ')
    print("reward_task_solvers")
    if len(params) != 2:
        await bot.send_message(message.chat.id, "Invalid number of arguments.")
        return
    if not await helpers.check_group_token_exists_by_id(message.chat.id):
        await bot.send_message(message.chat.id, "Token is not set for your community")
        return
    com_tok = await helpers.get_group_token(message.chat.id)
    com_tok = Web3.toChecksumAddress(com_tok)

    try:
        task_id = int(params[1])
    except Exception as e:
        await bot.send_message(message.chat.id, "Invalid task ID")
        return

    ctr_com_id = await contracts_reader.get_ctr_com_id_by_token(com_tok)

    link = await helpers.get_reward_link(ctr_com_id, task_id)
    await bot.send_message(message.chat.id, f"Use the following link to reward {task_id} task solvers: " + link)


async def start_polling():
    await dp.start_polling()


def main():
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    filters = constants.init()

    numb_of_filters = len(filters)
    print("nof: ", numb_of_filters)

    for i in range(numb_of_filters):
        print(f"worker {i} started")
        worker = Thread(target=event_handlers.log_loop, args=(filters[i], 5, i), daemon=True)
        worker.start()

    asyncio.run(start_polling())


if __name__ == '__main__':
    main()

# if __name__ == '__main__':
#    executor.start_polling(dp, skip_updates=True)
