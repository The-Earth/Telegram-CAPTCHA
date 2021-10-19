import json
import threading
import time

import catbot

from challenge import Challenge
from timeout import Timeout

config = json.load(open('config.json', 'r', encoding='utf-8'))
bot = catbot.Bot(config)
t_lock = threading.Lock()


def timeout_callback(chat_id: int, msg_id: int, user_id: int):
    member = bot.get_chat_member(chat_id, user_id)
    bot.edit_message(chat_id, msg_id, text=config['messages']['challenge_failed'].format(user_id=user_id,
                                                                                         name=member.name),
                     parse_mode='HTML')


def secure_record_fetch(key: str, data_type):
    """
    :param key: Name of the data you want in record file
    :param data_type: Type of the data. For example, if it is trusted user list, data_type will be list.
    :return: Returns a tuple. The first element is the data you asked for. The second is the deserialized record file.
    """
    try:
        rec = json.load(open(config['record'], 'r', encoding='utf-8'))
    except FileNotFoundError:
        record_list, rec = data_type(), {}
        json.dump({key: record_list}, open(config['record'], 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    else:
        if key in rec.keys():
            record_list = rec[key]
        else:
            record_list = data_type()

    return record_list, rec


def read_record_and_lift(chat_id: int, user_id: int):
    with t_lock:
        restrict_record, rec = secure_record_fetch('restrict_record', dict)
    if str(chat_id) in restrict_record \
            and str(user_id) in restrict_record[str(chat_id)]:
        record = restrict_record[str(chat_id)][str(user_id)]
        restricted_until = record['until'] if record['restricted_by'] != bot.id else time.time()
        lift_restriction(chat_id, user_id, int(restricted_until))
    else:
        lift_restriction(chat_id, user_id, int(time.time()))


def lift_restriction(chat_id: int, user_id: int, restricted_until: int):
    member = bot.get_chat_member(chat_id, user_id)
    if member.status == 'kicked':
        return
    try:
        if restricted_until <= time.time() + 35 and restricted_until != 0:
            bot.lift_restrictions(chat_id, user_id)
        else:
            bot.silence_chat_member(chat_id, user_id, until=restricted_until)
    except catbot.RestrictAdminError:
        pass
    except catbot.InsufficientRightError:
        pass
    except catbot.UserNotFoundError:
        pass


def greeting_cri(msg: catbot.ChatMemberUpdate) -> bool:
    if msg.new_chat_member.id == bot.id \
            and msg.new_chat_member.status == 'member' \
            and msg.old_chat_member.status == 'left':
        return True
    else:
        return False


def greeting(msg: catbot.ChatMemberUpdate):
    bot.send_message(msg.chat.id, text=config['messages']['self_intro'])


def new_member_cri(msg: catbot.ChatMemberUpdate) -> bool:
    if time.time() - msg.date > 180:
        return False
    if msg.new_chat_member.is_bot:
        return False
    elif msg.new_chat_member.status == 'member':
        if msg.old_chat_member.status == 'left':
            return True
        elif msg.old_chat_member.status == 'restricted' and not msg.old_chat_member.is_member:
            return True
        else:
            return False
    elif msg.new_chat_member.status == 'restricted' and msg.new_chat_member.is_member:
        if msg.old_chat_member.status == 'left':
            return True
        elif msg.old_chat_member.status == 'restricted' and not msg.old_chat_member.is_member:
            return True
        else:
            return False
    else:
        return False


def new_member(msg: catbot.ChatMemberUpdate):
    try:
        bot.silence_chat_member(msg.chat.id, msg.new_chat_member.id)
    except catbot.InsufficientRightError:
        return

    problem = Challenge()
    button_list = []
    answer_list = []
    for i in range(6):
        if problem.choices()[i] == problem.ans():
            answer_list.append(catbot.InlineKeyboardButton(text=problem.choices()[i],
                                                           callback_data=f'{msg.new_chat_member.id}_correct'))
        else:
            answer_list.append(catbot.InlineKeyboardButton(text=problem.choices()[i],
                                                           callback_data=f'{msg.new_chat_member.id}_wrong'))
    button_list.append(answer_list)
    button_list.append([catbot.InlineKeyboardButton(text=config['messages']['manually_approve'],
                                                    callback_data=f'{msg.new_chat_member.id}_approve'),
                        catbot.InlineKeyboardButton(text=config['messages']['manually_reject'],
                                                    callback_data=f'{msg.new_chat_member.id}_reject')
                        ])
    buttons = catbot.InlineKeyboard(button_list)

    sent = bot.send_message(msg.chat.id, text=config['messages']['new_member'].format(
        user_id=msg.new_chat_member.id,
        name=msg.new_chat_member.name,
        timeout=config['timeout'],
        challenge=problem.qus()
    ), parse_mode='HTML', reply_markup=buttons)

    timeout = Timeout(chat_id=msg.chat.id, user_id=msg.new_chat_member.id, msg_id=sent.id, timer=config['timeout'])
    timeout_thread = threading.Thread(target=timeout.run, kwargs={'callback': timeout_callback,
                                                                  'chat_id': msg.chat.id,
                                                                  'msg_id': sent.id,
                                                                  'user_id': msg.new_chat_member.id})

    timeout_thread.start()


def challenge_button_cri(query: catbot.CallbackQuery):
    return query.data.endswith('correct') or query.data.endswith('wrong')


def challenge_button(query: catbot.CallbackQuery):
    query_token = query.data.split('_')
    if len(query_token) != 2:
        bot.answer_callback_query(query.id)
        return
    try:
        challenged_user_id = int(query_token[0])
    except ValueError:
        bot.answer_callback_query(query.id)
        return
    else:
        if query.from_.id != challenged_user_id:
            bot.answer_callback_query(query.id, text=config['messages']['button_not_for_you'],
                                      show_alert=True, cache_time=config['timeout'])
            return

    bot.answer_callback_query(query.id)
    for timeout in Timeout.list_all():
        if timeout.chat_id == query.msg.chat.id and timeout.msg_id == query.msg.id:
            timeout.stop()
            break
    else:
        return

    challenged_user = bot.get_chat_member(query.msg.chat.id, challenged_user_id)
    if query_token[1] == 'correct':
        bot.edit_message(query.msg.chat.id, query.msg.id,
                         text=config['messages']['challenge_passed'].format(user_id=challenged_user_id,
                                                                            name=challenged_user.name),
                         parse_mode='HTML')
        read_record_and_lift(query.msg.chat.id, challenged_user_id)
        time.sleep(config['shorten_after_pass_delay'])
        bot.edit_message(query.msg.chat.id, query.msg.id,
                         text=config['messages']['challenge_passed_short'].format(user_id=challenged_user_id,
                                                                                  name=challenged_user.name),
                         parse_mode='HTML')
    else:
        bot.edit_message(query.msg.chat.id, query.msg.id,
                         text=config['messages']['challenge_failed'].format(user_id=challenged_user_id,
                                                                            name=challenged_user.name),
                         parse_mode='HTML')


def manual_operations_cri(query: catbot.CallbackQuery):
    return query.data.endswith('approve') or query.data.endswith('reject')


def manual_operations(query: catbot.CallbackQuery):
    operator = bot.get_chat_member(query.msg.chat.id, query.from_.id)
    if operator.status != 'administrator' and operator.status != 'creator':
        bot.answer_callback_query(query.id, text=config['messages']['manual_denied'],
                                  show_alert=True,
                                  cache_time=config['timeout'])
        return

    query_token = query.data.split('_')
    if len(query_token) != 2:
        bot.answer_callback_query(query.id)
        return
    try:
        challenged_user_id = int(query_token[0])
    except ValueError:
        bot.answer_callback_query(query.id)
        return

    bot.answer_callback_query(query.id)
    for timeout in Timeout.list_all():
        if timeout.chat_id == query.msg.chat.id and timeout.msg_id == query.msg.id:
            timeout.stop()
            break

    challenged_user = bot.get_chat_member(query.msg.chat.id, challenged_user_id)
    if query_token[1] == 'approve':
        bot.edit_message(query.msg.chat.id, query.msg.id,
                         text=config['messages']['manually_approved'].format(user_id=challenged_user_id,
                                                                             name=challenged_user.name,
                                                                             admin_name=operator.name),
                         parse_mode='HTML')
        read_record_and_lift(query.msg.chat.id, challenged_user_id)
    else:
        bot.edit_message(query.msg.chat.id, query.msg.id,
                         text=config['messages']['manually_rejected'].format(user_id=challenged_user_id,
                                                                             name=challenged_user.name,
                                                                             admin_name=operator.name),
                         parse_mode='HTML')
        try:
            bot.kick_chat_member(query.msg.chat.id, challenged_user_id)
        except catbot.InsufficientRightError:
            pass


def update_restriction_cri(msg: catbot.ChatMemberUpdate):
    if msg.from_.id != bot.id and msg.from_.id != msg.new_chat_member.id:
        return True
    else:
        return False


def update_restriction(msg: catbot.ChatMemberUpdate):
    with t_lock:
        restrict_record, rec = secure_record_fetch('restrict_record', dict)

        if msg.new_chat_member.status == 'restricted':
            until = msg.new_chat_member.until_date
            if str(msg.chat.id) not in restrict_record:
                restrict_record[str(msg.chat.id)] = {}
            restrict_record[str(msg.chat.id)][str(msg.new_chat_member.id)] = {'restricted_by': msg.from_.id,
                                                                              'until': until}
        else:  # The member is no longer restricted
            if str(msg.chat.id) in restrict_record:
                restrict_record[str(msg.chat.id)].pop(str(msg.new_chat_member.id), None)

        rec['restrict_record'] = restrict_record
        json.dump(rec, open(config['record'], 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


if __name__ == '__main__':
    bot.add_member_status_task(greeting_cri, greeting)
    bot.add_member_status_task(new_member_cri, new_member)
    bot.add_query_task(challenge_button_cri, challenge_button)
    bot.add_query_task(manual_operations_cri, manual_operations)
    bot.add_member_status_task(update_restriction_cri, update_restriction)

    bot.start()
