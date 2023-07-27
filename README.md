# ThinkingABetterName

# Subdomain Status Checker

This Python script fetches subdomains for a given domain using the "crt.sh" API and checks the HTTP and HTTPS status codes for each subdomain. The script outputs the results in JSON format.

## Usage

1. Install the required packages:

        pip install requests

2. Run the script:

        python crtsh_subdomains_status.py

    Replace the value of the `domain_to_search` variable in the script with the domain you want to search for subdomains.

## Output

The output will be a JSON representation of the subdomains along with their corresponding HTTP and HTTPS status codes.

Note: The script handles unreachable domains gracefully and excludes them from the final output.

## Dependencies

    - Python 3.x
    - Requests library (installed via pip)

## License

  This project is licensed under the MIT License - see the [LICENSE](LICENSE)
