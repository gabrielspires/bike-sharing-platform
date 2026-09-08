from celery import shared_task
from decouple import config
from django.core.mail import send_mail
from django.db import DatabaseError

from .models import Trip


@shared_task(
    autoretry_for=(DatabaseError, Exception),
    max_retries=20,
    retry_backoff=True,
)
def finish_trip(trip_id: str) -> int:
    """Task to send an e-mail notification when a bike trip is finished."""
    trip = Trip.objects.get(id=trip_id)

    subject = "Obrigado por pedalar com a gente! Confira os dados da sua viagem."
    message = (
        f"Prezado {trip.user.first_name},\n\nVocê conclui com sucesso a sua viagem.\n\n"
        + f"Id da viagem: {trip.id}.\n"
        + f"Horário de início: {trip.created_at}\n"
        + f"Horário de término: {trip.finished_at}\n\n"
        + "Não se esqueça de avaliar a sua viagem no app!"
    )
    mail_sent = send_mail(
        subject,
        message,
        from_email=config("TRIP_CONFIRMATION_SENDER"),
        recipient_list=[trip.user.email],
    )
    return mail_sent
