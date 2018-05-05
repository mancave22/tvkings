# -*- coding: utf-8 -*-

'''
        License summary below, for more details please read license.txt file

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 2 of the License, or
        (at your option) any later version.
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from tulip.control import setting, selectDialog, lang, condVisibility
from tulip.init import *


try:
    from urllib import unquote_plus
except ImportError:
    from urllib.parse import unquote_plus

action = params.get('action')
url = params.get('url')


def pair_tool(dialog=False):

    items = [
        {
            'title': '[COLORwhite][B]OPENLOAD[/COLOR][/B]',
            'url': 'https://olpair.com/',
            'icon': 'openload.png'
        }
        ,
        {
            'title': '[COLORwhite][B]THE VIDEO[/COLOR][/B]',
            'url': 'https://thevideo.cc/pair',
            'icon': 'thevideo.png'
        }
        ,
        {
            'title': '[COLORwhite][B]VIDUP[/COLOR][/B]',
            'url': 'https://vidup.me/pair',
            'icon': 'vidup.png'
        }
        ,
        {
            'title': '[COLORwhite][B]STREAMANGO[/COLOR][/B]',
            'url':'https://streamango.com/pair',
            'icon': 'streamango.jpg'
        }
        ,
        {
            'title': '[COLORwhite][B]FLASHX[/COLOR][/B]',
            'url': 'https://www.flashx.tv/pairing.php',
            'icon': 'flashx.png'
        }
    ]

    for i in items:
        i.update({'action': 'pair'})

    if not dialog:

        from tulip import directory
        directory.add(items)

    else:

        choice = selectDialog([i['title'] for i in items], lang(30004))

        if choice >= 0:

            selection = [i['url'] for i in items][choice]
            pair(selection)


def pair(link):

    link = unquote_plus(link)

    if condVisibility('system.platform.android'):
        from tulip.control import android_activity
        android_activity(link)
    else:
        import webbrowser
        webbrowser.open(link)


if action is None:

    pair_tool(dialog=True if setting('dialog') == 'true' else False)

elif action == 'pair':

    pair(url)
