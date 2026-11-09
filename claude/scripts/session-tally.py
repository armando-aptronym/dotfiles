#!/usr/bin/env python3
"""Tally token usage for a Claude Code session or sub-agent transcript.

Usage:
  session-tally.py <session> [--from TEXT] [--tools N] [--json]
  session-tally.py --list

<session> is a session name (the custom title), a session id or id prefix, or the
path to a .jsonl transcript (a sub-agent's task output file works too).
--from TEXT counts only from the first user message containing TEXT, so one skill
run inside a longer session can be isolated (for example --from /finish-task).

Token fields come from each API call's usage record:
  input         uncached input tokens
  cache_write   tokens written to the prompt cache (new context)
  cache_read    tokens re-read from the cache (the whole prefix, every call)
  output        tokens generated
Dollar cost is not computed, because rates change.
"""
import argparse, glob, json, os, sys
from collections import Counter, OrderedDict

PROJECTS = os.path.expanduser('~/.claude/projects')


def titles():
    out = []
    for t in glob.glob(f'{PROJECTS}/*/*/custom-title.json'):
        try:
            title = json.load(open(t)).get('customTitle') or ''
        except Exception:
            continue
        sid = os.path.basename(os.path.dirname(t))
        proj = os.path.dirname(os.path.dirname(t))
        path = f'{proj}/{sid}.jsonl'
        if os.path.exists(path):
            out.append((os.path.getmtime(path), title, sid, path))
    return sorted(out, reverse=True)


def find(query):
    if os.path.isfile(query):
        return query
    for _, title, sid, path in titles():
        if query == title:
            return path
    for p in glob.glob(f'{PROJECTS}/*/*.jsonl'):
        if os.path.basename(p).startswith(query):
            return p
    for _, title, sid, path in titles():
        if query in title:
            return path
    return None


def text_of(content):
    if isinstance(content, str):
        return content
    return ''.join(b.get('text', '') for b in content if isinstance(b, dict) and b.get('type') == 'text')


def load(path):
    rows = []
    for line in open(path):
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    return rows


def tally(rows, start_text):
    start = 0
    if start_text:
        for i, r in enumerate(rows):
            if r.get('type') == 'user' and start_text in text_of(r.get('message', {}).get('content', '')):
                start = i
                break
        else:
            sys.exit(f'No user message containing {start_text!r} found.')

    calls = OrderedDict()
    tool_names = {}
    results = OrderedDict()
    for i, r in enumerate(rows):
        msg = r.get('message') if isinstance(r.get('message'), dict) else None
        if not msg:
            continue
        content = msg.get('content')
        if isinstance(content, list):
            for b in content:
                if b.get('type') == 'tool_use':
                    tool_names[b['id']] = b['name']
        if i < start:
            continue
        if r.get('type') == 'assistant':
            mid = msg.get('id') or f'row{i}'
            u = msg.get('usage', {}) or {}
            cur = calls.setdefault(mid, {'u': Counter(), 'tools': [], 'model': msg.get('model')})
            for k in ('input_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens', 'output_tokens'):
                cur['u'][k] = max(cur['u'][k], u.get(k, 0) or 0)
            for b in content or []:
                if b.get('type') == 'tool_use' and b['name'] not in cur['tools']:
                    cur['tools'].append(b['name'])
        elif r.get('type') == 'user' and isinstance(content, list):
            for b in content:
                if b.get('type') == 'tool_result' and b['tool_use_id'] not in results:
                    c = b.get('content')
                    if isinstance(c, list):
                        c = ''.join(x.get('text', '') for x in c if isinstance(x, dict))
                    results[b['tool_use_id']] = len(str(c or ''))
    return calls, tool_names, results


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('session', nargs='?')
    ap.add_argument('--from', dest='start', help='start counting at the first user message containing this text')
    ap.add_argument('--tools', type=int, default=8, help='how many of the largest tool results to list')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--list', action='store_true', help='list named sessions, newest first')
    a = ap.parse_args()

    if a.list:
        for _, title, sid, path in titles():
            print(f'{title}\t{sid}')
        return
    if not a.session:
        ap.error('give a session name, id or transcript path, or use --list')
    path = find(a.session)
    if not path:
        sys.exit(f'No transcript found for {a.session!r}. Try --list.')

    calls, tool_names, results = tally(load(path), a.start)
    if not calls:
        sys.exit('No assistant API calls found in that range.')

    keys = ('input_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens', 'output_tokens')
    total = Counter()
    for c in calls.values():
        for k in keys:
            total[k] += c['u'][k]
    first = next(iter(calls.values()))['u']
    last = list(calls.values())[-1]['u']
    ctx = lambda u: u['input_tokens'] + u['cache_creation_input_tokens'] + u['cache_read_input_tokens']
    models = sorted({c['model'] for c in calls.values() if c['model']})
    big = sorted(((n, tool_names.get(t, '?')) for t, n in results.items()), reverse=True)[:a.tools]

    summary = {
        'transcript': path,
        'models': models,
        'api_calls': len(calls),
        'input': total['input_tokens'],
        'cache_write': total['cache_creation_input_tokens'],
        'cache_read': total['cache_read_input_tokens'],
        'output': total['output_tokens'],
        'context_at_first_call': ctx(first),
        'context_at_last_call': ctx(last),
        'largest_tool_results_tokens_est': [{'tool': t, 'tokens_est': n // 4} for n, t in big],
    }
    if a.json:
        print(json.dumps(summary, indent=2))
        return

    print(f'transcript: {path}')
    print(f'models: {", ".join(models)}   api calls: {len(calls)}')
    print()
    print(f'{"#":>2} {"input":>7} {"cache_w":>8} {"cache_r":>8} {"output":>7}  tools')
    for n, c in enumerate(calls.values()):
        u = c['u']
        tools = ', '.join(t.replace('mcp__claude_ai_', '') for t in c['tools'])
        print(f'{n:>2} {u["input_tokens"]:>7} {u["cache_creation_input_tokens"]:>8} {u["cache_read_input_tokens"]:>8} {u["output_tokens"]:>7}  {tools}')
    print(f'{"":>2} {"-" * 7} {"-" * 8} {"-" * 8} {"-" * 7}')
    print(f'{"":>2} {summary["input"]:>7} {summary["cache_write"]:>8} {summary["cache_read"]:>8} {summary["output"]:>7}  total')
    print()
    print(f'context at first call: {summary["context_at_first_call"]:,} tokens')
    print(f'context at last call:  {summary["context_at_last_call"]:,} tokens '
          f'(+{summary["context_at_last_call"] - summary["context_at_first_call"]:,} added in this range)')
    print()
    print('largest tool results (chars/4, an estimate):')
    for n, t in big:
        print(f'  {n // 4:>7,}  {t.replace("mcp__claude_ai_", "")}')
    print()
    print('A call that follows a tool-schema load shows a large cache_w. cache_r is the whole prefix re-read each call,')
    print('so it grows with context size and with the number of calls.')


if __name__ == '__main__':
    main()
