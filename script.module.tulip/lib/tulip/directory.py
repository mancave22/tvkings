# -*- coding: utf-8 -*-

'''
    Tulip routine libraries, based on lambda's lamlib
    Author Twilight0

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

try:
    from urllib import quote_plus, urlencode
except ImportError:
    from urllib.parse import quote_plus, urlencode
from . import control
from .init import sysaddon, syshandle


def add(items, cacheToDisc=True, content=None, mediatype=None, infotype='video'):

    if items is None or len(items) == 0:
        return

    # sysicon = control.join(control.addonInfo('path'), 'resources', 'media')
    sysimage = control.addonInfo('icon')
    sysfanart = control.addonInfo('fanart')

    for i in items:

        try:

            try:
                label = control.lang(i['title']).encode('utf-8')
            except BaseException:
                label = i['title']

            if 'label' in i and not i['label'] == '0':
                label = i['label']

            if 'image' in i and not i['image'] == '0':
                image = i['image']
            elif 'poster' in i and not i['poster'] == '0':
                image = i['poster']
            elif 'icon' in i and not i['icon'] == '0':
                image = control.addonmedia(i['icon'])
            else:
                image = sysimage

            if 'banner' in i and not i['banner'] == '0':
                banner = i['banner']
            elif 'fanart' in i and not i['fanart'] == '0':
                banner = i['fanart']
            else:
                banner = image

            fanart = i['fanart'] if 'fanart' in i and not i['fanart'] == '0' else sysfanart

            isFolder = False if 'isFolder' in i and not i['isFolder'] == '0' else True

            url = '%s?action=%s' % (sysaddon, i['action'])

            try:
                url += '&url=%s' % quote_plus(i['url'])
            except BaseException:
                pass
            try:
                url += '&image=%s' % quote_plus(i['image'])
            except BaseException:
                pass
            try:
                url += '&title=%s' % quote_plus(i['title'].encode('utf-8'))
            except BaseException:
                pass
            try:
                url += '&name=%s' % quote_plus(i['name'].encode('utf-8'))
            except BaseException:
                pass
            try:
                url += '&plot=%s' % quote_plus(i['plot'].encode('utf-8'))
            except BaseException:
                pass
            try:
                url += '&genre=%s' % quote_plus(i['genre'])
            except BaseException:
                pass
            try:
                url += '&dash=%s' % quote_plus(i['dash'])
            except BaseException:
                pass
            try:
                url += '&query=%s' % quote_plus(i['query'])
            except BaseException:
                pass

            cm = []
            menus = i['cm'] if 'cm' in i else []

            for menu in menus:
                try:
                    try:
                        tmenu = control.lang(menu['title']).encode('utf-8')
                    except BaseException:
                        tmenu = menu['title']
                    qmenu = urlencode(menu['query'])
                    cm.append((tmenu, 'RunPlugin(%s?%s)' % (sysaddon, qmenu)))
                except BaseException:
                    pass

            meta = dict((k, v) for k, v in i.iteritems() if not k == 'cm' and not v == '0')

            if mediatype is not None:
                meta['mediatype'] = mediatype

            item = control.item(label=label, iconImage=image, thumbnailImage=image)

            item.setArt(
                {
                    'icon': image, 'thumb': image, 'poster': image, 'tvshow.poster': image, 'season.poster': image,
                    'banner': banner, 'tvshow.banner': banner, 'season.banner': banner
                }
            )

            item.setProperty('Fanart_Image', fanart)

            item.addContextMenuItems(cm)
            item.setInfo(type=infotype, infoLabels=meta)

            if isFolder is False:
                if not i['action'] == 'pvr_client':
                    item.setProperty('IsPlayable', 'true')
                else:
                    item.setProperty('IsPlayable', 'false')
                if not i['action'] == 'pvr_client' and infotype == 'video':
                    item.addStreamInfo('video', {'codec': 'h264'})

            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder, totalItems=len(items))

        except BaseException:

            pass

    try:

        i = items[0]
        if i['next'] == '':
            raise Exception()

        url = '%s?action=%s&url=%s' % (sysaddon, i['nextaction'], quote_plus(i['next']))
        icon = i['nexticon'] if 'nexticon' in i else control.addonmedia('next.png')
        fanart = i['nextfanart'] if 'nextfanart' in i else sysfanart

        try:
            label = control.lang(i['nextlabel']).encode('utf-8')
        except BaseException:
            label = 'next'

        item = control.item(label=label, iconImage=icon, thumbnailImage=icon)

        item.setArt(
            {
                'icon': icon, 'thumb': icon, 'poster': icon, 'tvshow.poster': icon, 'season.poster': icon,
                'banner': icon, 'tvshow.banner': icon, 'season.banner': icon
            }
        )

        item.setProperty('Fanart_Image', fanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True, totalItems=len(items))
    except BaseException:
        pass

    if content is not None:
        control.content(syshandle, content)

    control.directory(syshandle, cacheToDisc=cacheToDisc)


def resolve(url, meta=None, icon=None, dash=False):

    item = control.item(path=url)

    if not icon is None:
        item.setArt({'icon': icon, 'thumb': icon})

    if meta is not None:
        item.setInfo(type='Video', infoLabels=meta)

    xbmc_python_ver = int(control.infoLabel('System.AddonVersion(xbmc.python)').replace('.', ''))

    try:
        ias_enabled = control.addon_details('inputstream.adaptive').get('enabled')
    except KeyError:
        ias_enabled = False

    if dash and xbmc_python_ver >= 2250 and ias_enabled:
        item.setContentLookup(False)
        item.setMimeType('application/xml+dash')
        item.setProperty('inputstreamaddon', 'inputstream.adaptive')
        item.setProperty('inputstream.adaptive.manifest_type', 'mpd')
    else:
        pass

    control.resolve(syshandle, True, item)
