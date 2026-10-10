# Café Aurora landing page

## Outcome and scope
Provide a responsive, accessible Spanish-language café concept for the Tarea 3
assignment, using dependency-free HTML and CSS. All human-facing page text,
metadata and accessible descriptions use neutral Spanish, with `lang="es"`.
The café and menu are fictional; purchases, reservations and visits are unavailable.

The bounded writer may edit only `index.html`, `README.md`,
`tests/test_landing.py` and this document. Keep `styles.css`, CSS classes, IDs,
internal anchor destinations and code identifiers unchanged. Preserve untracked
`.atl/` and `tests/__pycache__/`; do not stage or publish them.

## Work units
- [x] T1: Provide the static landing and structural checks.
- [x] T2: Provide Spanish page content, metadata, accessibility labels,
  preview/testing/hosting instructions and deterministic locale checks.
- [x] T3: Parent reruns the functional checks and assesses the publication candidate.

T2 route: delegated direct, sole bounded writer.
Acceptance includes meaningful structural coverage, valid internal anchors,
fictional academic disclosure and unchanged layout rules. The menu has three
named concept drinks and ordinal card numbers, not prices; no prices were invented.
README and page copy use neutral Spanish; test identifiers remain English.

## Observed local verification
Configured TDD mode: not configured, as recorded in this task. The default
deterministic test-first policy applies.

| Check | Observed result |
| --- | --- |
| `python3 -m unittest discover -s tests -v`, before HTML edits | RED: 12 tests, 33 failed assertions/subtests, 0 errors, 0 skips |
| Same command, after implementation | GREEN: 12 tests, 0 failures, 0 errors, 0 skips |
| `git diff --check` | Exit 0, no whitespace errors |
| Parent rerun: `python3 -m unittest discover -s tests -v` | 12 tests passed, 0 failures/errors/skips |
| Native risk assessment, excluded untracked inventory declared | Medium; `review_due=false`, `under_budget`; no review approval claimed |
| Local HTTP smoke command below | `/`: HTTP 200, `text/html`, 6070 bytes; `/styles.css`: HTTP 200, `text/css`, 8634 bytes; server shut down |
| Browser visual/keyboard/contrast review | Not performed; unavailable through this writer's browser tooling |
| Live deployment verification | Not performed; pending publication |

Coverage includes document language, exact title and description, UTF-8,
viewport, all four explicit accessible names, illustration captions,
representative navigation/menu/story/space/footer copy, heading references,
unique IDs, internal anchors, academic disclosure, dependency restrictions
and responsive/focus CSS rules. A bounded CSS content check found only empty
pseudo-element strings and no external URLs. No missed human-facing page
strings were identified by source review; tests are not exhaustive linguistic
or visual validation.

### Exact local HTTP smoke command
Run from the repository root. The standard-library server binds only to
`127.0.0.1`, chooses an ephemeral port and shuts down in `finally`.

```sh
python3 - <<'PY'
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.request import urlopen

root = Path.cwd()
handler = partial(SimpleHTTPRequestHandler, directory=str(root))
server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
thread = Thread(target=server.serve_forever, daemon=True)
thread.start()
try:
    for path, expected_type in (('/', 'text/html'), ('/styles.css', 'text/css')):
        with urlopen(f'http://127.0.0.1:{server.server_port}{path}', timeout=5) as response:
            body = response.read()
            content_type = response.headers.get_content_type()
            assert response.status == 200, response.status
            assert content_type == expected_type, content_type
            assert body, 'Empty response'
            print(f'{path}: HTTP {response.status}, {content_type}, {len(body)} bytes')
finally:
    server.shutdown()
    server.server_close()
    thread.join(timeout=5)
    assert not thread.is_alive(), 'Server did not stop'
    print('Localhost server shut down.')
PY
```

## Delivery boundary and next step
Keep the page, tests and documentation together as one coherent work unit.
The four writer-authorized files define the work-unit rollback boundary;
no CSS change or dependency installation was needed. Readable formatting and
coverage take priority over the advisory 400-line review budget.

Normalize text before final checks and native review; run no source-mutating
checks after freeze. The parent handles independent review, Git operations and
publication. The writer does not commit, change branches, push or use credentials.
The user authorized a single initial publication commit for `main` in
`Cesar0902/cafeteria-web`, using an exact-boundary force-with-lease. Only the five
project files are included; `.atl/` and `tests/__pycache__/` remain local.
External copies and hosting deployment retention are outside this operation.
Git publication is recorded separately in the recovery mirror; live deployment
and visual checks remain pending. No deployed result is claimed.
