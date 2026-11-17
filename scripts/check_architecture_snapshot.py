#!/usr/bin/env python3
"""Conservative early-warning Rails architecture scanner, NOT a proof of compliance.

Uses textual patterns deliberately: reports likely violations only; no repository class
resolution or comprehensive Ruby AST analysis. Never use 0 as a compliance attestation.
"""
import argparse
import json
import re
import sys
from pathlib import Path

CALLBACK = re.compile(r'^\s*(?:before|after|around)_(?:validation|save|create|update|destroy|commit|rollback|initialize|find|touch)\b')
DB_MUTATION = re.compile(r'\b(?:create!|update!|destroy!|save!|perform_later|perform_now)\b')
SQL_IN_VIEW = re.compile(r'\.(?:where|joins|left_joins|find_by|group|having|order|pluck|count|find)\s*\(')
DIRECT_JOB = re.compile(r'\b(?:perform_later|perform_now)\s*\(')
ERB_ASSIGN = re.compile(r'<%[=-]?\s*(?:@[a-z_]\w*|[a-z_]\w*)\s*(?:\|\|=|&&=|=(?!=|>))')
POLICY_SQL = re.compile(r'\.exists\?(?!\w)|\.(?:count|pluck|find|find_by|first|last|load|to_a|sum|average|maximum|minimum|delete_all|update_all)\b|\b(?:find_by_sql|connection\.execute)\b')
POLICY_POSSIBLE_SQL = re.compile(r'\.(?:any\?|none\?|empty\?)(?!\w)|\.size\b')
COMMENT_LINE = re.compile(r'^\s*#(?!\!)')
INTERACTOR_CALL = re.compile(r'\b[A-Z]\w*(?:::[A-Z]\w*)+\.call!?\s*\(')


def scan(root, changed_files=None):
    findings = []
    files = sorted(root.rglob('*'))
    changed = {str(Path(x)).replace('\\', '/') for x in changed_files} if changed_files is not None else None
    for path in files:
        if not path.is_file() or any(segment in {'vendor', 'tmp', '.git', 'node_modules'} for segment in path.relative_to(root).parts):
            continue
        relative = path.relative_to(root)
        s = str(relative)
        if changed is not None and s not in changed:
            continue
        if not (s.endswith('.rb') or s.endswith('.jbuilder') or s.endswith('.erb')):
            continue
        try:
            body = path.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            continue
        lines = body.splitlines()
        if s.startswith('lib/jumpstart/') and changed is not None:
            findings.append({'file': s, 'line': 1, 'rule': 'FT-003', 'kind': 'CANDIDATE', 'message': 'Changed lib/jumpstart/ file: move customization into approved app/ override.'})
        def add(i, rule, message):
            findings.append({'file': s, 'line': i, 'rule': rule, 'kind': 'CANDIDATE', 'message': message})
        in_scope = False
        in_policy_scope = False
        for i, line in enumerate(lines, 1):
            # Heuristic: recognize conventional nested `class Scope` sections.
            if s.startswith('app/policies/') and re.search(r'^\s*class\s+Scope\b', line):
                in_policy_scope = True
            if s.startswith('app/policies/') and re.search(r'^\s*def\s+resolve\b', line):
                in_scope = True
            if line.lstrip().startswith('#'):
                if changed is not None and COMMENT_LINE.search(line) and not s.endswith('.erb'):
                    add(i, 'FT-005', 'Added or changed code comment; inspect diff to distinguish existing comments.')
                continue
            if s.startswith('app/policies/') and re.search(r'^\s*def\s+[a-z_]\w*\?', line):
                in_scope = False
            if s.startswith('app/policies/') and not in_policy_scope and not in_scope:
                if POLICY_SQL.search(line):
                    add(i, 'FT-002', 'Potential SQL execution in Pundit policy; policy predicates must not fire SQL. Scope#resolve is exempt.')
                elif POLICY_POSSIBLE_SQL.search(line):
                    add(i, 'FT-002', 'Collection inspection might execute SQL in policy; review loaded-state semantics.')
            if s.endswith('.erb') and ERB_ASSIGN.search(line):
                add(i, 'FT-004', 'Variable assignment or initialization in ERB view is prohibited.')
            if s.startswith('app/models/') and CALLBACK.search(line):
                add(i, 'AR-005', 'New custom callback may require approval; check diff and local framework.')
            if ('app/views/' in s or s.startswith('app/views/')) and SQL_IN_VIEW.search(line):
                add(i, 'VW-004', 'Query construction in view; inspect relation provenance.')
            if s.startswith('app/jobs/') and DB_MUTATION.search(line) and not DIRECT_JOB.search(line):
                add(i, 'BJ-001', 'Potential mutation inside job; recurring batch selection is a permitted exception.')
            if s.startswith('app/models/') and DIRECT_JOB.search(line):
                add(i, 'AR-008', 'Job enqueued in model; use organizer after hook.')
        # No class-resolution available. Interactor/organizer `.call` patterns
        # cannot be reliably categorized, so do not report as certain violations.
    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('repo', type=Path)
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--changed-file', action='append', default=None, help='Limit scanning to specified repo-relative changed paths (repeatable). Enables FT-003 and FT-005 candidate findings.')
    args = ap.parse_args()
    if not args.repo.is_dir():
        ap.error('repo path must be a directory')
    findings = scan(args.repo.resolve(), args.changed_file)
    result = {'status': 'HEURISTIC_ONLY', 'findings': findings,
              'note': 'Zero findings does not establish architecture compliance. Required semantic checks remain UNVERIFIED.'}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for f in findings:
            print(f"{f['file']}:{f['line']}: {f['rule']}: {f['message']}")
        print(result['note'])
    return 2 if findings else 0


if __name__ == '__main__':
    sys.exit(main())
