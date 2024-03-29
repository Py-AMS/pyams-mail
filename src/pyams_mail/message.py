#
# Copyright (c) 2008-2015 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_mail.message module

This module provides classes which can automatically generate text part of an HTML message.
"""

import codecs
from html import entities

from pyramid_mailer.message import Message

from pyams_utils.html import html_to_text


__docformat__ = 'restructuredtext'


def html_replace(exc):
    """Handle HTML conversion exceptions"""
    if isinstance(exc, (UnicodeEncodeError, UnicodeTranslateError)):
        # pylint: disable=invalid-name
        s = ['&%s;' % entities.codepoint2name[ord(c)] for c in exc.object[exc.start:exc.end]]
        return ''.join(s), exc.end
    raise TypeError("Can't handle exception %s" % exc.__name__)


codecs.register_error('html_replace', html_replace)


def html_encode(unicode_data, encoding='utf-8'):
    """Encode HTML"""
    return unicode_data.encode(encoding, 'html_replace')


def HTMLMessage(subject, from_addr, to_addr, html,
                text=None, encoding='utf-8', reply_to=None,
                cc=None, bcc=None, extra_headers=None, attachments=None):
    # pylint: disable=invalid-name,too-many-arguments
    """Create a MIME message that will render as HTML or text"""
    html = html_encode(html, encoding).decode(encoding)
    if text is None:
        # produce textual rendering of the HTML string when None is provided
        text = html_to_text(html)
    if isinstance(to_addr, str):
        to_addr = (to_addr,)
    headers = extra_headers or {}
    if reply_to:
        headers['Reply-To'] = reply_to
    return Message(subject=subject,
                   sender=from_addr,
                   recipients=to_addr,
                   html=html,
                   body=text,
                   cc=cc,
                   bcc=bcc,
                   extra_headers=headers,
                   attachments=attachments)


def TextMessage(subject, from_addr, to_addr, text, reply_to=None,
                cc=None, bcc=None, extra_headers=None, attachments=None):
    # pylint: disable=invalid-name
    """Create a text message"""
    if isinstance(to_addr, str):
        to_addr = (to_addr,)
    headers = extra_headers or {}
    if reply_to:
        headers['Reply-To'] = reply_to
    return Message(subject=subject,
                   sender=from_addr,
                   recipients=to_addr,
                   body=text,
                   cc=cc,
                   bcc=bcc,
                   extra_headers=headers,
                   attachments=attachments)
