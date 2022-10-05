flake8
if ! flake8;
  then
    echo "Flake8 checks failed"
    exit 1
  fi

if ! pytest --asyncio-mode=auto;
  then
    echo "Pytest tests failed"
    exit 1
  fi
