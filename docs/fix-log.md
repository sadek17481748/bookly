# Development fix log

Short notes recorded next to bug-fix commits during local testing.

- Manual checklist (search with `?q=`): titles were missed when I briefly used case-sensitive contains; restored ilike so mixed-case queries match the brief.
- Manual checklist (review ownership): cross-user delete could be triggered before the guard landed; now only the author can delete (matches blocked-delete scenario).
- Manual checklist (checkout continuation): login dropped the return URL; preserved next on the form and after login so checkout could resume.
