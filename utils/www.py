

def check_email_adress(email):
    message = [True, 'email adress is OK']
    # Make sure it's a string
    if not isinstance(email, str):
        message = [False, 'email adress is not a string']

    # Make sure it has @
    if ('@' not in email) or ('.' not in email):
        message = [False, 'email adress is not a valid string']

    # Make sure has suffix
    splt = email.split('.')
    if any(len(i_)==0 for i_ in splt):
        message = [False, 'email adress is not a valid string']

    return message


