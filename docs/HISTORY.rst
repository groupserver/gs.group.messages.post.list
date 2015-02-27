Changelog
=========

4.2.4 (2015-02-27)
------------------

* Adding internationalisation support
* Pointing the product at Transifex_

4.2.3 (2014-10-10)
------------------

* Switching to GitHub_ as the primary code repository, and naming
  the reStructuredText files as such

.. _GitHub:
   https://github.com/groupserver/gs.group.messages.posts/

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
