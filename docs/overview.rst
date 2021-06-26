Overview
========

Abstract models contain all the necessary variables, attributes and methods,
except foreign keys which are implemented in the concrete models. Concrete
models inherit everything from the abstract models. You can use these concrete
models directly or override them.

The admin follows the same philosophy as the models.

Primary objects are instances with the ``is_primary`` attribute set to ``True``.
Usually these objects are not deletable because they are used to keep data
integrity. For example a person must have at least one address and telephone
number and if you want to delete the address, or the telephone number
you must delete the whole person. If you have multiple addresses you can change
the primary address and then execute a deletion.
