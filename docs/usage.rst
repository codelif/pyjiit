Usage
=====

This section covers general usage of the API.

Installing
----------

To get started, install the package using pip

.. code-block:: Bash    

  pip install pyjiit


Instantiation
-------------

.. code-block:: Python

   from pyjiit import Webportal

   w = Webportal()
   print(w)
   # Output:
   # Driver Class for JIIT Webportal

pretty self-explanatory ig

Logging in
----------

.. code-block:: Python

  from pyjiit import Webportal
  from pyjiit.default import CAPTCHA


  w = Webportal()
  s = w.student_login("username", "password", CAPTCHA)
  print(w.session.clientid)

  # Output:
  # JAYPEE


This calls the :code:`student_login` method with username, password and CAPTCHA

The login method needs the Captcha object as well to defend against bots.
But in practice, the captcha is not really tied to any state with your IP, so you can send any prefilled captcha and woohoo!!

So there is a premade CAPTCHA object in :code:`pyjiit.default`, which can be used while logging in


Changing the password
---------------------

.. code-block:: Python

  from pyjiit import Webportal
  from pyjiit.default import CAPTCHA


  w = Webportal()
  w.student_login("username", "password", CAPTCHA)
  w.set_password("password", "password_strong")

As usual we login and use the required method


Getting the attendance
----------------------

.. code-block:: Python

  # instantiate w = Webportal() and login before this
  
  meta = w.get_attendance_meta()
  header = meta.latest_header()
  sem = meta.latest_semester()

  print(w.get_attendance(header, sem))

  # Output:
  # {'currentSem': '1',
  #  'studentattendancelist': [{'LTpercantage': 83.3,
  #                           'Lpercentage': 92.9,
  #                           'Lprepercentage': 0.0,
  #                           'Lpretotalclass': 0.0,
  #                           'Lpretotalpres': 0.0,
  #                           'Lsubjectcomponentcode': 'L',
  #                           'Lsubjectcomponentid': 'JISCP19050000001',
  # ...
  # ...
  # ... many rows
  # }

You first get the metadata for the attendance which contains headers (courseid, etc) and semesters.
:code:`get_attendance_meta()` returns an instance of :code:`AttendanceMeta` object which contains a list of available headers and semester.

The methods :code:`latest_header()` and :code:`latest_semester()` are self-explanatory.

You can choose any other header and semester from the lists :code:`AttendanceMeta.headers` and :code:`AttendanceMeta.semesters`. 

.. note::

   Please note that the call to :code:`get_attendance` may take over 10 seconds to complete. This wait is from the server so nothing we can do, sadly ;( 



Getting Subject detail
----------------------

.. code-block:: Python

  # instantiate w = Webportal() and login before this

  semesters = w.get_registered_semesters()
  sem = semesters[-1] # get latest sem

  reg = w.get_registered_subjects_and_faculties(sem)
  print(*reg.subjects, sep="\n")
  
  # Output:
  # RegisteredSubject(employee_name='Teacher name', employee_code='SomeCode', minor_subject='N', remarks='REG', stytype='REG', credits=4.0, subject_code='15B11CI111', subject_component_code='T', subject_desc='SOFTWARE DEVELOPMENT FUNDAMENTALS-1', subject_id='150046', audtsubject='N')
  # ...
  # ... more rows

  print(reg.total_credits)

  # Output:
  22.5

We first get semester list and call the method with semester of choice.

The method :code:`get_registered_subjects_and_faculties` returns an instance of :code:`Registrations` class. 

Exception Handling
------------------

There several exceptions that might be raised during the use of the API. One such exception is :code:`NotLoggedIn`, which is raised when you try to call a method on :code:`Webportal`, which needs authorization (student_login). Like calling :code:`get_student_bank_info` before :code:`student_login` is first called.


There are many more uses of the API, refer to next section for full API reference.
