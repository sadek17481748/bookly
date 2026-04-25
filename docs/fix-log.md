# Development fix log

Short notes recorded next to bug-fix commits during local testing.

- Manual checklist (search with `?q=`): titles were missed when I briefly used case-sensitive contains; restored ilike so mixed-case queries match the brief.
- Manual checklist (review ownership): cross-user delete could be triggered before the guard landed; now only the author can delete (matches blocked-delete scenario).
- Manual checklist (checkout continuation): login dropped the return URL; preserved next on the form and after login so checkout could resume.
- Manual checklist (empty-cart checkout): checkout could post with no lines; short-circuit with flash and redirect to cart like the checklist expects.
- Manual checklist (admin analytics): non-admin could open the dashboard briefly; decorator now returns forbidden for normal accounts.
- Manual checklist (catalogue list): older seed rows kept empty jacket paths; init-db backfills cover_url when the title already exists.
