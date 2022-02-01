# Release procedure

##  Local install test

```
python setup.py develop
```

## Publish

1. Enter to venv
    ```
    source ./venv/bin/activate
    ```
2. Increase version in `napalm_h3c_comware/__init__.py`

3. Add tag to release a new version
    ```
    git tag -a <version> -m <comment>
    ```

4. Push to my github
    ```
    git push origin --tags
    ```

5. Push to napalm-automation-community
    ```
    git push community --tags
    ```

6. Build dist & upload to pypi.org
    ```
    python -m build

    python -m twine upload dist/*
    ```

