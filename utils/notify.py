from django.contrib import messages

class Notify:
    @staticmethod
    def __levels() -> dict:
        return {
            'success':messages.SUCCESS,
            'warning':messages.WARNING,
            'error':messages.ERROR,
            'info':messages.INFO,
            'critical':messages.ERROR,
        }

    @staticmethod
    def notify(*, request, message, level='success'):
        messages.add_message(
            request,
            Notify.__levels().get(level, messages.SUCCESS),
            message,
        )