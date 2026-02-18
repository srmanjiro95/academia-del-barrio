import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings
from app.schemas.gym import GymMember


def send_registration_email(member: GymMember) -> None:
    subject = "Tu registro en Academia del Barrio"
    html = _registration_template(member)
    _send_email(member.email, subject, html)


def send_qr_refresh_email(member: GymMember) -> None:
    subject = "Tu nuevo código QR de acceso"
    html = _qr_refresh_template(member)
    _send_email(member.email, subject, html)


def _send_email(to_email: str, subject: str, html: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.smtp_from_email
    msg["To"] = to_email
    msg.attach(MIMEText(html, "html", "utf-8"))

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        if settings.smtp_use_tls:
            server.starttls()
        if settings.smtp_username and settings.smtp_password:
            server.login(settings.smtp_username, settings.smtp_password)
        server.sendmail(settings.smtp_from_email, [to_email], msg.as_string())


def _registration_template(member: GymMember) -> str:
    return f"""
<!doctype html>
<html>
  <body style=\"margin:0;padding:0;background:#f5f5f5;font-family:Arial,sans-serif;\">
    <table role=\"presentation\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" style=\"background:#f5f5f5;padding:20px 0;\">
      <tr>
        <td align=\"center\">
          <table role=\"presentation\" width=\"600\" cellpadding=\"0\" cellspacing=\"0\" style=\"max-width:600px;background:#ffffff;border-radius:8px;overflow:hidden;\">
            <tr><td style=\"background:#111827;color:#fff;padding:20px;font-size:22px;font-weight:bold;\">Academia del Barrio</td></tr>
            <tr><td style=\"padding:24px;color:#111827;\">
              <h2 style=\"margin:0 0 12px;\">¡Registro exitoso, {member.first_name}!</h2>
              <p style=\"margin:0 0 16px;\">Tu membresía ha sido registrada correctamente.</p>
              <table role=\"presentation\" width=\"100%\" cellpadding=\"8\" cellspacing=\"0\" style=\"border:1px solid #e5e7eb;border-collapse:collapse;\">
                <tr><td style=\"background:#f9fafb;\"><b>Membresía</b></td><td>{member.membership_name or '-'}</td></tr>
                <tr><td style=\"background:#f9fafb;\"><b>Vigencia inicio</b></td><td>{member.membership_start_date or '-'}</td></tr>
                <tr><td style=\"background:#f9fafb;\"><b>Vigencia fin</b></td><td>{member.membership_end_date or '-'}</td></tr>
                <tr><td style=\"background:#f9fafb;\"><b>Precio</b></td><td>${member.membership_price if member.membership_price is not None else '-'}</td></tr>
                <tr><td style=\"background:#f9fafb;\"><b>Código único</b></td><td>{member.qr_uuid or '-'}</td></tr>
              </table>
              <p style=\"margin:16px 0 8px;\">Tu QR de acceso:</p>
              <p style=\"margin:0 0 8px;\"><a href=\"{member.qr_image_url or '#'}\">Ver QR</a></p>
            </td></tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""


def _qr_refresh_template(member: GymMember) -> str:
    return f"""
<!doctype html>
<html>
  <body style=\"margin:0;padding:0;background:#f5f5f5;font-family:Arial,sans-serif;\">
    <table role=\"presentation\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" style=\"background:#f5f5f5;padding:20px 0;\">
      <tr>
        <td align=\"center\">
          <table role=\"presentation\" width=\"600\" cellpadding=\"0\" cellspacing=\"0\" style=\"max-width:600px;background:#ffffff;border-radius:8px;overflow:hidden;\">
            <tr><td style=\"background:#111827;color:#fff;padding:20px;font-size:22px;font-weight:bold;\">Academia del Barrio</td></tr>
            <tr><td style=\"padding:24px;color:#111827;\">
              <h2 style=\"margin:0 0 12px;\">Nuevo QR generado</h2>
              <p style=\"margin:0 0 16px;\">Hola {member.first_name}, tu código QR fue actualizado.</p>
              <table role=\"presentation\" width=\"100%\" cellpadding=\"8\" cellspacing=\"0\" style=\"border:1px solid #e5e7eb;border-collapse:collapse;\">
                <tr><td style=\"background:#f9fafb;\"><b>Nuevo código</b></td><td>{member.qr_uuid or '-'}</td></tr>
              </table>
              <p style=\"margin:16px 0 8px;\">Tu nuevo QR:</p>
              <p style=\"margin:0 0 8px;\"><a href=\"{member.qr_image_url or '#'}\">Ver QR</a></p>
            </td></tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""
