# Service Messages

## Rôle du service
Le service **Messages** est responsable de la production des documents (ex. fichiers PDF) et de l'envoi des messages à destination des clients. Il fonctionne principalement en réaction aux événements asynchrones émis par les autres briques du système (réservations, paiements, passages d'accès).

---

## Informations générales

| Paramètre | Valeur |
| --- | --- |
| **Version actuelle** | `0.1.0` |
| **URL du service déployé** | `https://messages.api.domain.com` |
| **Documentation Swagger/OpenAPI** | `https://messages.api.domain.com/swagger-ui` |

---

## Principales dépendances
Le service interagit avec les modules suivants via un bus de messages asynchrone :

* **Booking** : Réception des événements de confirmation de réservation pour la génération des confirmations et tickets d'entrée.
* **Access** : Réception des événements d'entrée/sortie pour l'émission de tickets ou notifications de passage.

---

## Objets métier

* **Notification**
  * `id` : Identifiant unique
  * `type` : Type de notification (ex. `EMAIL`, `SMS`, `PUSH`)
  * `recipient_ref` : Référence client ou destinataire
  * `content` : Contenu du message
  * `status` : Statut d'envoi (`PENDING`, `SENT`, `FAILED`)
  * `created_at` : Horodatage de création

* **Document**
  * `id` : Identifiant unique
  * `type` : Type de document (ex. `TICKET`, `RECEIPT`, `CONFIRMATION`)
  * `payload` : Données source utilisées pour la génération
  * `file_path` : URI / Chemin du fichier généré (ex. PDF)
  * `generated_at` : Horodatage de génération

---

## Exemples de workflows

1. **Réservation** : `Booking` émet `booking.confirmed` ➔ `Messages` génère la confirmation et le ticket PDF ➔ Fichier mis à disposition du client.
3. **Accès** : `Access` émet `access.event` ➔ `Messages` génère le reçu ou notification associé.
