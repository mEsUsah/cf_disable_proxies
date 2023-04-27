# Cloudflare tools
Repo of cloudflare tools I create.

## Disable all proxies
By default cloudflare enables reverse proxy on all DNS records when you import them into a DNS Zone.
This tool enables you to disable proxy on all DNS records in a zone. You can then later manually activate reverse proxy on the records you want to activate.

### Usage
* Change variables at the start of the script
* Run script

```bash
python3 disable_all_proxies.py
```
