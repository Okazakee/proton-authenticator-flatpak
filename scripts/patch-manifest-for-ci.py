#!/usr/bin/env python3
"""Patch the Flatpak manifest for CI bundle builds.

Replaces the type:extra-data source with type:file (the binary extracted
from the RPM on the runner) so the resulting .flatpak bundle can be
installed directly without needing extra-data download support.

The original manifest keeps type:extra-data for Flathub submission.
Output is written to ci-build.yml.
"""
import yaml

with open('io.github.Okazakee.ProtonAuthenticator.yml') as f:
    manifest = yaml.safe_load(f)

for module in manifest['modules']:
    # Build-commands: drop apply_extra / wrapper installs; add direct binary install
    new_cmds = ['install -Dm755 proton-authenticator /app/bin/proton-authenticator']
    for cmd in module.get('build-commands', []):
        if 'apply_extra' in cmd or 'proton-authenticator.sh' in cmd:
            continue
        new_cmds.append(cmd)
    module['build-commands'] = new_cmds

    # Sources: drop script sources; replace extra-data with extracted binary file
    new_sources = []
    for src in module.get('sources', []):
        if src.get('type') == 'extra-data':
            new_sources.append({
                'type': 'file',
                'path': 'usr/bin/proton-authenticator',
                'dest-filename': 'proton-authenticator',
            })
        elif src.get('type') == 'script' and src.get('dest-filename') in (
            'apply_extra', 'proton-authenticator.sh'
        ):
            pass  # drop
        else:
            new_sources.append(src)
    module['sources'] = new_sources

with open('ci-build.yml', 'w') as f:
    yaml.dump(manifest, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

print('Generated ci-build.yml for CI bundle build.')
