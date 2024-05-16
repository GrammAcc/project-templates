# Python/Flask

This branch contains boilerplate for spinning up a new Flask project.

To use this template, clone this branch, delete the .git folder, then run:
```bash
    sed -i -- "s/packagename/project_package_name/g" **/*.py(.^D) **/*.toml(.^D) **/*.json(.^D) Caddyfile
    mv src/packagename src/project_package_name
```

Where `project_package_name` is the name of the new project being started.

You may need to change the `project_package_name.utils.get_domain` function to match how the domain is resolved both locally and in production if the package name differs from the domain name.

If `api.project_package_name.local` doesn't resolve with the Caddy reverse proxy server, you need to add it to your local hosts file.
