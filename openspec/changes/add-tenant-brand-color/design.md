# Design: Add Tenant Brand Color

## Context
Tenants already have a `CompanyProfile` for their specific settings (Stripe keys, logo, etc.). This makes it the ideal place to store branding elements like the brand color.

## Goals
- Allow per-tenant brand color customization.
- Transparently apply the color to both the Unfold admin interface and custom CSS.
- Provide a sensible fallback for the public schema and tenants without a set color.

## Decisions

### 1. Storage & Validation: `CompanyProfile`
- **What**: Add a `brand_color` field (CharField) to `scheduler.CompanyProfile`.
- **Validation**: Include a `RegexValidator` to ensure the value is either a valid Hex code or a well-formed OKLCH function.
- **Admin**: Use a `TextInput` with `type="color"` for a native color picker UI.

### 2. Implementation: Dynamic Palette
- **What**: Instead of a single variable, define light (400), main (500), and dark (600) shades.
- **How**: The `utils.callbacks.get_brand_config` helper will derive these shades. For OKLCH colors, this can be done by simple L (lightness) adjustments in a string template.
- **Why**: Ensures that hover effects, active states, and decorative elements (like accents in the Markdown editor) look polished and consistent with the base brand color.

### 3. Distribution: Centralized Config
- **What**: Implement `utils.callbacks.get_brand_config` (config logic) and `project.context_processors.branding` (template helper).
- **Why**: Centralizing logic in `utils` follows DDRY principles and avoids splitting tenant-resolution logic between multiple files.

### 4. Integration: Unfold Color Mapping
- **What**: Update `UNFOLD['COLORS']['primary']` in `settings.py` for shades 400, 500, and 600 to reference the CSS variables: `var(--color-primary-XXX)`.
- **Why**: This ensures that even if our manual override fails, the system has a valid default color that matches our current branding.

## Risks / Trade-offs
- **Risk**: Overriding `--color-primary-500` only might leave other related shades (e.g. 600, 400) inconsistent.
- **Mitigation**: We can use CSS `color-mix()` or `oklch()` color-space manipulation in the template to derive other shades from the single primary color if needed, or simply override the most critical ones with the same value for simplicity.

## Migration Plan
1. Add `brand_color` to `CompanyProfile` with a default value.
2. Run migrations for each tenant (`python manage.py migrate_schemas`).
3. Update templates and settings.
4. Update custom CSS.

## Open Questions
- Should we provide a color picker in the admin? (Yes, by using a widget).
