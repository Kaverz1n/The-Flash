import os

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hide_link

from keyboards.for_back import get_back_keyboard

router = Router()


@router.callback_query(F.data == 'about_company')
async def about_company(callback: CallbackQuery) -> None:
    '''
    A handler for showing the information about the company
    '''
    await callback.message.answer(
        text=f'{hide_link(os.getenv("FULL_LOGO_URL"))}'
             f'⛩️\u00A0О КОМПАНИИ\u00A0⛩️\n\n'
             f'Мы - <b>компания</b> с многолетним опытом в сфере логистики, '
             f'обеспечивающая <b>надежные</b> и <b>эффективные</b> поставки '
             f'товаров. С недавних пор мы начали расширять нашу деятельность '
             f'и доставлять качественные товары из Китая с маркетплейса '
             f'<b>POIZON (DEWU)</b>.\n\n'
             f'🌏\u00A0ГЛОБАЛЬНАЯ СЕТЬ\u00A0🌏\n\n'
             f'Наша команда <b>моментально</b> реагирует на заказы пользователей и '
             f'<b>незамедлительно</b> выкупает выбранные товары с маркетплейса '
             f'<b>POIZON (DEWU)</b> в Китае. После получения товаров на наших '
             f'складах в Китае, мы <b>оперативно</b> и <b>безупречно</b> организуем '
             f'доставку в Россию или в любую другую страну. Таким образом, вы можете '
             f'быть уверены, что <b>Ваш заказ</b> будет доставлен прямо к вам с '
             f'<b>минимальными задержками</b> и в <b>идеальном состоянии</b>.\n\n'
             f'📦\u00A0БЫСТРАЯ ДОСТАВКА📦\u00A0\n\n'
             f'Мы <b>гордимся</b> тем, что обеспечиваем <b>молниеносную</b> '
             f'доставку благодаря <b>оптимизированным логистическим процессам</b> и '
             f'<b>инновационным технологиям</b>. Ваш заказ достигнет вас быстрее, '
             f'потому что мы <b>ценим ваше время</b>.\n\n'
             f'💸\u00A0НИЗКАЯ КОМИССИЯ\u00A0💸\n\n'
             f'Наша <b>низкая комиссия</b> основана на нашей <b>уникальной модели бизнеса</b>, '
             f'которая позволяет нам <b>минимизировать издержки</b> и <b>предложить вам '
             f'лучшие цены на рынке</b>. Мы стремимся к <b>прямым</b> и <b>эффективным</b> '
             f'взаимоотношениям с нашими партнерами, что помогает нам <b>избежать излишних '
             f'посредников</b> и <b>связанных с ними комиссий</b>, а также <b>объединяем</b> '
             f'заказы наших клиентов. Благодаря этому подходу, мы можем сэкономить для Вас '
             f'ваши <b>средства</b> и <b>время</b>.\n\n⚡'
             f'️\u00A0ПОЧЕМУ МЫ?\u00A0⚡\n\n'
             f'Мы стремимся быть <b>лучшими в своей области</b>, предоставляя вам <b>оригинальные</b> '
             f'товары, <b>быструю</b> доставку и <b>превосходное</b> обслуживание клиентов. '
             f'Доверьтесь нам, и вы не пожалеете о своем выборе!\n\n'
             f'☎️\u00A0КОНТАКТЫ\u00A0☎️\n\n'
             f'Если у Вас <b>возникли вопросы</b> или вам <b>требуется помощь</b>, свяжитесь '
             f'с нашей командой поддержки, нажав соответсвующую кнопку в главном меню, или '
             f'по указанным ниже контактам:\n\n<b>E-mail:</b> theflash@gmail.com\n'
             f'<b>Администратор:</b> @Kaverz1n',
        reply_markup=get_back_keyboard()
    )
    await callback.answer()
