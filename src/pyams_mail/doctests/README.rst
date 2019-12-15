==================
PyAMS_mail package
==================

Introduction
------------

This package is composed of a set of utility functions, usable into any Pyramid application.

    >>> from pyramid.testing import setUp, tearDown
    >>> config = setUp()


HTML messages
-------------

An HTML message is a multipart MIME message which provides HTML and text versions of the same
test:

    >>> from pyams_mail.message import HTMLMessage, TextMessage
    >>> body = '<p>This is my message body</p>'
    >>> message = HTMLMessage(subject='Test message',
    ...                       fromaddr='testing@example.com',
    ...                       toaddr='john.doe@example.com',
    ...                       html=body)

    >>> message
    <pyramid_mailer.message.Message object at 0x...>
    >>> message.validate()

    >>> message.subject
    'Test message'
    >>> message.sender
    'testing@example.com'
    >>> message.recipients
    ('john.doe@example.com',)
    >>> message.html
    '<p>This is my message body</p>'
    >>> message.body
    'This is my message body\n'

It can then be converted to an email message which will be used by a mailer utility:

    >>> msg = message.to_message()
    >>> msg
    <email.mime.multipart.MIMEMultipart object at 0x...>
    >>> msg.is_multipart()
    True
    >>> msg.get_content_type()
    'multipart/alternative'
    >>> sorted(msg.keys())
    ['Content-Type', 'From', 'MIME-Version', 'Subject', 'To']
    >>> payload = msg.get_payload()
    >>> payload
    [<...MIMENonMultipart object at 0x...>, <...MIMENonMultipart object at 0x...>]

    >>> part = payload[0]
    >>> part.get_content_type()
    'text/plain'
    >>> part.get_payload(decode=True)
    b'This is my message body\n'
    >>> part.get_charset()
    us-ascii

    >>> part = payload[1]
    >>> part.get_content_type()
    'text/html'
    >>> part.get_payload(decode=True)
    b'<p>This is my message body</p>'
    >>> part.get_charset()
    us-ascii

Tests cleanup:

    >>> tearDown()
