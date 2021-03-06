===================
 django-discussion
===================
------------------------------------------
 A Facebook group style discussion forum.
------------------------------------------

*Note*: Requires authentication

Installation
------------

::

  pip install django-discussion

Configuration
-------------

JS/CSS
======

Example CSS and script references are commented out in the base template.
Example CSS is compiled from SASS, so make any changes in the SASS and re-compile the CSS file.

The default AJAX/javascript require three jQuery libraries:
  * jquery.autogrow.js
    commit 8d632548aad3f07269adf03d4a47b7f2c3c7965c
    https://github.com/jaz303/jquery-grab-bag/blob/master/javascripts/jquery.autogrow-textarea.js
  * jquery.placeholder.js
    commit #47c4a3c89eed697d843a004034f7a33d555a1353
    https://github.com/danielstocks/jQuery-Placeholder
  * jquery.form.js
    v3.01
    https://github.com/malsup/form/

Settings
========

DISCUSSION_UPLOAD_EXTENSIONS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A Whitelist of file extensions that can be uploaded to a discussion.
If this is set to ``[]``, no uploads will be accepted.
If it is set to ``None``, the whitelist will not be used.

Default::

  DISCUSSION_UPLOAD_EXTENSIONS = [
      'odt', 'odf', 'odp',  # Open/LibreOffice
      'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',  # MS Office
      'pdf', 'gif', 'jpg', 'jpeg', 'png',  # Other sane defaults...
  ]
