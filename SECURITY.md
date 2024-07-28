# Security Policy

## Releases

I thought it was impossible to attack via fonts, but I researched the topic and found out about [CVE-2015-2426](https://nvd.nist.gov/vuln/detail/CVE-2015-2426). So just in case, here are the rules that apply to built font files published in Releases:

Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| CVSS v3.0 | Supported Versions                        |
| --------- | ----------------------------------------- |
| 9.0-10.0  | Releases within the previous three months |
| 4.0-8.9   | Most recent release                       |

## Builder

In the case of the build environment, vulnerabilities found in the `master` branch that have a CVSS v3.0 Rating greater than 4.0 are considered.

## Reporting a Vulnerability

Please report (suspected) security vulnerabilities to
**[misha@myrt.co](mailto:misha@myrt.co)**. I'll respond in 3 days.

If the issue is confirmed, i will release a patch as soon
as possible depending on complexity but historically within a few days.