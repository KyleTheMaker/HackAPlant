# Run fastapi
    ## Install UV[https://docs.astral.sh/uv/getting-started/installation/]
    ## sync UV command : `uv sync` This is same as npm install
    ## Local Dev Command: `uv run uvicorn main:app --port 8000`

    
# Tunnel using cloudflare accountless
    ## Install Cloudflare[https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/downloads/]
    ## Run local app using Local Dev Command
        ### if regular local dev command does not work then use the below
        ### `uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
    ## Run cloudflare tunnel
        ### tunnel command: `cloudflared tunnel --protocol http2 --url http://localhost:8000

    This will give you a free url that is accessible from anywhere on internet.

#### cloudflare Tunnel information[https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/]

