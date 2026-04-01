# Project Requirements: Multi-Tenant Scalable Scheduler

## 1. Project Overview
The objective is to build a **Multi-Tenant Scheduling Platform** where independent companies can manage their own booking rules, event types, and third-party integrations (Google Calendar and Stripe) with total data isolation.

## 2. Core Architecture
The system will follow a **Shared Database, Shared Schema** approach with strict **Row-Level Filtering** (or `django-tenants` for schema isolation) to ensure that a Company Admin only interacts with their own data.

### Key Components:
* **Django Core:** Handles User Authentication, RBAC (Role-Based Access Control), and the Business Logic for bookings.
* **n8n Integration Layer:** Acts as the "glue" for external APIs. Django will emit webhooks to n8n, which will then talk to Google Calendar and Stripe.
* **PostgreSQL:** Chosen for its robustness in handling complex relational queries and time-range overlaps.

---

## 3. Functional Requirements

### **Company & User Management**
* **Multi-Tenancy (Isolated Schemas):** Each `Company` acts as a tenant with a dedicated PostgreSQL schema (via `django-tenants`). This ensures 100% data isolation at the database level.
* **Independent Credentials:** Each company stores its own **Stripe Secret Key** and **Google OAuth** tokens, which must be encrypted in the database using `django-cryptography`.

### **Event Type Configuration**
The system supports highly customizable `EventType` models within each tenant:
* **Custom Duration:** Defines the length of the slot (e.g., 30, 60 min).
* **Payment Logic:**
    * **Pre-paid:** Booking confirmed only after Stripe webhook.
    * **Post-paid:** Booking confirmed immediately; invoiced after the event via n8n.
* **Overlap Management:** A boolean flag `allow_overlap`. If `False`, the system runs a conflict check during the `Booking.clean()` process.

---

## 4. Integration Workflow (via n8n)

| Trigger Event | Source | Action in n8n |
| :--- | :--- | :--- |
| **New Booking** | Django Webhook | Create Event in the specific Company's **Google Calendar**. |
| **Payment Success** | Stripe Webhook | Update Django Database status to `PAID`. |
| **Post-paid Event End** | Cron Job/n8n | Generate and send **Stripe Invoice** to the client. |

---

## 5. Technical Specifications

### **Data Model (Detailed Architecture)**

#### **App: `customers` (Shared - Public Schema)**
* **Client (Tenant):** `schema_name`, `name`, `created_on`, `is_active`.
* **Domain:** `domain` (e.g., `company.domain.com`), `tenant` (FK), `is_primary`.

#### **App: `scheduler` (Tenant - Isolated Schemas)**
* **CompanyProfile:** `stripe_public_key`, `stripe_secret_key` (Encrypted), `google_calendar_id`, `logo`.
* **EventType:** `title`, `duration_minutes`, `price`, `payment_model` (PRE/POST), `allow_overlap` (BOOL).
* **Booking:** `event_type` (FK), `client_name`, `client_email`, `start_time`, `end_time` (Auto-calculated), `status` (PENDING/CONFIRMED/PAID).

### **Development Standards**
* **Language:** Python/Django.
* **Theme:** `django-unfold` for a modern, professional administrative interface.
* **API:** Django Rest Framework (DRF) for public availability check.

---

## 6. Scalability Strategy
1. **Schema Isolation:** Prevents cross-tenant data leaks and allows for easier backups/migrations per company.
2. **Offload I/O:** API heavy-lifting (Google/Stripe) is delegated to **n8n**.
3. **Indexing:** Database indexes on `start_time` and `end_time` within each schema to keep conflict checks O(1) relative to total system size.

---

# Project phases:

---

## Phase 1: Tenant Infrastructure (`django-tenants`)
Implement the multi-database schema approach for total isolation.

* **Shared vs. Tenant Apps:** 
    * `SHARED_APPS`: `django_tenants`, `customers`, `django.contrib.admin`, `django.contrib.auth`.
    * `TENANT_APPS`: `scheduler`, `django.contrib.contenttypes`, `django.contrib.admin`.
* **Middleware & Router:** Configure `TenantMainMiddleware` and `TenantSyncRouter`.
* **Domain Routing:** Set up sub-domain mapping to automatically route requests to the correct schema.

---

## Phase 2: Administrative Control (Django Admin / Unfold)
The Django Admin acts as the primary "Product" for the Company Admin.

* **Unfold Customization:**
    * Dynamic `site_header` and branding based on the active `CompanyProfile`.
    * Dashboard summary components for "Pending vs Paid" bookings.
* **ModelAdmins:**
    * **Bookings:** Use `list_filter` for status/dates and `list_display` with status badges.
    * **Encrypted Storage:** Integrate `django-cryptography` for API keys within `CompanyProfile`.
    * **Auto-Validation:** Implement conflict checks in `Booking.clean()` to enforce `allow_overlap` rules.

---

## Phase 3: Public API & The Scheduling Engine
The APIs will be read-only and public, designed to feed your calendar UI.

* **Public DRF Endpoints:** Create unauthenticated endpoints that return available slots and event types.
    * *Note:* Since it's public, ensure you only expose `start_time`, `end_time`, and `title`—never client emails or private notes.
* **Overlap Validation Logic:** Even without "additional logic," the core conflict check must remain to prevent double-booking.
    > $$\text{Conflict} = (\text{NewStart} < \text{ExistingEnd}) \text{ AND } (\text{NewEnd} > \text{ExistingStart})$$
* **The `allow_overlap` Flag:** A simple `if not event_type.allow_overlap:` block in the `Booking.save()` method to trigger the validation.



---

## Phase 4: The n8n "Glue" Layer
With the schema isolation in place, n8n needs to know which tenant is talking to it.

* **Webhook Payload:** Every time a booking is saved in the Admin, Django sends a webhook to n8n including the **Tenant ID/Schema Name**.
* **Dynamic Credentials:** n8n will use the API keys provided in the webhook payload to authenticate with the specific company's **Google Calendar** or **Stripe** account.
* **Stripe Webhook Receiver:** A public endpoint in Django that receives the "Payment Success" signal from n8n and updates the booking status in the specific tenant's schema.

---

## Phase 5: Deployment & Scalability (Coolify)
* **VPS Setup:** Deploying the Django app on **Coolify** using a Dockerized setup.
* **PostgreSQL Management:** Ensure the DB user has `CREATEDB` and `SUPERUSER` permissions (required by `django-tenants` to manage schemas).
* **Static Assets:** Since you're using Django Admin, ensure `collectstatic` is handled correctly so all company sub-domains have access to the CSS/JS for the admin panel.



This setup is very "Django-centric," making it extremely fast to develop since the Admin handles 90% of your UI needs. Are you planning to use a specific theme for the Django Admin, or will the default one suffice?