from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def get_start_keyboard() -> VkKeyboard:

    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)

    keyboard.add_line()
    keyboard.add_button('Мой счёт', color=VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()
