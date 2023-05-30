import re

import constants
import db
from db import conn

BASE_URI = "http://127.0.0.1:3000/"

CREATE_COMMUNITY_WITH_TOKEN = "create_com_tok/"
CREATE_WITH_CUSTOM = "create_community/"
MINT_TOKEN = "mint_token/"
CHANGE_PRICE = "change_price/"
CREATE_MEMBER = "create_member/"
VERIFY_MEMBER = "verify_member/"
CREATE_TASK = "create_task/"
PROPOSE_SOLUTION = "propose_solution/"
START_VOTING_ON_TASK = "start_task_voting/"
CREATE_VOTING = "create_voting/"
VOTE = "vote/"
VOTING_RESULTS = "voting_res/"
TASK_RESULTS = "task_res/"
REWARD = "reward/"



async def is_address(address: str) -> (bool, str):
    if address == constants.COMMUNITY_FACTORY_ADDRESS:
        raise ValueError('The address should not be the address of the factory contract')
    if address[:2] != "0x":
        raise ValueError('Address should start with 0x')
    adr = address[2:]
    # throws exception if the string is not convertible to a hexadecimal number
    bts = bytearray.fromhex(adr)
    if len(bts) != 20:
        raise ValueError("The address must be 20 bytes")
    return True, "Wow, you go good!"


async def is_float(price: str) -> bool:
    try:
        float(price)
        return True
    except ValueError:
        return False


async def is_int(val) -> bool:
    try:
        itis = int(val)
        return True
    except ValueError:
        return False


async def check_string(s: str):
    return bool(re.match("^[A-Za-z0-9_]*$", s))


async def get_create_community_with_token_link(_name, _symbol, _price, _com_wallet, _tg_id) -> str:
    return '{}{}{}/{}/{}/{}/{}'.format(BASE_URI, CREATE_COMMUNITY_WITH_TOKEN, _name, _symbol, _price, _com_wallet, _tg_id)


async def get_create_community_with_custom(_com_tok, _com_wallet, _tg_id) -> str:
    return '{}{}{}/{}/{}'.format(BASE_URI, CREATE_WITH_CUSTOM, _com_wallet, _com_tok, _tg_id)


async def get_mint_token_link(_token_address, _amount) -> str:
    return '{}{}{}/{}'.format(BASE_URI, MINT_TOKEN, _token_address, _amount)


async def get_change_price_link(_token_address, _new_price) -> str:
    return '{}{}{}/{}'.format(BASE_URI, CHANGE_PRICE, _token_address, _new_price)


async def get_create_member_link(_com_id, _user_id) -> str:
    # in contracts: comId, tgID
    return '{}{}{}/{}'.format(BASE_URI, CREATE_MEMBER, _com_id, _user_id)


async def get_verify_member_link(_com_id, _user_id) -> str:
    # in contracts: comId, tgID
    return '{}{}{}/{}'.format(BASE_URI, VERIFY_MEMBER, _com_id, _user_id)


async def get_link_to_create_task(com_id, deadline, reward) -> str:
    return '{}{}{}/{}/{}'.format(BASE_URI, CREATE_TASK, com_id, deadline, reward)


async def get_link_to_propose_solution(ctr_com_id, task_id) -> str:
    return '{}{}{}/{}'.format(BASE_URI, PROPOSE_SOLUTION, ctr_com_id, task_id)


async def get_start_task_voting_link(ctr_com_id, task_id, voting_deadline) -> str:
    return '{}{}{}/{}/{}'.format(BASE_URI, START_VOTING_ON_TASK, ctr_com_id, task_id, voting_deadline)


async def get_create_voting_link(ctr_com_id, n_of_options, deadline) -> str:
    return '{}{}{}/{}/{}'.format(BASE_URI, CREATE_VOTING, ctr_com_id, n_of_options, deadline)


async def get_vote_link(ctr_com_id, voting_id, option) -> str:
    return '{}{}{}/{}/{}'.format(BASE_URI, VOTE, ctr_com_id, voting_id, option)


async def get_voting_results_link(ctr_com_id, voting_id) -> str:
    return '{}{}{}/{}'.format(BASE_URI, VOTING_RESULTS, ctr_com_id, voting_id)


async def get_task_results_link(ctr_com_id, task_id) -> str:
    return '{}{}{}/{}'.format(BASE_URI, TASK_RESULTS, ctr_com_id, task_id)


async def get_reward_link(ctr_com_id, task_id) -> str:
    return '{}{}{}/{}'.format(BASE_URI, REWARD, ctr_com_id, task_id)


async def add_community_token(address: str, chat_id: str) -> str:
    inserted_row_id = db.insert("community_chat", {
        "id": chat_id,
        "gt": address[2:]
    })
    res = await get_group_token(chat_id)
    return res


async def get_group_token(chat_id: str) -> str:
    cursor = db.get_cursor()
    sql_select_query = f"select * from community_chat where id = {chat_id}"
    cursor.execute(sql_select_query)
    record = cursor.fetchall()
    print("record: " + str(record))
    return f"0x{record[0][1]}"


async def check_group_token_exists_by_id(chat_id: int) -> bool:
    cursor = db.get_cursor()
    sql_select_query = f"select exists(select * from community_chat where id = {chat_id})"
    cursor.execute(sql_select_query)
    record = cursor.fetchall()
    print(f"check_group_token_exists_by_id: {record}")
    return bool(record[0][0])


# TODO: by address, not by chat_id
async def check_group_token_exists(com_tok: str) -> bool:
    cursor = db.get_cursor()
    blob = str(com_tok[2:])
    print("blob: ", blob)
    #sql_select_query = f"select exists(select * from community_chat where gt = {blob})"
    cursor.execute("""SELECT EXISTS(SELECT id FROM community_chat WHERE gt=?)""", [blob])
    #cursor.execute(sql_select_query)
    record = cursor.fetchall()
    print("check_group_token_exists record: ", record)
    print(f"check_group_token_exists: {bool(record)}")
    return bool(record[0][0])


async def get_chat_id_by_token(com_tok: str) -> int:
    if await check_group_token_exists(com_tok):
        cursor = db.get_cursor()
        blob = com_tok[2:]
        cursor.execute("""SELECT id FROM community_chat WHERE gt=?""", [blob])
        record = cursor.fetchall()
        print(f"get_chat_id_by_token: {record}")
        return record[0][0]
    else:
        return -1


async def delete_group_token(chat_id) -> bool:
    db.delete("community_chat", chat_id)
    return True


async def save_approve_request(_user_addr, _user_id, _chat_id):
    addr = _user_addr[2:]
    db.insert("approve", {
        "user_address": addr,
        "id": _user_id,
        "chat_id": _chat_id
    })


async def get_approve_request(_user_addr: str, _chat_id: str) -> ():
    print("get_approve_request")
    cursor = db.get_cursor()
    #try:
    blob = _user_addr[2:]
    print("blob: " + blob)
    print("chat id: " + _chat_id)
    cursor.execute("""SELECT id FROM approve WHERE user_address=? AND chat_id=?""", (blob, _chat_id))
    record = cursor.fetchall()
    print(f"get_approve_request: {record}")
    return record
    #except:
    #    return "-1"


async def delete_approve_request(_user_addr, _chat_id):
    print("delete_approve_request")
    cursor = db.get_cursor()
    blob = _user_addr[2:]
    cursor.execute("""DELETE FROM approve WHERE user_address=? AND chat_id=?""", (blob, _chat_id))
    conn.commit()
