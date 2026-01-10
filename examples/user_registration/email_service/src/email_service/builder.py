import email
import email.message


def get_email_payload(recipient: str) -> str:
    return (
        f"Thanks for registering, {recipient}!\n"    
        "\n"
        "Normally, we would give you a confirmation code or link to verify your account, "
        "but this is just an example project and we don't have a functionality for this yet.\n"
        "\n"
        "So let's just think you're already verified and yada-yada. We trust ya."
    )


def build_email(sender: str, recipient: str) -> bytes:
    message = email.message.EmailMessage()
    
    message.add_header("From", sender)
    message.add_header("To", recipient)
    message.add_header("Subject", "Confirm your registration")
    
    payload = get_email_payload(recipient)
    message.set_payload(payload)
    message.set_charset("utf-8")
    return message.as_bytes()
