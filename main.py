import re
import threading
import time
import logging

import catbot
from catbot.util import html_escape

from challenge import Challenge, TextReadingChallenge
from timeout import Timeout

bot = catbot.Bot(config_path='config.json')
t_lock = threading.Lock()


def timeout_callback(chat_id: int, msg_id: int, user_id: int):
    language = get_chat_language(chat_id)
    member = bot.get_chat_member(chat_id, user_id)
    try:
        bot.edit_message(
            chat_id,
            msg_id,
            text=bot.config['messages'][language]['challenge_failed'].format(
                user_id=user_id,
                name=member.name
            ),
            parse_mode='HTML'
        )
    except catbot.MessageNotFoundError:
        pass


def read_record_and_lift(chat_id: int, user_id: int):
    with t_lock:
        if 'restrict_record' in bot.record:
            restrict_record = bot.record['restrict_record']
        else:
            restrict_record = {}
    if str(chat_id) in restrict_record and str(user_id) in restrict_record[str(chat_id)]:
        record = restrict_record[str(chat_id)][str(user_id)]
        restricted_until = record['until'] if record['restricted_by'] != bot.id else time.time()
        bot.lift_and_preserve_restriction(chat_id, user_id, int(restricted_until))
    else:
        bot.lift_and_preserve_restriction(chat_id, user_id, int(time.time()))


def get_chat_language(chat_id: int) -> str:
    """
    Return language setting of a chat. If the chat has no language setting then return the default 'en'.
    :param chat_id:
    :return:
    """
    with t_lock:
        if 'language' in bot.record:
            chat_languages = bot.record['language']
        else:
            chat_languages = {}
    if str(chat_id) in chat_languages:
        return chat_languages[str(chat_id)]
    else:
        return 'en'


def match_blacklist(tokens: list[str]) -> bool:
    for reg in bot.config['blacklist']:
        for token in tokens:
            if re.search(reg, token):
                return True

    return False


def greeting_cri(msg: catbot.ChatMemberUpdate) -> bool:
    if msg.new_chat_member.id == bot.id \
            and msg.new_chat_member.status == 'member' \
            and msg.old_chat_member.status == 'left':
        return True
    else:
        return False


@bot.member_status_task(greeting_cri)
def greeting(msg: catbot.ChatMemberUpdate):
    language = get_chat_language(msg.chat.id)
    bot.send_message(msg.chat.id, text=bot.config['messages'][language]['self_intro'])


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


@bot.member_status_task(new_member_cri)
def new_member(msg: catbot.ChatMemberUpdate):
    try:
        bot.silence_chat_member(msg.chat.id, msg.new_chat_member.id)
        user_chat = bot.get_chat(msg.new_chat_member.id)
        if match_blacklist([msg.new_chat_member.name, user_chat.bio if user_chat.bio is not None else '']):
            bot.kick_chat_member(msg.chat.id, msg.new_chat_member.id)
            return
    except catbot.InsufficientRightError:
        return

    language = get_chat_language(msg.chat.id)
    # Randomly challenge user with a math or text reading problem
    problem: Challenge = TextReadingChallenge(bot.config['messages'][language]['text_reading_challenge'], language)
    button_list: list[list[catbot.InlineKeyboardButton]] = []
    answer_list: list[catbot.InlineKeyboardButton] = []
    for i in range(6):
        if problem.choices()[i] == problem.ans():
            answer_list.append(catbot.InlineKeyboardButton(
                text=problem.choices()[i],
                callback_data=f'{msg.new_chat_member.id}_correct'
            ))
        else:
            answer_list.append(catbot.InlineKeyboardButton(
                text=problem.choices()[i],
                callback_data=f'{msg.new_chat_member.id}_wrong'
            ))
    button_list.append(answer_list)
    button_list.append([
        catbot.InlineKeyboardButton(
            text=bot.config['messages'][language]['manually_approve'],
            callback_data=f'{msg.new_chat_member.id}_approve'
        ),
        catbot.InlineKeyboardButton(
            text=bot.config['messages'][language]['manually_reject'],
            callback_data=f'{msg.new_chat_member.id}_reject'
        )
    ])
    buttons = catbot.InlineKeyboard(button_list)

    try:
        sent = bot.send_message(msg.chat.id, text=bot.config['messages'][language]['new_member'].format(
            user_id=msg.new_chat_member.id,
            name=html_escape(msg.new_chat_member.name),
            timeout=bot.config['timeout'],
            challenge=problem.qus()
        ), parse_mode='HTML', reply_markup=buttons)
    except catbot.APIError as e:
        logging.info(e.args[0])
        new_member(msg)  # rerun if any problem in sending
    else:
        timeout = Timeout(
            chat_id=msg.chat.id,
            user_id=msg.new_chat_member.id,
            msg_id=sent.id,
            timer=bot.config['timeout']
        )
        timeout_thread = threading.Thread(target=timeout.run, kwargs={
            'callback': timeout_callback,
            'chat_id': msg.chat.id,
            'msg_id': sent.id,
            'user_id': msg.new_chat_member.id
        })
        timeout_thread.start()


def challenge_button_cri(query: catbot.CallbackQuery):
    return query.data.endswith('correct') or query.data.endswith('wrong')


@bot.query_task(challenge_button_cri)
def challenge_button(query: catbot.CallbackQuery):
    language = get_chat_language(query.msg.chat.id)
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
            bot.answer_callback_query(
                query.id,
                text=bot.config['messages'][language]['button_not_for_you'],
                show_alert=True,
                cache_time=bot.config['timeout']
            )
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
        bot.edit_message(
            query.msg.chat.id,
            query.msg.id,
            text=bot.config['messages'][language]['challenge_passed'].format(
                user_id=challenged_user_id,
                name=html_escape(challenged_user.name)
            ),
            parse_mode='HTML'
        )
        read_record_and_lift(query.msg.chat.id, challenged_user_id)
        time.sleep(bot.config['shorten_after_pass_delay'])
        try:
            bot.edit_message(
                query.msg.chat.id,
                query.msg.id,
                text=bot.config['messages'][language]['challenge_passed_short'].format(
                    user_id=challenged_user_id,
                    name=html_escape(challenged_user.name)
                ),
                parse_mode='HTML'
            )
        except catbot.MessageNotFoundError:
            pass
    else:
        bot.edit_message(
            query.msg.chat.id,
            query.msg.id,
            text=bot.config['messages'][language]['challenge_failed'].format(
                user_id=challenged_user_id,
                name=html_escape(challenged_user.name)
            ),
            parse_mode='HTML'
        )


def kicked_before_captcha_cri(msg: catbot.ChatMemberUpdate):
    return msg.new_chat_member.id != msg.from_.id and msg.new_chat_member.status == 'kicked' and msg.from_.id != bot.id


@bot.member_status_task(kicked_before_captcha_cri)
def kicked_before_captcha(msg: catbot.ChatMemberUpdate):
    for timeout in Timeout.list_all():
        if timeout.chat_id == msg.chat.id and timeout.user_id == msg.new_chat_member.id:
            timeout.stop()
            try:
                bot.delete_message(timeout.chat_id, timeout.msg_id)
            except catbot.DeleteMessageError:
                pass


def manual_operations_cri(query: catbot.CallbackQuery):
    return query.data.endswith('approve') or query.data.endswith('reject')


@bot.query_task(manual_operations_cri)
def manual_operations(query: catbot.CallbackQuery):
    language = get_chat_language(query.msg.chat.id)
    operator = bot.get_chat_member(query.msg.chat.id, query.from_.id)
    if operator.status != 'administrator' and operator.status != 'creator':
        bot.answer_callback_query(
            query.id,
            text=bot.config['messages'][language]['permission_denied'],
            show_alert=True,
            cache_time=bot.config['timeout']
        )
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
        bot.edit_message(
            query.msg.chat.id,
            query.msg.id,
            text=bot.config['messages'][language]['manually_approved'].format(
                user_id=challenged_user_id,
                name=html_escape(challenged_user.name),
                admin_name=html_escape(operator.name)
            ),
            parse_mode='HTML'
        )
        read_record_and_lift(query.msg.chat.id, challenged_user_id)
    else:
        bot.edit_message(
            query.msg.chat.id,
            query.msg.id,
            text=bot.config['messages'][language]['manually_rejected'].format(
                user_id=challenged_user_id,
                name=html_escape(challenged_user.name),
                admin_name=html_escape(operator.name)
            ),
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


@bot.member_status_task(update_restriction_cri)
def update_restriction(msg: catbot.ChatMemberUpdate):
    with t_lock:
        if 'restrict_record' in bot.record:
            restrict_record = bot.record['restrict_record']
        else:
            restrict_record = {}

        if msg.new_chat_member.status == 'restricted':
            until = msg.new_chat_member.until_date
            if str(msg.chat.id) not in restrict_record:
                restrict_record[str(msg.chat.id)] = {}
            restrict_record[str(msg.chat.id)][str(msg.new_chat_member.id)] = {
                'restricted_by': msg.from_.id,
                'until': until
            }
        else:  # The member is no longer restricted
            if str(msg.chat.id) in restrict_record:
                restrict_record[str(msg.chat.id)].pop(str(msg.new_chat_member.id), None)

        bot.record['restrict_record'] = restrict_record


def set_language_cri(msg: catbot.Message) -> bool:
    return bot.detect_command('/set_language', msg, require_username=True)


@bot.msg_task(set_language_cri)
def set_language(msg: catbot.Message):
    language = get_chat_language(msg.chat.id)
    operator = bot.get_chat_member(msg.chat.id, msg.from_.id)
    if operator.status != 'administrator' and operator.status != 'creator':
        bot.send_message(msg.chat.id, text=bot.config['messages'][language]['permission_denied'])
        return
    button_list = []
    for item in bot.config['languages']:
        button_list.append([catbot.InlineKeyboardButton(item, callback_data=f'language_{item}')])
    buttons = catbot.InlineKeyboard(button_list)
    bot.send_message(msg.chat.id, text=bot.config['messages'][language]['set_language_prompt'], reply_markup=buttons)


def set_language_button_cri(query: catbot.CallbackQuery) -> bool:
    return query.data.startswith('language')


@bot.query_task(set_language_button_cri)
def set_language_button(query: catbot.CallbackQuery):
    chat_id = query.msg.chat.id
    language = get_chat_language(chat_id)
    operator = bot.get_chat_member(chat_id, query.from_.id)
    if operator.status != 'administrator' and operator.status != 'creator':
        bot.answer_callback_query(
            query.id,
            text=bot.config['messages'][language]['permission_denied'],
            show_alert=True,
            cache_time=bot.config['timeout']
        )
        return

    target_language = query.data.split('_')[1]
    language = target_language
    with t_lock:
        if 'language' in bot.record:
            chat_languages = bot.record['language']
        else:
            chat_languages = {}
        chat_languages[str(chat_id)] = target_language
        bot.record['language'] = chat_languages

    bot.edit_message(query.msg.chat.id, query.msg.id, text=bot.config['messages'][language]['set_language_done'].format(
        language=target_language
    ))


def check_user_id_cri(msg: catbot.Message) -> bool:
    return bot.detect_command('/user_id', msg) and msg.reply and msg.reply_to_message.from_.id == bot.id


@bot.msg_task(check_user_id_cri)
def check_user_id(msg: catbot.Message):
    chat_id = msg.chat.id
    language = get_chat_language(chat_id)

    captcha_msg = msg.reply_to_message
    if captcha_msg.text_mention:
        uid = captcha_msg.text_mention[0][1].id
        bot.send_message(msg.chat.id, text=str(uid), reply_to_message_id=msg.reply_to_message.id)
    else:
        bot.send_message(
            chat_id,
            text=bot.config['messages'][language]['check_user_id_failed'],
            reply_to_message_id=msg.reply_to_message.id
        )

    try:
        bot.delete_message(msg.chat.id, msg.id)
    except (catbot.DeleteMessageError, catbot.InsufficientRightError):
        pass


if __name__ == '__main__':
    bot.start()
