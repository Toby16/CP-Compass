from email_validator import validate_email, EmailNotValidError


def email_validator(usr_email):
    try:
        emailinfo = validate_email(usr_email, check_deliverability=False)
        return emailinfo.normalized
    except EmailNotValidError as e:
        return {
            "statusCode": 400,
            "error": str(e)
        }
    except exception as e:
        raise
