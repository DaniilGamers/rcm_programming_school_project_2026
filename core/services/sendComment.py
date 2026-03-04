from apps.orders.models import CommentModel


class SendCommentService:
    @staticmethod
    def send_comment(order, user, text):

        CommentModel.objects.create(
            order=order,
            text=text,
            sender_name=user.name + ' ' + user.surname
        )

        if not order.manager:
            order.manager = user.name

        if order.status in (None, "New"):
            order.status = "In Work"

        order.save()
