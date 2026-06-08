#!/bin/sh
if [ "$DASFLAG" ]; then
    INSERT_FLAG="$DASFLAG"
elif [ "$FLAG" ]; then
    INSERT_FLAG="$FLAG"
elif [ "$GZCTF_FLAG" ]; then
    INSERT_FLAG="$GZCTF_FLAG"
else
    INSERT_FLAG="flag{TEST_Dynamic_FLAG}"
fi

echo "$INSERT_FLAG" > /flag
chmod 644 /flag

if [ -f /app/static/.git/config ]; then
    cd /app/static
    git filter-branch -f --env-filter 'GIT_AUTHOR_DATE="2025-03-01T10:00:00+08:00"; GIT_COMMITTER_DATE="2025-03-01T10:00:00+08:00"' --tree-filter "sed -i 's|__PLACEHOLDER_FLAG__|$INSERT_FLAG|g' config.php 2>/dev/null || true" --all 2>/dev/null || true
    rm -rf .git/refs/original/ 2>/dev/null || true
    git reflog expire --expire=now --all 2>/dev/null || true
    git gc --prune=now --aggressive 2>/dev/null || true
fi
