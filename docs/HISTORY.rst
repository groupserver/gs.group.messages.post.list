Changelog
=========

4.3.2 (2016-02-02)
------------------

* Following the update to `gs.search.base`_
* Updating the JavaScript that loads the *Posts* tab so it passes
  the `Google Closure Linter`_
* Adding some unit tests

.. _gs.search.base: https://github.com/groupserver/gs.search.base
.. _Google Closure Linter:
   https://developers.google.com/closure/utilities/

4.3.1 (2015-11-12)
------------------

* Following the updates to `gs.content.js.sharebox`_
* Running `gjslint`_ over the JavaScript resources

.. _gs.content.js.sharebox:
   https://github.com/groupserver/gs.content.js.sharebox
.. _gjslint:
   https://developers.google.com/closure/utilities/docs/linter_howto

4.3.0 (2015-10-15)
------------------

* Renaming the product ``gs.group.messages.post.list``, to bring
  it in with the refactor of `gs.group.messages.post.base`_

.. _gs.group.messages.post.base:
   https://github.com/groupserver/gs.group.messages.post.base/

4.2.7 (2015-09-21)
------------------

* [DE] Updating the German translation, thanks to Cousin Clara

4.2.6 (2015-04-28)
------------------

* Removing ``role="application"``, closing  `Bug 4156`_

.. _Bug 4156: https://redmine.iopen.net/issues/4156

4.2.5 (2015-03-11)
------------------

* [FR] Adding a French translation, thanks to `Razique Mahroua`_

.. _Razique Mahroua:
   https://www.transifex.com/accounts/profile/Razique/

4.2.4 (2015-02-27)
------------------

* Adding internationalisation support
* Pointing the product at Transifex_

.. _Transifex:
   https://www.transifex.com/groupserver/gs-group-messages-post-list/

4.2.3 (2014-10-10)
------------------

* Switching to GitHub_ as the primary code repository, and naming
  the reStructuredText files as such

.. _GitHub:
   https://github.com/groupserver/gs.group.messages.post.list/

4.2.2 (2014-06-24)
------------------

* Refactor of the *Posts* tab to make it WAI-ARIA compliant

4.2.1 (2014-03-13)
------------------

* Switching to ``"use strict";`` in the JavaScript
* Unicode and general code cleanup

4.2.0 (2013-11-26)
------------------

* Using the new loading-character
* Adding a *failed* state to the page-template
* Following the new core JavaScript search code

4.1.0 (2013-06-06)
------------------

* Adding the ATOM-feed icon to the *Posts* tab

4.0.1 (2013-03-22)
------------------

* Using a better URL for the post-link
* Minifying the JavaScript libraries

4.0.0 (2013-02-20)
------------------

* Switch to Twitter Bootstrap (``gs.content.js.bootstrap``) from
  JQuery.UI
* Deferring loading of the JavaScript
* Using the new JavaScript loader (``gs.content.js.loader``) to
  load the search JS

3.0.0 (2012-09-26)
------------------

* Using full-text retrieval (FTR) to perform the search
* Moved the queries here from ``Products.XWFMailingListManager``

2.1.1 (2012-06-22)
------------------

* Update to SQLAlchemy

2.1.0 (2012-06-06)
------------------

* Rely on ``gs.group.messages.base`` to supply the core
  JavaScript
* Only load the posts when the *Posts* tab is selected

2.0.0 (2012-05-15)
------------------

* Initial version (was part of ``gs.group.messages.post``,
  singular)

..  LocalWords:  Changelog Transifex GitHub reStructuredText
