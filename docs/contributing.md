# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit helps,
and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/PaloAltoNetworks/pan-os-ansible/issues.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" is open to whoever
wants to fix it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" is
open to whoever wants to implement it.

### Submit Feedback

The best way to send feedback is to file an issue at
https://github.com/PaloAltoNetworks/pan-os-ansible/issues.

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions 
  are welcome :)

## Get Started!

Ready to contribute some code? Here's how to set up `pan-os-ansible` for local development.

1. Install Python 3.6 or higher, along with Ansible

   Development must be done using Python 3.6 or higher.  Ansible still technically
   supports Python 2.7, but all code should target Python 3.6 or higher.

2. Fork the `pan-os-ansible` repo on GitHub.

3. Create a top level directory for your work, for example `ansible-hacking`:

```
$ mkdir ansible-hacking
$ cd ansible-hacking/
```

3. Clone your fork locally, using a special directory name so that Ansible understands
   it as a collection:

```
$ mkdir -p ansible_collections/paloaltonetworks
$ git clone https://github.com/your-username/pan-os-ansible.git ansible_collections/paloaltonetworks/panos
```

4. Create a playbooks directory, and add our top level directory to `ansible.cfg`:

   Adding our top level directory to `ansible.cfg` will interpret the directory
   `ansible_collections/paloaltonetworks/panos` as the collection
   `paloaltonetworks.panos` without us having to build and install the collection each
   time!

   You can add any test playbooks to the `playbooks/` directory.  Any
   `ansible-playbook` runs from this directory will pick up our custom `ansible.cfg`
   file.

```
$ mkdir playbooks
$ echo "[defaults]\ncollections_paths = .." > playbooks/ansible.cfg
``` 

5. Create a branch for local development

```
$ cd ansible_collections/paloaltonetworks/panos
$ git checkout -b name-of-your-bugfix-or-feature
```

6. Now you can make your changes locally, and test them out by running
`ansible-playbook` from the `playbooks/` directory.

7. When you're done making changes, check that your changes pass `ansible-test sanity`:

```
$ ansible-test sanity --local
```

8. Commit your changes and push your branch to GitHub:

```
$ git add -A
$ git commit -m "Your detailed description of your changes."
$ git push origin name-of-your-bugfix-or-feature
```

9. Submit a pull request through the GitHub website.

## Publish a new release (for maintainers)

This workflow requires node, npm, and semantic-release to be installed locally:

```
$ npm install -g semantic-release@^17.1.1 @semantic-release/git@^9.0.0 @semantic-release/exec@^5.0.0 conventional-changelog-conventionalcommits@^4.4.0
```

### Test the release process

Run `semantic-release` on develop:

```
semantic-release --dry-run --no-ci --branches=develop
```

Verify in the output that the next version is set correctly, and the release notes are generated correctly.

### Merge develop to master and push

```
git checkout master
git merge develop
git push origin master
```

At this point, GitHub Actions builds the final release, and uploads it to Ansible Galaxy.

### Merge master to develop and push

Now, sync develop to master to add the new commits made by the release bot.

```
git fetch --all --tags
git pull origin master
git checkout develop
git merge master
git push origin develop
```

Now you're ready to branch again and work on the next feature.
