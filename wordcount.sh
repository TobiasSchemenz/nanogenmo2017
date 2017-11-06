cat test.md | wc -w
cat test.md | tr -d '[:punct:][:digit:]' | wc -w