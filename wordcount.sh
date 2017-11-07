cat $1 | wc -w
cat $1 | tr -d '[:punct:][:digit:]' | wc -w