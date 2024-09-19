Introduction
============

**pyjiit** is a Python library for accessing data from JIIT Webportal. It uses the internal APIs of JIIT Webportal to programattically access the data. It can be used in various types of projects which require getting attendance data or general student information (like results, registration, etc).

.. note::

   The data provided by the APIs is only as correct as provided on https://webportal.jiit.ac.in:6011/studentportal/


Features
--------

* Login and Session management (with invalidation)
* Attendance data queries
* Subject registration data
* Exam event data
* Explicit exceptions
* Happiness

Roadmap
-------

* :code:`Webportal` instantiation with :code:`WebportalSession` (for cached sessions)
* Cover more endpoints
* Drink water
* Sleep more than 2 hours in a day
* Meetup with the people who designed JIIT Webportal
* Heavily judge their design choices


Dependencies
------------

* requests
* pycryptodome (this is explicit for very interesting reasons)
* NESCAFE
* `Dopamine Dose`_

.. _Dopamine Dose: https://open.spotify.com/playlist/3MD5jRlnXlLrMacF9rirOv?si=pH4WlKBPRyaJUokQwoehnA


