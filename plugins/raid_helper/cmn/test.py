import logging

from raid_helper import utils as raid_utils
from raid_helper.utils.typing import *

enable_test = raid_utils.common_trigger.add_value(raid_utils.BoolCheckBox('test/enable', False))
draw_test = raid_utils.common_trigger.add_value(raid_utils.BoolCheckBox('test/draw_test', False))
test_value_1 = raid_utils.common_trigger.add_value(raid_utils.IntSlider('test/value1', -5, 5, 0))
test_target = raid_utils.common_trigger.add_value(raid_utils.Select('test/target', [
    ('Me', 0),
    ('Any', 1),
], 0))
test_exception = raid_utils.common_trigger.add_value(raid_utils.BoolCheckBox('test/test_exception', False))
logger = logging.getLogger('raid_helper/test')


@raid_utils.common_trigger.on_effect()
def on_any_effect(msg: NetworkMessage[zone_server.ActionEffect]):
    if enable_test.value and msg.message.action_kind == 1 and (test_target.value or raid_utils.is_me_id(msg.header.source_id)):
        if test_exception.value:
            raise Exception('Test')
        if actor := raid_utils.main.mem.actor_table.get_actor_by_id(msg.header.source_id):
            raid_utils.draw_knock_predict_circle(radius=40, pos=actor.pos, duration=5, knock_distance=10)
            # raid_utils.draw_share(radius=3, pos=actor, duration=5)
            name = actor.name
        else:
            name = f'actor#{msg.header.source_id:X}'
        action_name = str(raid_utils.main.sq_pack.sheets.action_sheet[msg.message.action_id].text)
        logger.info(f'{name} use {action_name} test value:{test_value_1.value} target_mode:{test_target.value}')
        raid_utils.tts(action_name)


@raid_utils.common_trigger.on_effect()
def on_any_effect_draw_test(msg: NetworkMessage[zone_server.ActionEffect]):
    if not (draw_test.value and raid_utils.is_me_id(msg.header.source_id)): return
    logger.info('draw_test')
    # for a in raid_utils.iter_main_party(False):
    #     raid_utils.draw_circle(radius=3, pos=a, duration=5)

    if (me := raid_utils.main.mem.actor_table.me) is None: return
    if (target := raid_utils.main.mem.actor_table.get_actor_by_id(me.target_id)) is None: return
    raid_utils.draw_distance_line(me, target, duration=20, min_distance=10, max_distance=15)


def draw_circle():
    if me := raid_utils.get_me():
        raid_utils.draw_circle(radius=6, pos=me, duration=5)


def draw_donut():
    if me := raid_utils.get_me():
        raid_utils.draw_circle(radius=6, inner_radius=3, pos=me, duration=5)


def draw_fan():
    if me := raid_utils.get_me():
        raid_utils.draw_fan(radius=6, degree=60, pos=me, duration=5)


def draw_rect():
    if me := raid_utils.get_me():
        raid_utils.draw_rect(width=4, length=10, pos=me, duration=5)


raid_utils.common_trigger.add_value(raid_utils.ClickButton('test/draw_circle', draw_circle))
raid_utils.common_trigger.add_value(raid_utils.ClickButton('test/draw_donut', draw_donut))
raid_utils.common_trigger.add_value(raid_utils.ClickButton('test/draw_fan', draw_fan))
raid_utils.common_trigger.add_value(raid_utils.ClickButton('test/draw_rect', draw_rect))
