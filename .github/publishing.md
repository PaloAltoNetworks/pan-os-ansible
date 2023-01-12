# Publishing to AutomationHub and Galaxy

## Publishing Process

Publishing to both AutomationHub and Galaxy is done with the same methodology per destination, but with different targets. An ```ansible.cfg``` file is used to define the targets and per-target parameters. Currently, the release process performed by GitHub Actions creates this ```ansible.cfg``` file on the fly, injecting sensitive values from GitHub secrets as required. The current sensitive values are stored in corporate vault, and the values can be sourced/refreshed from [the AutomationHub API token page](https://console.redhat.com/ansible/automation-hub/token):
- AUTOMATION_HUB_API_TOKEN -> "Load token" button on the page
- AUTOMATION_HUB_URL -> Server URL value on the page
- AUTOMATION_HUB_SSO_URL -> SSO URL value on the page

With the ```ansible.cfg``` file created and populated with the relevant values, GitHub Actions continues to publish to both Galaxy and AutomationHub, with two separate ```ansible-galaxy collection publish``` commands.

## Keeping the API Token Active

Inactive AutomationHub API tokens last for 30 days. In order to keep the token live between releases, a command described [here](https://console.redhat.com/ansible/automation-hub/token) should be executed. This command is currently executed by GitHub Actions on a regular schedule, and requires the current API token be passed as a parameter.

## Documentation/References
- https://docs.ansible.com/ansible/latest/galaxy/user_guide.html#configuring-the-ansible-galaxy-client
- https://access.redhat.com/documentation/en-us/red_hat_ansible_automation_platform/1.2/html/getting_started_with_red_hat_ansible_automation_hub/index
