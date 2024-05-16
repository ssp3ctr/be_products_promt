from babel.support import Translations
import os

def load_translations(locale: str):
    translations = Translations.load(
        dirname='locales',
        locales=[locale],
        domain='messages'
    )
    return translations

def _(request, message):
    """A shortcut for fetching the translated message."""
    gettext = request.state.gettext
    return gettext(message)
