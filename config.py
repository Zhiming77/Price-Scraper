from decouple import config


credentials = {}

credentials['sender_password'] = config('sender-password')
credentials['sender_email'] = config('sender-email')
credentials['recipient_email'] = config('recipient-email')
credentials['SMTP_config'] = config('SMTP-config')
credentials['SMTP_port'] = config('SMTP-port')
