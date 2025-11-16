                                          models.py

"""                            AbstractUser                                           """
- In my project i am using AbstractUser rather than django built in User model. The reason for this is that in User model the fields are limited and i cant add new fields
of my own. I cant use Email as username, Control authentication logic is limited. And it is not future proof(i cant swap user models later, as its going to be hectic)

- Why am i using AbstractUser? It gives me all built-in authentication features and also gives me the ability to customize fields and behavior
- AbstractUser alraedy have "username, email, password, first_name, last_name", adding extra fields only extends it.

Why this is better:

- You let Django handle authentication, password hashing, and validation.
- You only add the extra fields that are truly unique to your project.
- You don’t duplicate fields like email or is_active.

AUTH_USER_MODEL vs get_user_model() when to user what?

- inside models.py use settings.AUTH_USER_MODEL (for foreignkey or one to one) because:
  - its a string (eg. AccountsApp.Users) and Django resolves it lazily (no circular import issues)
  - not use get_user_model() here because it returns the actual class, and if you load it too early (while django is loading other models), it causes circular import errors



                                            views.py

- i am creating user with create_user() rather than create. create_user() automatically calls set_password(), which hashes
