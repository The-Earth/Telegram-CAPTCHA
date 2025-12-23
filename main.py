import re
import threading
import time
import logging
from collections import defaultdict

import catbot
from catbot.util import html_escape

from challenge import Challenge, TextReadingChallenge, MathChallenge
from anti_flood import AntiFlood
from timeout import Timeout


class CaptchaBot(catbot.Bot):
    def __init__(self, config_path):
        super().__init__(config_path=config_path)

        self.anti_flood_period: int = int(self.config['anti_flood']['period'])
        self.anti_flood_count: int = int(self.config['anti_flood']['count'])

        self.flood_messages: defaultdict[str, list[catbot.ChatMemberUpdate]] = defaultdict(list)
        self.anti_floods: defaultdict[str, AntiFlood] = defaultdict(AntiFlood)


bot = CaptchaBot(config_path='config.json')
t_lock = threading.Lock()


def test_if_flooding(msg: catbot.ChatMemberUpdate) -> bool:
    chat_id = msg.chat.id
    current_time = msg.date
    with t_lock:
        for item in filter(lambda x: x.date < current_time - bot.anti_flood_period, bot.flood_messages[chat_id]):
            bot.flood_messages[chat_id].remove(item)
        bot.flood_messages[chat_id].append(msg)
    return len(bot.flood_messages[chat_id]) >= bot.anti_flood_count


def timeout_callback(chat_id: int, msg_id: int, user_id: int, is_flooding: bool):
    language = get_chat_language(chat_id)
    member = bot.get_chat_member(chat_id, user_id)
    try:
        text = bot.config['messages'][language]['challenge_failed'].format(
            user_id=user_id,
            name=member.name
        )
        if is_flooding:
            text += '\n' + bot.config['messages'][language]['flood_detected']
        bot.edit_message(
            chat_id,
            msg_id,
            text=text,
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


def msg_contain_anti_flood_advice(msg: catbot.Message) -> bool:
    return any(map(lambda x: x.startswith('/enable_anti_flood'), msg.commands))


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
        if int(msg.new_chat_member.id) not in bot.config['whitelist'] and \
                match_blacklist([msg.new_chat_member.name, user_chat.bio if user_chat.bio is not None else '']):
            bot.kick_chat_member(msg.chat.id, msg.new_chat_member.id)
            return
    except catbot.InsufficientRightError:
        return

    chat_id = msg.chat.id
    language = get_chat_language(msg.chat.id)
    is_flooding = test_if_flooding(msg)

    if bot.anti_floods[chat_id].enabled:
        bot.anti_floods[chat_id].counter += 1
        text = bot.config['messages'][language]['anti_flood_enabled'].format(
            num=bot.anti_floods[chat_id].counter
        )
        try:
            bot.edit_message(chat_id, bot.anti_floods[chat_id].msg_id, text=text)
        except catbot.APIError as e:
            logging.info(e.args[0])
    else:
        template = bot.config['messages'][language]['text_reading_challenge']
        user_agent = bot.config['user_agent']
        # Randomly challenge user with a math or text reading problem
        problem: Challenge = TextReadingChallenge(template, language, user_agent)
        # problem: Challenge = MathChallenge()
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
        text = bot.config['messages'][language]['new_member'].format(
            user_id=msg.new_chat_member.id,
            name=html_escape(msg.new_chat_member.name),
            timeout=bot.config['timeout'],
            challenge=problem.qus()
        )
        if is_flooding:
            text += '\n\n' + bot.config['messages'][language]['flood_detected']

        try:
            sent = bot.send_message(msg.chat.id, text=text, parse_mode='HTML', reply_markup=buttons)
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
                'user_id': msg.new_chat_member.id,
                'is_flooding': is_flooding
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
    keep_anti_flood = msg_contain_anti_flood_advice(query.msg)
    if query_token[1] == 'correct':
        text = bot.config['messages'][language]['challenge_passed'].format(
            user_id=challenged_user_id,
            name=html_escape(challenged_user.name)
        )
        if keep_anti_flood:
            text += '\n' + bot.config['messages'][language]['flood_detected']
        bot.edit_message(
            query.msg.chat.id,
            query.msg.id,
            text=text,
            parse_mode='HTML'
        )
        read_record_and_lift(query.msg.chat.id, challenged_user_id)
        time.sleep(bot.config['shorten_after_pass_delay'])
        try:
            text = bot.config['messages'][language]['challenge_passed_short'].format(
                user_id=challenged_user_id,
                name=html_escape(challenged_user.name)
            )
            if keep_anti_flood:
                text += '\n' + bot.config['messages'][language]['flood_detected']
            bot.edit_message(
                query.msg.chat.id,
                query.msg.id,
                text=text,
                parse_mode='HTML'
            )
        except catbot.MessageNotFoundError:
            pass
    else:
        text = bot.config['messages'][language]['challenge_failed'].format(
            user_id=challenged_user_id,
            name=html_escape(challenged_user.name)
        )
        if keep_anti_flood:
            text += '\n' + bot.config['messages'][language]['flood_detected']
        bot.edit_message(
            query.msg.chat.id,
            query.msg.id,
            text=text,
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


def enable_anti_flood_cri(msg: catbot.Message) -> bool:
    return bot.detect_command('/enable_anti_flood', msg)


@bot.msg_task(enable_anti_flood_cri)
def enable_anti_flood(msg: catbot.Message):
    chat_id = msg.chat.id
    language = get_chat_language(chat_id)
    operator = bot.get_chat_member(chat_id, msg.from_.id)
    if operator.status != 'administrator' and operator.status != 'creator':
        bot.send_message(msg.chat.id, text=bot.config['messages'][language]['permission_denied'],
                         reply_to_message_id=msg.reply_to_message.id)
        return

    sent = bot.send_message(chat_id, text=bot.config['messages'][language]['anti_flood_enabled'].format(num=0))
    bot.anti_floods[chat_id].enable(sent)


def disable_anti_flood(msg: catbot.Message) -> bool:
    return bot.detect_command('/disable_anti_flood', msg)


@bot.msg_task(disable_anti_flood)
def disable_anti_flood(msg: catbot.Message):
    chat_id = msg.chat.id
    language = get_chat_language(chat_id)
    operator = bot.get_chat_member(chat_id, msg.from_.id)
    if operator.status != 'administrator' and operator.status != 'creator':
        bot.send_message(msg.chat.id, text=bot.config['messages'][language]['permission_denied'],
                         reply_to_message_id=msg.reply_to_message.id)
        return

    if bot.anti_floods[chat_id].enabled:
        anti: AntiFlood = bot.anti_floods[chat_id]
        anti.disable()
        try:
            bot.send_message(
                chat_id,
                text=bot.config['messages'][language]['anti_flood_disabled'].format(num=anti.counter)
            )
        except catbot.APIError as e:
            logging.info(e.args[0])


def add_whitelist_cri(msg: catbot.Message):
    return bot.detect_command('/add_whitelist', msg)


@bot.msg_task(add_whitelist_cri)
def add_whitelist(msg: catbot.Message):
    chat_id = msg.chat.id
    language = get_chat_language(chat_id)
    operator = bot.get_chat_member(chat_id, msg.from_.id)
    if operator.status != 'administrator' and operator.status != 'creator':
        bot.send_message(msg.chat.id, text=bot.config['messages'][language]['permission_denied'],
                         reply_to_message_id=msg.id)
        return

    if msg.reply:
        to_whitelist_id = int(msg.reply_to_message.from_.id)
    else:
        msg_split = msg.text.split(' ')
        if len(msg_split) < 2:
            bot.send_message(chat_id, text=bot.config['messages'][language]['add_whitelist_prompt'],
                             reply_to_message_id=msg.id)
            return
        try:
            to_whitelist_id = int(msg_split[1])
        except ValueError:
            bot.send_message(chat_id, text=bot.config['messages'][language]['add_whitelist_prompt'],
                             reply_to_message_id=msg.id)
            return

    new_list = bot.config['whitelist']
    new_list.append(to_whitelist_id)
    new_list = list(set(new_list))
    bot.config['whitelist'] = new_list
    bot.send_message(chat_id, text=bot.config['messages'][language]['add_whitelist_succeeded'].format(user_id=to_whitelist_id),
                     reply_to_message_id=msg.id)


def remove_whitelist_cri(msg: catbot.Message):
    return bot.detect_command('/remove_whitelist', msg)


@bot.msg_task(remove_whitelist_cri)
def remove_whitelist(msg: catbot.Message):
    chat_id = msg.chat.id
    language = get_chat_language(chat_id)
    operator = bot.get_chat_member(chat_id, msg.from_.id)
    if operator.status != 'administrator' and operator.status != 'creator':
        bot.send_message(msg.chat.id, text=bot.config['messages'][language]['permission_denied'],
                         reply_to_message_id=msg.id)
        return

    if msg.reply:
        to_remove_id = int(msg.reply_to_message.from_.id)
    else:
        msg_split = msg.text.split(' ')
        if len(msg_split) < 2:
            bot.send_message(chat_id, text=bot.config['messages'][language]['remove_whitelist_prompt'],
                             reply_to_message_id=msg.id)
            return
        try:
            to_remove_id = int(msg_split[1])
        except ValueError:
            bot.send_message(chat_id, text=bot.config['messages'][language]['remove_whitelist_prompt'],
                             reply_to_message_id=msg.id)
            return

    try:
        bot.config['whitelist'].remove(to_remove_id)
    except ValueError:
        pass
    bot.send_message(chat_id, text=bot.config['messages'][language]['remove_whitelist_succeeded'].format(user_id=to_remove_id),
                     reply_to_message_id=msg.id)


if __name__ == '__main__':
    with bot:
        bot.start()
