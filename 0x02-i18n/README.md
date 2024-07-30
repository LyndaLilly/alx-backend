Flask-Babel
Flask-Babel is an extension to Flask that adds i18n and l10n support to any Flask application with the help of babel, pytz and speaklater. It has builtin support for date formatting with timezone support as well as a very simple and friendly interface to gettext translations.

Installation
Install the extension from PyPi:

$ pip install Flask-Babel
Please note that Flask-Babel requires Jinja >=2.5. If you are using an older version you will have to upgrade or disable the Jinja support (see configuration).

Configuration
To get started all you need to do is to instantiate a Babel object after configuring the application:

from flask import Flask
from flask_babel import Babel

app = Flask(__name__)
app.config.from_pyfile('mysettings.cfg')
babel = Babel(app)
To disable jinja support, include configure_jinja=False in the Babel constructor call. The babel object itself can be used to configure the babel support further. Babel has the following configuration values that can be used to change some internal defaults:

BABEL_DEFAULT_LOCALE

The default locale to use if no locale selector is registered. This defaults to 'en'.

BABEL_DEFAULT_TIMEZONE

The timezone to use for user facing dates. This defaults to 'UTC' which also is the timezone your application must use internally.

BABEL_TRANSLATION_DIRECTORIES

A semi-colon (;) separated string of absolute and relative (to the app root) paths to translation folders. Defaults to translations.

BABEL_DOMAIN

The message domain used by the application. Defaults to messages.

For more complex applications you might want to have multiple applications for different users which is where selector functions come in handy. The first time the babel extension needs the locale (language code) of the current user it will call a localeselector() function, and the first time the timezone is needed it will call a timezoneselector() function.

If any of these methods return None the extension will automatically fall back to what’s in the config. Furthermore for efficiency that function is called only once and the return value then cached. If you need to switch the language between a request, you can refresh() the cache.

Example selector functions:

from flask import g, request

@babel.localeselector
def get_locale():
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support de/fr/en in this
    # example.  The best match wins.
    return request.accept_languages.best_match(['de', 'fr', 'en'])

@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone
The example above assumes that the current user is stored on the flask.g object.

Formatting Dates
To format dates you can use the format_datetime(), format_date(), format_time() and format_timedelta() functions. They all accept a datetime.datetime (or datetime.date, datetime.time and datetime.timedelta) object as first parameter and then optionally a format string. The application should use naive datetime objects internally that use UTC as timezone. On formatting it will automatically convert into the user’s timezone in case it differs from UTC.

To play with the date formatting from the console, you can use the test_request_context() method:

app.test_request_context().push()
Here some examples:

from flask_babel import format_datetime
from datetime import datetime
format_datetime(datetime(1987, 3, 5, 17, 12))
u'Mar 5, 1987 5:12:00 PM'
format_datetime(datetime(1987, 3, 5, 17, 12), 'full')
u'Thursday, March 5, 1987 5:12:00 PM World (GMT) Time'
format_datetime(datetime(1987, 3, 5, 17, 12), 'short')
u'3/5/87 5:12 PM'
format_datetime(datetime(1987, 3, 5, 17, 12), 'dd mm yyy')
u'05 12 1987'
format_datetime(datetime(1987, 3, 5, 17, 12), 'dd mm yyyy')
u'05 12 1987'
And again with a different language:

app.config['BABEL_DEFAULT_LOCALE'] = 'de'
from flask_babel import refresh; refresh()
format_datetime(datetime(1987, 3, 5, 17, 12), 'EEEE, d. MMMM yyyy H:mm')
u'Donnerstag, 5. M\xe4rz 1987 17:12'
For more format examples head over to the babel documentation.

Formatting Numbers
To format numbers you can use the format_number(), format_decimal(), format_currency(), format_percent() and format_scientific() functions.

To play with the date formatting from the console, you can use the test_request_context() method:

app.test_request_context().push()
Here are some examples:

from flask_babel import format_number
format_number(1099)
'1,099'
from flask_babel import format_decimal
format_decimal(1.2346)
u'1.235'
from flask_babel import format_currency
format_currency(1099.98, 'USD')
'$1,099.98'
from flask_babel import format_percent
format_percent(0.34)
'34%'
from flask_babel import format_scientific
format_scientific(10000)
'1E4'
And again with a different language:

app.config['BABEL_DEFAULT_LOCALE'] = 'de'
from flask_babel import refresh; refresh()
format_number(1099)
'1.099'
format_decimal(1.2346)
'1,235'
format_currency(1099.98, 'USD')
'1.099,98\xa0$'
format_percent(0.34)
'34\xa0%'
format_scientific(10000)
'1E4'
For more format examples head over to the babel documentation.

Using Translations
The other big part next to date formatting are translations. For that, Flask uses gettext together with Babel. The idea of gettext is that you can mark certain strings as translatable and a tool will pick all those up, collect them in a separate file for you to translate. At runtime the original strings (which should be English) will be replaced by the language you selected.

There are two functions responsible for translating: gettext() and ngettext(). The first to translate singular strings and the second to translate strings that might become plural. Here some examples:

from flask_babel import gettext, ngettext

gettext(u'A simple string')
gettext(u'Value: %(value)s', value=42)
ngettext(u'%(num)s Apple', u'%(num)s Apples', number_of_apples)
Additionally if you want to use constant strings somewhere in your application and define them outside of a request, you can use a lazy strings. Lazy strings will not be evaluated until they are actually used. To use such a lazy string, use the lazy_gettext() function:

from flask_babel import lazy_gettext

class MyForm(formlibrary.FormBase):
    success_message = lazy_gettext(u'The form was successfully saved.')
So how does Flask-Babel find the translations? Well first you have to create some. Here is how you do it:

Translating Applications
First you need to mark all the strings you want to translate in your application with gettext() or ngettext(). After that, it’s time to create a .pot file. A .pot file contains all the strings and is the template for a .po file which contains the translated strings. Babel can do all that for you.

First of all you have to get into the folder where you have your application and create a mapping file. For typical Flask applications, this is what you want in there:

[python: **.py]
[jinja2: **/templates/**.html]
extensions=jinja2.ext.autoescape,jinja2.ext.with_
Save it as babel.cfg or something similar next to your application. Then it’s time to run the pybabel command that comes with Babel to extract your strings:

$ pybabel extract -F babel.cfg -o messages.pot .
If you are using the lazy_gettext() function you should tell pybabel that it should also look for such function calls:

$ pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
This will use the mapping from the babel.cfg file and store the generated template in messages.pot. Now we can create the first translation. For example to translate to German use this command:

$ pybabel init -i messages.pot -d translations -l de
-d translations tells pybabel to store the translations in this folder. This is where Flask-Babel will look for translations. Put it next to your template folder.

Now edit the translations/de/LC_MESSAGES/messages.po file as needed. Check out some gettext tutorials if you feel lost.

To compile the translations for use, pybabel helps again:

$ pybabel compile -d translations
What if the strings change? Create a new messages.pot like above and then let pybabel merge the changes:

$ pybabel update -i messages.pot -d translations
Afterwards some strings might be marked as fuzzy (where it tried to figure out if a translation matched a changed key). If you have fuzzy entries, make sure to check them by hand and remove the fuzzy flag before compiling.

Troubleshooting
On Snow Leopard pybabel will most likely fail with an exception. If this happens, check if this command outputs UTF-8:

$ echo $LC_CTYPE
UTF-8
This is a OS X bug unfortunately. To fix it, put the following lines into your ~/.profile file:

export LC_CTYPE=en_US.utf-8
Then restart your terminal.

API
This part of the documentation documents each and every public class or function from Flask-Babel.

Configuration
class flask_babel.Babel(app=None, default_locale='en', default_timezone='UTC', default_domain='messages', date_formats=None, configure_jinja=True)[source]
Central controller class that can be used to configure how Flask-Babel behaves. Each application that wants to use Flask-Babel has to create, or run init_app() on, an instance of this class after the configuration was initialized.

property default_locale
The default locale from the configuration as instance of a babel.Locale object.

property default_timezone
The default timezone from the configuration as instance of a pytz.timezone object.

property domain
The message domain for the translations as a string.

domain_instance[source]
The message domain for the translations.

init_app(app)[source]
Set up this instance for use with app, if no app was passed to the constructor.

list_translations()[source]
Returns a list of all the locales translations exist for. The list returned will be filled with actual locale objects and not just strings.

New in version 0.6.

localeselector(f)[source]
Registers a callback function for locale selection. The default behaves as if a function was registered that returns None all the time. If None is returned, the locale falls back to the one from the configuration.

This has to return the locale as string (eg: 'de_AT', 'en_US')

timezoneselector(f)[source]
Registers a callback function for timezone selection. The default behaves as if a function was registered that returns None all the time. If None is returned, the timezone falls back to the one from the configuration.

This has to return the timezone as string (eg: 'Europe/Vienna')

Context Functions
flask_babel.get_translations()[source]
Returns the correct gettext translations that should be used for this request. This will never fail and return a dummy translation object if used outside of the request or if a translation cannot be found.

flask_babel.get_locale()[source]
Returns the locale that should be used for this request as babel.Locale object. This returns None if used outside of a request.

flask_babel.get_timezone()[source]
Returns the timezone that should be used for this request as pytz.timezone object. This returns None if used outside of a request.

Datetime Functions
flask_babel.to_user_timezone(datetime)[source]
Convert a datetime object to the user’s timezone. This automatically happens on all date formatting unless rebasing is disabled. If you need to convert a datetime.datetime object at any time to the user’s timezone (as returned by get_timezone() this function can be used).

flask_babel.to_utc(datetime)[source]
Convert a datetime object to UTC and drop tzinfo. This is the opposite operation to to_user_timezone().

flask_babel.format_datetime(datetime=None, format=None, rebase=True)[source]
Return a date formatted according to the given pattern. If no datetime object is passed, the current time is assumed. By default rebasing happens which causes the object to be converted to the users’s timezone (as returned by to_user_timezone()). This function formats both date and time.

The format parameter can either be 'short', 'medium', 'long' or 'full' (in which cause the language’s default for that setting is used, or the default from the Babel.date_formats mapping is used) or a format string as documented by Babel.

This function is also available in the template context as filter named datetimeformat.

flask_babel.format_date(date=None, format=None, rebase=True)[source]
Return a date formatted according to the given pattern. If no datetime or date object is passed, the current time is assumed. By default rebasing happens which causes the object to be converted to the users’s timezone (as returned by to_user_timezone()). This function only formats the date part of a datetime object.

The format parameter can either be 'short', 'medium', 'long' or 'full' (in which cause the language’s default for that setting is used, or the default from the Babel.date_formats mapping is used) or a format string as documented by Babel.

This function is also available in the template context as filter named dateformat.

flask_babel.format_time(time=None, format=None, rebase=True)[source]
Return a time formatted according to the given pattern. If no datetime object is passed, the current time is assumed. By default rebasing happens which causes the object to be converted to the users’s timezone (as returned by to_user_timezone()). This function formats both date and time.

The format parameter can either be 'short', 'medium', 'long' or 'full' (in which cause the language’s default for that setting is used, or the default from the Babel.date_formats mapping is used) or a format string as documented by Babel.

This function is also available in the template context as filter named timeformat.

flask_babel.format_timedelta(datetime_or_timedelta, granularity='second', add_direction=False, threshold=0.85)[source]
Format the elapsed time from the given date to now or the given timedelta.

This function is also available in the template context as filter named timedeltaformat.

Number Functions
flask_babel.format_number(number)[source]
Return the given number formatted for the locale in request

Parameters
number – the number to format

Returns
the formatted number

Return type
unicode

flask_babel.format_decimal(number, format=None)[source]
Return the given decimal number formatted for the locale in request

Parameters
number – the number to format

format – the format to use

Returns
the formatted number

Return type
unicode

flask_babel.format_currency(number, currency, format=None, currency_digits=True, format_type='standard')[source]
Return the given number formatted for the locale in request

Parameters
number – the number to format

currency – the currency code

format – the format to use

currency_digits – use the currency’s number of decimal digits [default: True]

format_type – the currency format type to use [default: standard]

Returns
the formatted number

Return type
unicode

flask_babel.format_percent(number, format=None)[source]
Return formatted percent value for the locale in request

Parameters
number – the number to format

format – the format to use

Returns
the formatted percent number

Return type
unicode

flask_babel.format_scientific(number, format=None)[source]
Return value formatted in scientific notation for the locale in request

Parameters
number – the number to format

format – the format to use

Returns
the formatted percent number

Return type
unicode

Gettext Functions
flask_babel.gettext(*args, **kwargs)[source]
flask_babel.ngettext(*args, **kwargs)[source]
flask_babel.pgettext(*args, **kwargs)[source]
flask_babel.npgettext(*args, **kwargs)[source]
flask_babel.lazy_gettext(*args, **kwargs)[source]
flask_babel.lazy_pgettext(*args, **kwargs)[source]
Low-Level API
flask_babel.refresh()[source]
Refreshes the cached timezones and locale information. This can be used to switch a translation between a request and if you want the changes to take place immediately, not just with the next request:

user.timezone = request.form['timezone']
user.locale = request.form['locale']
refresh()
flash(gettext('Language was changed'))
Without that refresh, the flash() function would probably return English text and a now German page.

flask_babel.force_locale(locale)[source]
Temporarily overrides the currently selected locale.

Sometimes it is useful to switch the current locale to different one, do some tasks and then revert back to the original one. For example, if the user uses German on the web site, but you want to send them an email in English, you can use this function as a context manager:

with force_locale('en_US'):
    send_email(gettext('Hello!'), ...)
Parameters
locale – The locale to temporary switch to (ex: ‘en_US’).
