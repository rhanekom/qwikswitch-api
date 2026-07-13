# Releasing `qwikswitch-api`

Releases are published to [PyPI](https://pypi.org/project/qwikswitch-api/)
automatically by the [`release.yml`](.github/workflows/release.yml) workflow
using **PyPI Trusted Publishing** (OIDC). No API token is stored in the repo or
in GitHub secrets — PyPI verifies the workflow's signed OIDC identity instead.

## One-time setup on PyPI (do this once, before the first automated release)

The trusted publisher must be registered against the existing project on PyPI:

1. Sign in to PyPI and open the project's management page:
   <https://pypi.org/manage/project/qwikswitch-api/settings/publishing/>
2. Under **Add a new publisher → GitHub**, enter:
   - **Owner:** `rhanekom`
   - **Repository name:** `qwikswitch-api`
   - **Workflow name:** `release.yml`
   - **Environment name:** `pypi`
3. Save. (No secret is generated — this is the whole point of OIDC.)

The **environment name must be `pypi`** to match the `environment: pypi` block in
`release.yml`. Optionally, in GitHub → Settings → Environments → `pypi`, add
protection rules (e.g. required reviewers) so a human approves each publish.

## Cutting a release

1. **Bump the version** in `pyproject.toml` (`[project].version`), e.g.
   `0.0.11` → `0.0.12`. This is the single source of truth for the version.
2. **Land it on `main`** through the normal PR flow so CI (lint + tests) is
   green on the commit you intend to tag.
3. **Tag the release commit** with the exact version (no `v` prefix) and push
   the tag:

   ```bash
   git tag 0.0.12
   git push origin 0.0.12
   ```

4. The push triggers `release.yml`, which:
   - checks the tag name equals the `pyproject.toml` version (fails otherwise),
   - runs the test suite,
   - builds the sdist + wheel with `uv build`,
   - publishes to PyPI via Trusted Publishing, generating
     [PEP 740](https://peps.python.org/pep-0740/) attestations automatically.

5. Confirm the new version at
   <https://pypi.org/project/qwikswitch-api/> and that the GitHub Actions run
   succeeded.

## Notes

- **Tag scheme:** plain semver, no `v` prefix (matching existing tags
  `0.0.2` … `0.0.11`). The workflow trigger only matches `N.N.N`.
- **Version mismatch guard:** if the tag and `pyproject.toml` version disagree,
  the build job fails before anything is published.
- **Manual fallback:** if you ever need to publish by hand, build with
  `uv build` and upload with `uv publish` (or `uv run twine upload dist/*`)
  using a PyPI API token. PyPI is immutable — a version can never be
  re-uploaded or overwritten, so bump the version rather than trying to replace
  an existing release.
- **Cross-repo:** the Home Assistant integration `hass-qwikswitch-api` pins this
  package in `custom_components/qwikswitch_api/manifest.json`. Bump that pin
  there after a release if the integration should pick up the new version.
